"""Descriptive diagnostics for an fps-text-v2 phase (no model calls, no new metrics).

Separates why attempts stopped: which step and language failed, why code
extraction failed, how often each translation direction produced working code,
and how far adjacent restored similarity was from the thresholds.

Usage: python scripts/diagnose_fps_v2.py fps_v2.yaml main
"""
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
import sys

from rttdist.experiment_io import read_json, write_json, timestamp
from rttdist.fps_experiment import load_config

def main(config_path,phase):
    cfg=load_config(config_path);root=Path(cfg['output_root'])/phase
    records=[read_json(p) for p in sorted(root.glob('*/*/attempt-*/observation.json'))]
    routes=[a+'-via-'+b for a,b in cfg['routes']]
    out={'at':timestamp(),'phase':phase,'attempts':len(records),'routes':{}}
    for route in routes:
        rs=[r for r in records if r['route']==route]
        stop=Counter();where=Counter();extract=Counter();direction=defaultdict(lambda:[0,0])
        sym=[];first_restore=[];max_sym=[]
        for r in rs:
            stop[r['status']]+=1
            last=r['steps'][-1]
            if r['status'] not in ('collection_complete','max_distance_reached','translation_budget_reached'):
                where[('intermediate' if last['language']!=r['seed_language'] else 'restored')+f"@{'1' if last['step']==1 else '2' if last['step']==2 else '3+'}"]+=1
            if r['status']=='format_error':
                step=root/r['problem_id']/route/f"attempt-{r['attempt']:02}"/f"step-{last['step']:02}"/'response.json'
                text=read_json(step)['body']['choices'][0]['message'].get('content') or ''
                extract['multiple_fenced_blocks' if text.count('```')>2 else 'empty' if not text.strip() else 'other']+=1
            for s in r['steps']:
                pair=(r['seed_language'] if s['language']!=r['seed_language'] else r['target_language'])+'->'+s['language']
                direction[pair][1]+=1
                if s.get('evaluation_status')=='success':direction[pair][0]+=1
            values=[s['sym_adj'] for s in r['steps'] if s.get('sym_adj') is not None]
            sym+=values
            if values:first_restore.append(values[0]);max_sym.append(max(values))
        out['routes'][route]={
            'statuses':dict(stop),'functional_failure_at':dict(where),'format_error_causes':dict(extract),
            'step_pass_rate':{k:{'passed':v[0],'steps':v[1],'rate':v[0]/v[1]} for k,v in direction.items()},
            'sym_adj':{'n':len(sym),'mean':mean(sym) if sym else None,'median':median(sym) if sym else None,
                       'share_zero':sum(1 for v in sym if v==0)/len(sym) if sym else None,
                       'share_ge_085':sum(1 for v in sym if v>=.85)/len(sym) if sym else None},
            'first_restore_sym_median':median(first_restore) if first_restore else None,
            'attempts_with_measured_restore':len(max_sym),
            'max_sym_per_attempt_median':median(max_sym) if max_sym else None,
            'successes_from_exact_repeat':sum(1 for r in rs if r['success'] and r['sym_adj']==1.0),
            'successes':sum(1 for r in rs if r['success'])}
    write_json(root/'diagnostics.json',out)
    for route,v in out['routes'].items():
        rate={k:f"{x['passed']}/{x['steps']}" for k,x in v['step_pass_rate'].items()}
        print(route,'| fail at',v['functional_failure_at'],'| extract',v['format_error_causes'],'| pass',rate,
              '| sym median',None if v['sym_adj']['median'] is None else round(v['sym_adj']['median'],3),'zero',
              None if v['sym_adj']['share_zero'] is None else round(v['sym_adj']['share_zero'],2),
              '| success exact repeat',v['successes_from_exact_repeat'],'/',v['successes'])

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
