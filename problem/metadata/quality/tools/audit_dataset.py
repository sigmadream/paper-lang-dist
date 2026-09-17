"""Reproducible shape, prompt, public-example and diagnostic mutation audit."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from time import perf_counter

from mutants import PANEL

DATA=Path(__file__).resolve().parents[3]
ROOT=DATA.parent
sys.path.insert(0,str(ROOT/'src'))
from rttdist.config import load_experiment_config
from rttdist.corpus import validate_corpus
from rttdist.prompts import build_translation_prompt

# Structure-based strata, not official ratings or measured model difficulty.
STRATA = {
 'linear_or_ordered': ['IPOP_10988','IPOP_18870','IPOP_1929','IPOP_2217','IPOP_2609','LC_0121','LC_0217','LC_0704','LC_0035','LC_0283','LC_0242','LC_0387','LC_0338','LC_0912'],
 'stateful': ['IPOP_1158','IPOP_1436','IPOP_14719','IPOP_1620','IPOP_2003','IPOP_2110','IPOP_2579','IPOP_5567','IPOP_9012','IPOP_9251','IPOP_9935','LC_0001','LC_0053','LC_0003','LC_0139','LC_0518','LC_0062','LC_0063','LC_0064','LC_0739','LC_0496','LC_0547','LC_0207'],
 'recursive_or_combinatorial': ['IPOP_11729','IPOP_1992','IPOP_9663'],
}
FAMILIES = {
 'binary_search': ['IPOP_2110','LC_0704','LC_0035'],
 'grid_dp': ['LC_0062','LC_0063','LC_0064'],
 'monotonic_stack': ['LC_0739','LC_0496'],
 'string_frequency': ['LC_0242','LC_0387'],
 'sliding_window': ['IPOP_2003','LC_0003'],
 'graph_reachability': ['IPOP_5567','LC_0547'],
}


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def normalized(text):return text.split()
def save_json(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',default=str(ROOT/'.tools/gcc/bin/g++.exe'))
    args=parser.parse_args()
    config=load_experiment_config(ROOT/'lmstudio_v2.yaml');entries=validate_corpus(config)
    output=DATA/'metadata/quality';previews=output/'prompt_previews';previews.mkdir(exist_ok=True)
    baseline=DATA/'archive/v2-a-before-quality'
    build=ROOT/'.tools/quality-build';build.mkdir(exist_ok=True)
    compiler=str(Path(args.compiler).resolve());env=dict(os.environ);env['PATH']=str(Path(compiler).parent)+os.pathsep+env.get('PATH','')
    rows=[];errors=[];pair_total=0;prompt_total=0
    baseline_inputs_preserved=True;seeds_preserved=True;first_samples_preserved=True
    for e in entries:
        pid=e.problem_id;directory=DATA/pid;old=baseline/pid
        statement=e.statement_path.read_text(encoding='utf-8');sample=e.prompt_sample
        baseline_inputs_preserved &= all((directory/'evaluation'/p.name).read_bytes()==p.read_bytes() for p in (old/'evaluation').glob('*') if p.suffix in ('.inp','.out'))
        seeds_preserved &= sha(e.seed_path)==sha(old/'reference.cpp')
        first_samples_preserved &= all((old/'prompt_examples'/p.name).read_bytes()==p.read_bytes() for p in (sample.input_path,sample.output_path))
        prompts=[]
        for target in config.target_languages:
            bundle=build_translation_prompt(problem_id=pid,source_language='cpp',target_language=target,
                problem_statement=statement,sample_input=sample.input_path.read_text(encoding='utf-8'),
                sample_output=sample.output_path.read_text(encoding='utf-8'),source_code=e.seed_path.read_text(encoding='utf-8'),
                direction='seed_to_target',template_version=config.prompt_template_version)
            messages=[m.to_dict() for m in bundle.messages]
            prompts.append({'target':target,'messages':messages,'sha256':hashlib.sha256(json.dumps(messages,ensure_ascii=False,sort_keys=True).encode()).hexdigest()})
        save_json(previews/f'{pid}.json',{'problem_id':pid,'template':config.prompt_template_version,'scope':'initial forward prompts; reverse source depends on model output','prompts':prompts})
        exe=build/(pid+'.exe' if os.name=='nt' else pid)
        compiled=subprocess.run([compiler,'-std=c++17','-O2',str(e.seed_path),'-o',str(exe)],capture_output=True,text=True,timeout=30,env=env)
        assert compiled.returncode==0,compiled.stderr
        checks=[];unique={}
        for pair in e.prompt_examples:
            input_bytes=pair.input_path.read_bytes();expected=pair.output_path.read_text(encoding='utf-8')
            key=(input_bytes,tuple(expected.split()))
            if key not in unique:
                start=perf_counter()
                run=subprocess.run([str(exe)],input=input_bytes,capture_output=True,timeout=30,env=env)
                ok=run.returncode==0 and run.stdout.decode('utf-8').split()==expected.split()
                unique[key]={'passed':ok,'elapsed_seconds':round(perf_counter()-start,6)}
            row={'case':pair.input_path.stem,**unique[key]};checks.append(row)
            if not row['passed']:errors.append(f'{pid}/prompt/{row["case"]}')
        strata=next(k for k,v in STRATA.items() if pid in v)
        family=next((k for k,v in FAMILIES.items() if pid in v),pid)
        inputs=[p.input_path.read_text(encoding='utf-8') for p in e.fixture_pairs]
        keys=[value.removesuffix('\n') if pid=='LC_0003' else tuple(value.split()) for value in inputs]
        assert len(keys)==len(set(keys)),pid
        row={'problem_id':pid,'algorithm_structure':strata,'family':family,
            'evaluation_cases':len(e.fixture_pairs),'unique_evaluation_inputs':len(set(keys)),
            'max_input_bytes':max(p.input_path.stat().st_size for p in e.fixture_pairs),
            'baseline_max_input_bytes':max(p.stat().st_size for p in (old/'evaluation').glob('*.inp')),
            'statement_characters':len(statement),'baseline_statement_characters':len((old/'statement.md').read_text(encoding='utf-8')),
            'prompt_pairs_stored':len(checks),'prompt_pairs_unique':len(unique),'prompt_checks':checks,
            'first_prompt_characters':sum(len(m['content']) for m in prompts[0]['messages']),
            'source_sha256':sha(e.seed_path),'statement_sha256':sha(e.statement_path)}
        rows.append(row);pair_total+=len(e.fixture_pairs);prompt_total+=len(checks)
        print(f'{pid}: {len(e.fixture_pairs)} evaluation inputs; {len(checks)} public examples checked',flush=True)
    mutants=[]
    for pid,name,mutant in PANEL:
        outcomes={}
        for scope,folder in [('before',baseline/pid/'evaluation'),('after',DATA/pid/'evaluation')]:
            detected=[]
            for inp in sorted(folder.glob('*.inp')):
                expected=inp.with_suffix('.out').read_text(encoding='utf-8')
                actual=mutant(inp.read_text(encoding='utf-8'))
                if normalized(actual)!=normalized(expected):detected.append(inp.stem)
            outcomes[scope]={'detected':bool(detected),'cases':detected}
        mutants.append({'problem_id':pid,'fault':name,**outcomes})
    assert baseline_inputs_preserved and seeds_preserved and first_samples_preserved
    report={'corpus_version':'v2-a-quality-1','problem_count':len(rows),'evaluation_pairs':pair_total,
        'prompt_pairs_checked':prompt_total,'all_prompt_pairs_passed':not errors,'errors':errors,
        'original_400_pairs_byte_preserved':baseline_inputs_preserved,'reference_sources_byte_preserved':seeds_preserved,
        'first_prompt_samples_byte_preserved':first_samples_preserved,'algorithm_structure_counts':dict(Counter(r['algorithm_structure'] for r in rows)),
        'family_count':len({r['family'] for r in rows}),'classification_policy':'Author-defined structure rubric; not official difficulty or empirical model success.',
        'compiler':subprocess.check_output([compiler,'--version'],text=True,env=env).splitlines()[0],
        'prompt_template':config.prompt_template_version,'problem_rows':rows,'diagnostic_mutants':mutants,
        'mutants_detected_before':sum(m['before']['detected'] for m in mutants),
        'mutants_detected_after':sum(m['after']['detected'] for m in mutants),
        'mutation_scope':'Eight purposively chosen implementation faults; no general mutation score or held-out model accuracy claim.',
        'input_generation_seed':20260917,
        'source_references':['https://arxiv.org/abs/2305.01210','https://oeis.org/A000170/b000170.txt'],
        'audit_code_hashes':{p.name:sha(p) for p in Path(__file__).parent.glob('*.py')},
        'config_sha256':sha(ROOT/'lmstudio_v2.yaml'),'dataset_index_sha256':sha(DATA/'dataset-index.json'),
        'prompt_module_sha256':sha(ROOT/'src/rttdist/prompts.py')}
    save_json(output/'audit_report.json',report)
    columns=[k for k in rows[0] if k!='prompt_checks']
    with (output/'problem_profile.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=columns,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
    print(json.dumps({k:report[k] for k in ('problem_count','evaluation_pairs','prompt_pairs_checked','all_prompt_pairs_passed','mutants_detected_before','mutants_detected_after')}))
    raise SystemExit(1 if errors else 0)


if __name__=='__main__':main()
