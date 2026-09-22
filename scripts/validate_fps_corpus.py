"""Execute and fingerprint every reference solution before translation (stage 0 gate).

Usage: python scripts/validate_fps_corpus.py fps_v2.yaml
The runtime block of the config is used as-is, so the validation record matches
what freeze() later compares against.
"""
from pathlib import Path
import sys

from rttdist.experiment_io import digest, write_json, timestamp
from rttdist.fps_execution import evaluate, EXTENSIONS, process
from rttdist.fps_experiment import load_config

ROOT=Path(__file__).resolve().parents[1]

def main(config_path):
    cfg=load_config(config_path)
    corpus=Path(cfg['corpus_root']);artifact=Path(cfg['validation']).parent
    runtime=cfg['runtime']
    versions={lang:process([p,'--version'],ROOT,30) for lang,p in runtime['tools'].items()}
    results=[]
    for pid in cfg['problem_ids']:
        expected=len(list((corpus/pid/'evaluation').glob('*.inp')))
        for lang,ext in EXTENSIONS.items():
            reference=corpus/pid/f'reference.{ext}'
            if not reference.exists():continue
            value=evaluate(reference.read_text(encoding='utf-8'),lang,corpus/pid,artifact/pid/lang,runtime)
            results.append({'problem_id':pid,'language':lang,'status':value['status'],
                            'case_count':len(value['cases']),'expected_cases':expected})
            print(pid,lang,value['status'],flush=True)
    hashes={str(p.relative_to(corpus)):digest(p.read_bytes()) for p in sorted(corpus.rglob('*')) if p.is_file()}
    languages={lang for lang,ext in EXTENSIONS.items() if any((corpus/pid/f'reference.{ext}').exists() for pid in cfg['problem_ids'])}
    expected_count=len(cfg['problem_ids'])*len(languages)
    value={'created_at':timestamp(),'config':str(Path(config_path).resolve()),'runtime':runtime,'tool_versions':versions,
           'results':results,'file_hashes':hashes,'reference_languages':sorted(languages),
           'passed':len(results)==expected_count and all(r['status']=='success' and r['case_count']==r['expected_cases']>=10 for r in results)}
    write_json(artifact/'validation.json',value)
    print('validation:',artifact/'validation.json','passed' if value['passed'] else 'FAILED')
    if not value['passed']: raise SystemExit('Reference gate failed; do not translate')

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'fps_v2.yaml')
