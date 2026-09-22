import io
import json
from pathlib import Path
import yaml
from rttdist.config import load_experiment_config
from rttdist.translation_factory import create_translation_client

def test_common_config_and_general_client_use_provider_without_lmstudio_block(tmp_path,monkeypatch):
    config={'provider':'openai_compatible','problem_ids':['p'],'seed_language':'haskell',
            'target_languages':['prolog'],'output_root':str(tmp_path/'output'),
            'runtime':{'max_iterations':2,'timeout_seconds':5},
            'llm':{'model':'test','endpoint':'http://localhost:9999/v1','generation':{'temperature':0},'retries':0}}
    path=tmp_path/'config.yaml';path.write_text(yaml.safe_dump(config))
    cfg=load_experiment_config(path)
    received=[]
    def send(req,timeout):
        received.append(json.loads(req.data))
        return io.BytesIO(json.dumps({'id':'id','model':'test','choices':[{'index':0,
            'message':{'role':'assistant','content':'```prolog\nmain :- writeln(1).\n```'},'finish_reason':'stop'}]}).encode())
    monkeypatch.setattr('rttdist.providers.request.urlopen',send)
    result=create_translation_client(cfg).translate(problem_id='p',source_language='haskell',target_language='prolog',
        problem_statement='Print one.',sample_input='1',sample_output='1',source_code='main = print 1',iteration_index=1)
    assert len(received)==1 and received[0]['model']=='test'
    assert result.request.metadata['provider']=='openai_compatible'
    assert result.response.usage.prompt_tokens is None
    assert list((tmp_path/'output/provider_requests').glob('*/response.json'))
