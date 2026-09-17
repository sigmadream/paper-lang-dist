"""Recheck frozen files, independent oracles, current C++ references and mappings."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess

from build_dataset import BASE, DATA, ROOT, canonical, exclusion, sha
from oracles import solve


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',default=str(ROOT/'.tools/gcc/bin/g++.exe'))
    parser.add_argument('--upstream',default=str(ROOT/'.tools/leetcode-source'))
    args=parser.parse_args()
    manifest_path=BASE/'manifest.json'
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    compiler=str(Path(args.compiler).resolve()); upstream=Path(args.upstream).resolve()
    env=dict(os.environ);env['PATH']=str(Path(compiler).parent)+os.pathsep+env.get('PATH','')
    build=ROOT/'.tools/evaluation-v2-a-build';build.mkdir(exist_ok=True)
    report={'dataset_id':manifest['dataset_id'], 'validated_at_utc':datetime.now(timezone.utc).isoformat(),
      'manifest_sha256':sha(manifest_path), 'python':platform.python_version(), 'compiler_path':compiler,
      'compiler_version':subprocess.check_output([compiler,'--version'],env=env,text=True).splitlines()[0],
      'compile_flags':['-std=c++17','-O2'], 'per_case_timeout_seconds':30,
      'comparison':'whitespace-token equality', 'problems':[], 'errors':[]}
    assert manifest['generator_sha256']==sha(BASE/'tools/build_dataset.py')
    assert manifest['oracle_sha256']==sha(BASE/'tools/oracles.py')
    assert manifest['problem_count']==len(manifest['problems'])==19
    assert len({p['problem_id'] for p in manifest['problems']})==19
    for p in manifest['problems']:
        pid=p['problem_id'].split('_')[1]
        old,_,_=exclusion(pid)
        for src in p['exclusion_sources']:
            assert sha(ROOT/src['path'])==src['sha256'], f'Exclusion source changed: {src}'
        reference=DATA/p['problem_id']/'reference.cpp'
        exe=build/(p['problem_id']+('.exe' if os.name=='nt' else ''))
        result={'problem_id':p['problem_id'],'reference_path':reference.relative_to(ROOT).as_posix(),
                'reference_sha256':sha(reference),'cases':[]}
        compile_run=subprocess.run([compiler,'-std=c++17','-O2',str(reference),'-o',str(exe)],
                                   capture_output=True,text=True,env=env,timeout=30)
        result['compile_status']='pass' if compile_run.returncode==0 else 'fail'
        if compile_run.returncode:
            result['compile_stderr']=compile_run.stderr
            report['errors'].append(p['problem_id']+': compile failure')
        seen=set()
        for c in p['cases']:
            ip=BASE/c['input'];op=BASE/c['output']
            assert ip.parent.resolve()==DATA/p['problem_id']/'evaluation' and op.parent==ip.parent
            assert sha(ip)==c['input_sha256'] and sha(op)==c['output_sha256']
            inp=ip.read_text(encoding='utf-8');expected=op.read_text(encoding='utf-8');key=canonical(inp)
            assert key not in old and key not in seen
            assert hashlib.sha256(key.encode()).hexdigest()==c['canonical_input_sha256']
            seen.add(key)
            a,b=solve(pid,inp)
            assert canonical(a)==canonical(b)==canonical(expected), (pid,c['case_id'],'oracle mismatch')
            rec={'case_id':c['case_id'],'input_constraints':'pass','distinct_from_examples_and_old_fixtures':True,
                 'oracle_cross_check':'pass', 'reference_status':'not_run'}
            if compile_run.returncode==0:
                try:
                    run=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,env=env,timeout=30,cwd=build)
                    rec['reference_exit_code']=run.returncode
                    rec['reference_stdout_sha256']=hashlib.sha256(run.stdout.encode()).hexdigest()
                    rec['reference_status']='pass' if run.returncode==0 and canonical(run.stdout)==canonical(expected) else 'fail'
                    if rec['reference_status']=='fail':
                        rec['stderr']=run.stderr;report['errors'].append(f'{pid}/{c["case_id"]}: reference mismatch')
                except subprocess.TimeoutExpired:
                    rec['reference_status']='timeout';report['errors'].append(f'{pid}/{c["case_id"]}: timeout')
            result['cases'].append(rec)
        result['unique_inputs']=len(seen)
        assert len(seen)==len(p['cases']) and len(seen)>=10
        report['problems'].append(result)
        print(f'{p["problem_id"]}: {sum(c["reference_status"]=="pass" for c in result["cases"])}/{len(seen)} reference checks',flush=True)
    upstream_run=subprocess.run([shutil.which('node') or 'node',str(BASE/'tools/check_upstream.cjs'),str(upstream)],
                                capture_output=True,text=True,timeout=60)
    if upstream_run.returncode:
        report['errors'].append('Upstream adapter failed: '+upstream_run.stderr)
    else:
        report['upstream_checks']=json.loads(upstream_run.stdout)
        if any(c['status']!='pass' for c in report['upstream_checks']['cases']):report['errors'].append('Upstream mismatch')
    report['problem_count']=len(report['problems'])
    report['case_count']=sum(len(p['cases']) for p in report['problems'])
    assert report['case_count']==manifest['case_count']==190
    report['all_passed']=not report['errors'] and all(c['reference_status']=='pass' for p in report['problems'] for c in p['cases'])
    report['validator_sha256']=sha(Path(__file__))
    report['upstream_adapter_sha256']=sha(BASE/'tools/check_upstream.cjs')
    (BASE/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:report[k] for k in ('problem_count','case_count','all_passed','errors')}))
    raise SystemExit(0 if report['all_passed'] else 1)


if __name__=='__main__':main()
