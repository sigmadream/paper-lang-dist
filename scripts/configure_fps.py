"""Write the prospective single-model campaign configuration after reference checks."""
from pathlib import Path
import yaml
from rttdist.experiment_io import read_json
from calibrate_fps_similarity import config as similarity_config

ROOT=Path(__file__).resolve().parents[1]

def main():
    validation=read_json(ROOT/'artifacts-lmstudio/fps-v1/preflight-authorized/validation.json')
    assert validation['passed']
    selection=read_json(ROOT/'data/fps-v1/selection.json')
    config={'experiment_version':'fps-text-v1','repeats':1,
            'problem_ids':[p['problem_id'] for p in selection['problems']],
            'pilot_problem_ids':selection['pilot_problem_ids'],
            'corpus_root':'data/fps-v1','output_root':'artifacts-lmstudio/fps-v1',
            'validation':'artifacts-lmstudio/fps-v1/preflight-authorized/validation.json',
            'llm':{'provider':'lmstudio','endpoint':'http://localhost:1234/v1',
                   'model':'qwen2.5-coder-7b-instruct','api_key_env':None,
                   'generation':{'temperature':0,'top_p':1,'max_tokens':4096,'seed':20260918},
                   'request_timeout':300,'retries':2},
            'threshold':.85,'max_fps_size':10,'max_translation_steps':20,
            'state_identity':'language + SHA256(extracted source, CRLF/CR to LF only)',
            'similarity':similarity_config(),'runtime':validation['runtime'],
            'observation_wall_seconds':14400,'schedule_seed':20260918,
            'analysis':{'bootstrap_replicates':2000,'bootstrap_seed':20260918,
                        'comparisons':'three reverse-direction pairs; Bonferroni family of 3 for each metric',
                        'pilot_exclusion_sensitivity':True,
                        'threshold_sensitivity':'not registered; cannot infer unobserved high-threshold trajectories'},
            'scope_amendment':'2026-09-18 user requested LM Studio only; second model and live external-provider comparison deferred'}
    (ROOT/'fps_v1.yaml').write_text(yaml.safe_dump(config,sort_keys=False,allow_unicode=True),encoding='utf-8')
    print('fps_v1.yaml written; N=15, M=1, R=1; pilot 18, main 90; maximum logical translations 2160')

if __name__=='__main__':main()
