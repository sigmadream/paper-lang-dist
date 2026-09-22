"""Main-design gate for fps-text-v2 computed from the complete pilot, no translations.

Also seeds the main phase with the pilot attempts (v1/abs_EXPERIMENT.md D4: pilot
included as-is), so the main campaign replays them without new model calls.

Usage: python scripts/freeze_fps_v2_main.py fps_v2.yaml
"""
from collections import Counter
from pathlib import Path
import shutil
import sys

from rttdist.experiment_io import read_json, write_json, timestamp, digest
from rttdist.fps_experiment import load_config

def main(config_path):
    cfg=load_config(config_path);root=Path(cfg['output_root']);pilot=root/'pilot';main_root=root/'main'
    audit=read_json(pilot/'completion_audit.json')
    planned=len(cfg['pilot_problem_ids'])*len(cfg['routes'])*cfg['repeats']
    assert audit['passed'] and audit['observed']==planned
    records=[read_json(p) for p in pilot.glob('*/*/attempt-*/observation.json')]
    replies=[read_json(p) for p in pilot.glob('*/*/attempt-*/step-*/response.json')]
    completion=sum(r['usage']['completion_tokens'] for r in replies);prompt=sum(r['usage']['prompt_tokens'] for r in replies)
    cost=sum(r['cost_usd'] for r in replies)
    scale=len(cfg['problem_ids'])/len(cfg['pilot_problem_ids'])
    projected=cost*scale
    assert projected<=cfg['llm']['cost_cap_usd']
    design={'at':timestamp(),'approved_for_main':True,
            'approval_basis':'User asked to run v1/abs_PLAN.md and v1/abs_EXPERIMENT.md; the registered pilot gate '
                             '(projected main cost <= 30 USD) passed; design kept frozen, reviewed by executing agent',
            'config_sha256':digest(Path(config_path).read_bytes()),'pilot_audit_sha256':digest((pilot/'completion_audit.json').read_bytes()),
            'main_attempts':len(cfg['problem_ids'])*len(cfg['routes'])*cfg['repeats'],'pilot_attempts':planned,
            'pilot_statuses':dict(Counter(r['status'] for r in records)),
            'pilot_primary_categories':dict(Counter(r['category'] for r in records)),
            'pilot_calls':len(replies),'pilot_prompt_tokens':prompt,'pilot_completion_tokens':completion,'pilot_cost_usd':cost,
            'pilot_finish_reasons':dict(Counter(str(r['body']['choices'][0].get('finish_reason')) for r in replies)),
            'main_projected_cost_usd':projected,'cost_cap_usd':cfg['llm']['cost_cap_usd'],
            'parallel_shards':3,
            'decisions':['D1: temperature 0.6, top_p 0.95, N=5, seed 20260919+attempt-1',
                         'D3: reasoning_effort low, max_tokens 16384',
                         'D4: pilot attempts are included as-is (copied into main, replayed without calls); pilot-exclusion sensitivity reported',
                         'Design frozen despite pilot floor effect (3/90 primary successes): extraction rule (multiple fenced blocks = format_error), '
                         'theta .85 and temperature are unchanged; any change is a separate design version',
                         'Main runs as 3 shards of the shuffled schedule, each with cost cap 30/3 USD',
                         'D2: control routes (cpp-via-python, cpp-via-java) run after main as a separate phase config if budget remains']}
    write_json(root/'main_design.json',design)
    main_root.mkdir(parents=True,exist_ok=True)
    for pid in cfg['pilot_problem_ids']:
        target=main_root/pid
        if not target.exists():shutil.copytree(pilot/pid,target)
    print({k:v for k,v in design.items() if k!='decisions'})

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else 'fps_v2.yaml')
