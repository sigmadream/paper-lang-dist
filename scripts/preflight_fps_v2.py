"""Stage 0 analyzer-fairness and state-identity checks for fps-text-v2 (v1/abs_EXPERIMENT.md 3.3).

Applies the same kinds of edits to every reference solution of every problem and
records how far JPlag text Sym(reference, edited) moves per language. No model calls.

Usage: python scripts/preflight_fps_v2.py fps_v2.yaml
"""
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
import re
import sys

from rttdist.experiment_io import write_json, timestamp
from rttdist.fps_execution import EXTENSIONS
from rttdist.fps_experiment import load_config
from rttdist.fps_state import source_hash
from rttdist.jplag_similarity import measure

LANGUAGES=('cpp','haskell','prolog')
COMMENT={'cpp':'// diagnostic comment','haskell':'-- diagnostic comment','prolog':'% diagnostic comment'}
KEYWORDS={
    'cpp':set('include using namespace std int long double char bool void return if else for while do auto const '
              'main cin cout endl vector string true false break continue size push_back ios_base sync_with_stdio tie NULL '
              'nullptr static_cast unsigned sizeof struct class public private new delete'.split()),
    'haskell':set('module where import main do let in if then else case of data type newtype instance class deriving '
                  'print read words lines map show getContents getLine putStrLn putStr return IO Int Integer String '
                  'mod div fmap mapM_ otherwise True False'.split()),
    'prolog':set('main use_module library readutil read_string user_input split_string maplist number_string '
                 'atomic_list_concat writeln write nl is mod length nth0 nth1 msort sort append true false fail format'.split())}
OPERATOR_SWAPS=[('<=','>='),('>=','<='),('==','!='),('+','-'),('*','+'),('<','>'),('>','<'),('-','+')]

def identifier_edit(source,lang):
    words=Counter(w for w in re.findall(r'[A-Za-z_][A-Za-z0-9_]*',source) if w not in KEYWORDS[lang] and len(w)>=2)
    if not words:return None
    name=words.most_common(1)[0][0]
    replacement=('Q' if lang=='prolog' and name[0].isupper() else 'q')+'renamed_'+name.lower()
    return re.sub(r'\b'+re.escape(name)+r'\b',replacement,source),name

def operator_edit(source):
    for old,new in OPERATOR_SWAPS:
        index=source.find(old)
        if index>=0:return source[:index]+new+source[index+len(old):],old+'->'+new
    return None

def line_drop(source):
    lines=source.split('\n')
    body=[i for i,l in enumerate(lines) if l.strip()]
    if len(body)<3:return None
    i=body[len(body)//2]
    return '\n'.join(lines[:i]+lines[i+1:]),i+1

def variants(source,lang):
    out={'identical':(source,None),'whitespace':(source.replace(' ','  '),None),
         'comment':(COMMENT[lang]+'\n'+source,None),'short':('x',None)}
    for name,value in [('identifier',identifier_edit(source,lang)),('operator',operator_edit(source)),('line_drop',line_drop(source))]:
        if value is not None:out[name]=value
    return out

def state_identity_checks():
    base='int main() {\n  return 0;\n}\n'
    return {'crlf_equals_lf':source_hash(base.replace('\n','\r\n'))==source_hash(base),
            'cr_equals_lf':source_hash(base.replace('\n','\r'))==source_hash(base),
            'extra_space_differs':source_hash(base.replace('return','return '))!=source_hash(base),
            'trailing_newline_differs':source_hash(base+'\n')!=source_hash(base)}

def main(config_path):
    cfg=load_config(config_path)
    corpus=Path(cfg['corpus_root']);root=Path(cfg['validation']).parent/'analyzer'
    rows=[]
    for pid in cfg['problem_ids']:
        for lang in LANGUAGES:
            source=(corpus/pid/f'reference.{EXTENSIONS[lang]}').read_text(encoding='utf-8')
            for variant,(candidate,detail) in variants(source,lang).items():
                m=measure(source,candidate,root/pid/lang/variant,config=cfg['similarity'])
                rows.append({'problem_id':pid,'language':lang,'variant':variant,'detail':detail,
                             'status':m['status'],'value':m['value'],'reason':m['reason'],
                             'chars':len(source),'lines':source.count('\n')+1})
                print(pid,lang,variant,m['status'],m['value'],flush=True)
    summary=defaultdict(dict)
    for lang in LANGUAGES:
        for variant in sorted({r['variant'] for r in rows}):
            sel=[r for r in rows if r['language']==lang and r['variant']==variant]
            vals=[r['value'] for r in sel if r['status']=='measured']
            summary[variant][lang]={'n':len(sel),'measured':len(vals),'na':len(sel)-len(vals),
                                    'mean':mean(vals) if vals else None,'median':median(vals) if vals else None,
                                    'min':min(vals) if vals else None,'max':max(vals) if vals else None}
    spread={v:(max(s['mean'] for s in by.values() if s['mean'] is not None)-min(s['mean'] for s in by.values() if s['mean'] is not None))
            if all(s['mean'] is not None for s in by.values()) else None for v,by in summary.items() if v!='short'}
    identity=state_identity_checks()
    identical_ok=all(r['status']=='measured' and r['value']==1.0 for r in rows if r['variant']=='identical')
    na_real=[r for r in rows if r['variant']!='short' and r['status']!='measured']
    value={'created_at':timestamp(),'config':str(Path(config_path).resolve()),'similarity':cfg['similarity'],
           'state_identity':identity,'identical_is_one':identical_ok,'na_on_real_code':len(na_real),
           'short_is_na':all(r['status']!='measured' for r in rows if r['variant']=='short'),
           'summary':summary,'cross_language_mean_spread':spread,'rows':rows}
    write_json(root/'analyzer_check.json',value)
    print('state identity',identity)
    print('identical == 1.0:',identical_ok,'NA on real code:',len(na_real))
    for variant,by in summary.items():
        print(variant,{l:(round(s['mean'],3) if s['mean'] is not None else None,s['na']) for l,s in by.items()},'spread',spread.get(variant))

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'fps_v2.yaml')
