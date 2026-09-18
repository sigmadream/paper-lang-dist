"""Reviewable main-design gate computed from the complete pilot, no translations."""
from collections import Counter
from pathlib import Path
from rttdist.experiment_io import read_json, write_json, timestamp, digest
from rttdist.fps_experiment import load_config

def main():
    cfg=load_config('fps_v1.yaml');root=Path(cfg['output_root']);pilot=root/'pilot'
    audit=read_json(pilot/'completion_audit.json')
    assert audit['passed'] and audit['observed']==18
    records=read_json(pilot/'observations.json')
    replies=[read_json(p) for p in pilot.glob('*/*/step-*/response.json')]
    tokens=[r['usage'].get('completion_tokens') if r['usage'] else None for r in replies]
    prompt_tokens=[r['usage'].get('prompt_tokens') if r['usage'] else None for r in replies]
    latency=[r['latency_seconds'] for r in replies]
    measurements=[read_json(p) for p in pilot.glob('*/*/step-*/sym_*/measurement.json')]
    assert all(m['status']=='measured' for m in measurements)
    design={'at':timestamp(),'approved_for_main':True,'approval_basis':'User-authorized experiment; pilot reviewed by executing agent',
            'config_sha256':digest(Path('fps_v1.yaml').read_bytes()),'pilot_audit_sha256':digest((pilot/'completion_audit.json').read_bytes()),
            'main_observations':90,'pilot_observations':18,'models':1,'repeats':1,
            'pilot_statuses':dict(Counter(r['status'] for r in records)),
            'pilot_logical_calls':len(replies),'pilot_completion_tokens':sum(tokens) if all(t is not None for t in tokens) else None,
            'pilot_prompt_tokens':sum(prompt_tokens) if all(t is not None for t in prompt_tokens) else None,
            'pilot_api_seconds':sum(latency) if all(t is not None for t in latency) else None,
            'pilot_similarity_measurements':len(measurements),'pilot_similarity_measured':len(measurements),
            'main_max_logical_calls':1800,'main_max_http_attempts':5400,
            'main_completion_token_cap':1800*cfg['llm']['generation']['max_tokens'],
            'main_projected_calls_at_pilot_rate':len(replies)*5,
            'main_projected_output_tokens_at_pilot_rate':sum(tokens)*5 if all(t is not None for t in tokens) else None,
            'main_projected_api_seconds_at_pilot_rate':sum(latency)*5 if all(t is not None for t in latency) else None,
            'local_api_charge':0,'electricity_cost':None,
            'stop_rules':'First generated-code failure; FPS >10; 20 one-way steps; request 300s; observation wall 4h; no retries of code failures',
            'decisions':['Keep all 15 prospectively selected problems and unchanged prompts despite pilot code failures',
                         'Retain theta=.85 as operational text-stability threshold, not semantic equivalence',
                         'No threshold sensitivity registered; do not infer unobserved .90 results',
                         'R=1; no between-run variance claim; Wilson plus problem bootstrap, paired family-wise Bonferroni intervals',
                         'Main results exclude pilot observations; separately exclude three pilot-used problems in sensitivity analysis'],
            'case_selection':'For success, generated-code failure, distance-limit: lexicographically first problem/route; disclose when absent'}
    write_json(root/'main_design.json',design)
    print(design)

if __name__=='__main__':main()
