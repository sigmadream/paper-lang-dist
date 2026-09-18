"""Execute and fingerprint all 45 references before translation."""
from pathlib import Path
import json
import shutil

from rttdist.experiment_io import digest, read_json, write_json, timestamp
from rttdist.fps_execution import evaluate, EXTENSIONS, process

ROOT=Path(__file__).resolve().parents[1]

def main():
    corpus=ROOT/'data/fps-v1'
    artifact=ROOT/'artifacts-lmstudio/fps-v1/preflight-authorized'
    runtime={'tools':{'cpp':str(ROOT/'.tools/mingw64/bin/g++.exe'),
                       'haskell':shutil.which('ghc'), 'prolog':shutil.which('swipl')},
             'compile_timeout':90, 'fixture_timeout':30}
    versions={lang:process([p,'--version'],ROOT,30) for lang,p in runtime['tools'].items()}
    selection=read_json(corpus/'selection.json')
    results=[]
    for item in selection['problems']:
        pid=item['problem_id']
        for lang,ext in EXTENSIONS.items():
            source=(corpus/pid/f'reference.{ext}').read_text(encoding='utf-8')
            value=evaluate(source,lang,corpus/pid,artifact/pid/lang,runtime)
            results.append({'problem_id':pid,'language':lang,'status':value['status'],
                            'case_count':len(value['cases'])})
            print(pid,lang,value['status'],flush=True)
    hashes={str(p.relative_to(corpus)):digest(p.read_bytes()) for p in sorted(corpus.rglob('*')) if p.is_file()}
    value={'created_at':timestamp(),'runtime':runtime,'tool_versions':versions,'results':results,
           'file_hashes':hashes, 'passed':len(results)==45 and all(r['status']=='success' and r['case_count']==13 for r in results)}
    write_json(artifact/'validation.json',value)
    if not value['passed']: raise SystemExit('Reference gate failed; do not translate')

if __name__=='__main__':main()
