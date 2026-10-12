"""Validate all generated cases and C++ programs, plus the original JS solutions."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess

from build_dataset import BASE,DATA,ROOT,sha,canonical,save_json,relative
from catalog import decode,output
from oracles import solve


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',default=str(ROOT/'.tools/gcc/bin/g++.exe'))
    parser.add_argument('--upstream',default=str(ROOT/'.tools/leetcode-source'))
    args=parser.parse_args();compiler=str(Path(args.compiler).resolve())
    manifest=json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
    for name,digest in manifest['tool_hashes'].items():assert sha(BASE/name)==digest, f'Tool changed: {name}'
    env=dict(os.environ);env['PATH']=str(Path(compiler).parent)+os.pathsep+env.get('PATH','')
    build=ROOT/'.tools/leetcode-21-build';build.mkdir(exist_ok=True)
    report={'dataset_id':manifest['dataset_id'],'validated_at_utc':datetime.now(timezone.utc).isoformat(),
      'manifest_sha256':sha(BASE/'manifest.json'),'python_version':platform.python_version(),
      'compiler_version':subprocess.check_output([compiler,'--version'],text=True,env=env).splitlines()[0],
      'flags':['-std=c++17','-O2'],'timeout_seconds':30,'problems':[],'errors':[]}
    requests=[]
    assert len(manifest['problems'])==manifest['problem_count']==21
    for p in manifest['problems']:
        pid=p['id'];folder=DATA/p['problem_id']
        for name,digest in p['frozen_files'].items():assert sha(BASE/name)==digest,(name,'file changed')
        exe=build/(p['problem_id']+('.exe' if os.name=='nt' else ''))
        compiled=subprocess.run([compiler,'-std=c++17','-O2',str(folder/'reference.cpp'),'-o',str(exe)],env=env,capture_output=True,text=True,timeout=30)
        assert compiled.returncode==0,compiled.stderr
        rec={'problem_id':p['problem_id'],'reference_sha256':sha(folder/'reference.cpp'),'compile_status':'pass','cases':[]}
        excluded={canonical(pid,e['args']) for e in p['excluded_public_examples']};seen=set()
        tasks=[{'case_id':'prompt_example01','input':relative(folder/'prompt_examples/example01.inp'),'output':relative(folder/'prompt_examples/example01.out')}]+p['cases']
        for c in tasks:
            ip=BASE/c['input'];op=BASE/c['output'];inp=ip.read_text(encoding='utf-8');expected=op.read_text(encoding='utf-8')
            decoded=decode(pid,inp);key=canonical(pid,decoded)
            evaluation=c['case_id']!='prompt_example01'
            if evaluation:
                assert sha(ip)==c['input_sha256'] and sha(op)==c['output_sha256']
                assert hashlib.sha256(key.encode()).hexdigest()==c['canonical_args_sha256']
                assert key not in excluded and key not in seen;seen.add(key)
            a,b=solve(pid,decoded);assert a==b and output(a).split()==expected.split()
            run=subprocess.run([str(exe)],input=inp,text=True,capture_output=True,timeout=30,env=env,cwd=build)
            status='pass' if run.returncode==0 and run.stdout.split()==expected.split() else 'fail'
            row={'case_id':c['case_id'],'scope':'evaluation' if evaluation else 'prompt','input_constraints':'pass',
                 'oracle_cross_check':'pass','cpp_status':status,'exit_code':run.returncode,
                 'stdout_sha256':hashlib.sha256(run.stdout.encode()).hexdigest()}
            if status!='pass':report['errors'].append(f'{p["problem_id"]}/{c["case_id"]}: C++ mismatch');row['stderr']=run.stderr
            rec['cases'].append(row)
            requests.append({'id':pid,'case_id':c['case_id'],'args':decoded,'expected':a})
        assert len(seen)==13
        report['problems'].append(rec)
        print(f'{p["problem_id"]}: {sum(c["cpp_status"]=="pass" for c in rec["cases"])} / 14 C++ checks',flush=True)
    js=subprocess.run([shutil.which('node') or 'node',str(BASE/'tools/check_upstream.cjs'),args.upstream],input=json.dumps(requests),capture_output=True,text=True,timeout=60)
    assert js.returncode==0,js.stderr
    report['upstream']=json.loads(js.stdout)
    rows=[c for p in report['problems'] for c in p['cases'] if c['scope']=='evaluation']
    report['evaluation_case_count']=len(rows)
    report['cpp_evaluation_pass_count']=sum(c['cpp_status']=='pass' for c in rows)
    report['oracle_evaluation_pass_count']=sum(c['oracle_cross_check']=='pass' for c in rows)
    report['upstream_evaluation_pass_count']=sum(c['status']=='pass' for c in report['upstream']['results'] if c['case_id']!='prompt_example01')
    report['upstream_failures']=[c for c in report['upstream']['results'] if c['status']!='pass']
    report['dataset_validation_passed']=not report['errors'] and len(rows)==273
    report['note']='Upstream mismatches are retained and do not redefine the independently verified expected outputs.'
    save_json(BASE/'validation_report.json',report)
    print(json.dumps({k:report[k] for k in ('evaluation_case_count','cpp_evaluation_pass_count','upstream_evaluation_pass_count','dataset_validation_passed','upstream_failures')},ensure_ascii=True))
    raise SystemExit(0 if report['dataset_validation_passed'] else 1)


if __name__=='__main__':main()
