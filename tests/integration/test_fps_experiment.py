import json
from pathlib import Path
import pytest
import yaml
from rttdist import fps_experiment as fps
from rttdist.experiment_io import write_json
from rttdist.providers import CostCapReached

class ReplayProvider:
    cost_cap=None;total_cost=0.0;cap_reached=False
    def __init__(self, outputs, model='test'): self.outputs=iter(outputs);self.calls=0;self.model=model
    def complete(self,payload,folder):
        p=Path(folder)/'response.json'
        if p.exists():return json.loads(p.read_text())
        self.calls+=1
        response={'body':{'choices':[{'message':{'content':next(self.outputs)},'finish_reason':'stop'}]},
                  'actual_model':self.model,'usage':{'prompt_tokens':10,'completion_tokens':5},'latency_seconds':.1,'cost_usd':.001}
        write_json(p,response)
        return response

@pytest.fixture
def setup(tmp_path,monkeypatch):
    problem=tmp_path/'corpus'/'p';problem.mkdir(parents=True)
    (problem/'reference.cpp').write_text('A')
    (problem/'statement.md').write_text('Problem')
    monkeypatch.setattr(fps,'evaluate',lambda *args:{'status':'success'})
    monkeypatch.setattr(fps,'measure',lambda *args,**kw:{'status':'measured','value':.9})
    cfg={'corpus_root':str(tmp_path/'corpus'),'threshold':.85,'thresholds':[.85],'max_fps_size':10,'max_translation_steps':20,
         'llm':{'model':'test','generation':{'seed':7}},'runtime':{},'similarity':{},'observation_wall_seconds':30}
    folder=tmp_path/'observation';folder.mkdir()
    return cfg,folder

def test_replay_and_conditional_distance(setup):
    cfg,folder=setup;p=ReplayProvider(['B','A1'])
    first=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    second=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert first['status']==second['status']=='collection_complete'
    assert first['success'] and first['category']=='success' and first['d_n']==second['d_n']==3
    assert first['states']==second['states'] and first['seed']==7 and first['attempt']==1
    assert first['reached_step']==2 and first['sym_adj']==.9 and first['cost_usd']==pytest.approx(.002)
    assert p.calls==2

def test_attempt_seed_offsets_and_separate_folders(setup,tmp_path):
    cfg,folder=setup;p=ReplayProvider(['B','A1','B','A1'])
    one=fps.run_observation(cfg,'p','cpp','prolog',folder/'attempt-01',p,attempt=1)
    two=fps.run_observation(cfg,'p','cpp','prolog',folder/'attempt-02',p,attempt=2)
    assert one['seed']==7 and two['seed']==8 and two['attempt']==2 and p.calls==4
    request=json.loads((folder/'attempt-02'/'step-01'/'response.json').read_text())
    assert request  # both attempts persisted their own steps
    assert fps.attempt_generation({'llm':{'generation':{'temperature':0}}},3)=={'temperature':0}

def test_intermediate_failure_stops_and_has_no_distance(setup,monkeypatch):
    cfg,folder=setup;p=ReplayProvider(['bad'])
    monkeypatch.setattr(fps,'evaluate',lambda *args:{'status':'compile_error'})
    r=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert p.calls==1 and r['evaluable'] and not r['functional']
    assert r['category']=='functional_failure' and r['d_n'] is None and r['fps_size_at_stop']==2

def test_origin_score_does_not_stop_and_intermediate_limit_has_no_return(setup,monkeypatch):
    cfg,folder=setup
    # First restored source duplicates x0, so the tenth new state arrives on an odd step.
    p=ReplayProvider(['B1','A','B2','A2','B3','A3','B4','A4','B5','A5','B6'])
    monkeypatch.setattr(fps,'measure',lambda a,b,folder,**kw:{'status':'measured','value':1 if folder.name=='sym_origin' else .1})
    r=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert r['status']=='max_distance_reached' and r['category']=='fps_limit' and r['fps_size_at_stop']==11
    assert p.calls==11 and r['steps'][-1]['language']=='prolog'
    assert r['functional'] and not r['success'] and r['d_n'] is None and r['duplicate_steps']==1

def test_unavailable_similarity_continues_and_unjudged_attempt_is_invalid(setup,monkeypatch):
    cfg,folder=setup;cfg['max_translation_steps']=4;p=ReplayProvider(['B','A1','B','A1'])
    monkeypatch.setattr(fps,'measure',lambda *args,**kw:{'status':'unavailable','value':None})
    r=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert p.calls==4 and r['status']=='translation_budget_reached'
    assert r['category']=='invalid' and not r['evaluable'] and r['reason']=='similarity_unavailable'
    assert r['similarity_unavailable_steps']==2 and r['d_n'] is None

def test_multi_threshold_primary_fixed_before_later_failure(setup,monkeypatch):
    cfg,folder=setup;cfg['thresholds']=[.8,.85,.9]
    p=ReplayProvider(['B','A1','B2','bad'])
    monkeypatch.setattr(fps,'evaluate',lambda source,*args:{'status':'compile_error' if source=='bad' else 'success'})
    monkeypatch.setattr(fps,'measure',lambda a,b,folder,**kw:{'status':'measured','value':.86})
    r=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert p.calls==4 and r['status']=='compile_error' and r['functional'] is False
    assert r['success'] and r['d_n']==3 and r['category']=='success' and r['reached_step']==2
    assert r['outcomes']['0.80']['success'] and r['outcomes']['0.90']['category']=='functional_failure'
    assert r['steps'][1]['thresholds_reached']==['0.80','0.85']

def test_largest_threshold_ends_collection(setup,monkeypatch):
    cfg,folder=setup;cfg['thresholds']=[.8,.85,.9]
    p=ReplayProvider(['B','A1','B2','A2'])
    values=iter([.86,.95])
    monkeypatch.setattr(fps,'measure',lambda a,b,folder,**kw:{'status':'measured','value':next(values) if folder.name=='sym_adj' else .5})
    r=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert p.calls==4 and r['status']=='collection_complete' and r['d_n']==3
    assert r['outcomes']['0.90']['d_n']==5 and r['outcomes']['0.90']['reached_step']==4

def test_unexpected_model_and_cost_cap_are_invalid(setup):
    cfg,folder=setup
    r=fps.run_observation(cfg,'p','cpp','prolog',folder/'m',ReplayProvider(['B'],model='other'))
    assert r['status']=='infrastructure_error' and r['reason']=='unexpected_response_model' and r['category']=='invalid'
    cfg['llm']['expected_model']='oth'
    r=fps.run_observation(cfg,'p','cpp','prolog',folder/'m2',ReplayProvider(['B','A1'],model='other'))
    assert r['success']
    class Capped(ReplayProvider):
        def complete(self,payload,folder):raise CostCapReached('cap')
    r=fps.run_observation(cfg,'p','cpp','prolog',folder/'c',Capped([]))
    assert r['reason']=='cost_cap_reached' and not r['evaluable'] and r['translation_steps']==0

def test_load_config_routes_thresholds_and_repeats(tmp_path):
    cfg={'experiment_version':'fps-text-v2','repeats':5,'problem_ids':[f'p{i}' for i in range(10)],'pilot_problem_ids':['p1'],
         'threshold':.85,'thresholds':[.9,.8,.85],'max_fps_size':10,'max_translation_steps':20,
         'corpus_root':'.','output_root':'out','validation':'v.json','routes':['cpp-via-python',['cpp','haskell']],
         'runtime':{'tools':{'cpp':'g++','python':'python','haskell':'ghc'}},
         'llm':{'provider':'openai_compatible','endpoint':'http://localhost:1/v1','model':'test','generation':{},'retries':0,'request_timeout':1,'api_key_env':None}}
    path=tmp_path/'c.yaml';path.write_text(yaml.safe_dump(cfg))
    loaded=fps.load_config(path)
    assert loaded['routes']==[['cpp','python'],['cpp','haskell']] and loaded['thresholds']==[.8,.85,.9]
    cfg['routes']=['cpp-via-java'];path.write_text(yaml.safe_dump(cfg))
    with pytest.raises(ValueError,match='runtime tools'):fps.load_config(path)
    cfg['routes']=None;cfg['repeats']=0;path.write_text(yaml.safe_dump(cfg))
    with pytest.raises(ValueError,match='repeats'):fps.load_config(path)
    cfg['repeats']=1;cfg['runtime']['tools']['prolog']='swipl';path.write_text(yaml.safe_dump(cfg))
    assert len(fps.load_config(path)['routes'])==6

def test_shards_partition_the_shuffled_schedule(monkeypatch,tmp_path):
    cfg={'pilot_problem_ids':['p','q'],'problem_ids':['p','q'],'routes':[['cpp','haskell'],['haskell','cpp']],'repeats':3,
         'schedule_seed':1,'llm':{'cost_cap_usd':30}}
    seen={}
    monkeypatch.setattr(fps,'freeze',lambda cfg,phase:({},tmp_path))
    class Provider:
        cap_reached=False;total_cost=0.0
        def __init__(self,llm,ledger):self.cost_cap=llm['cost_cap_usd'];self.ledger=ledger
    def fake_run(cfg,pid,a,b,folder,provider,attempt):
        seen.setdefault(provider.ledger.name,[]).append((pid,a,b,attempt))
        assert provider.cost_cap==10
        return {'status':'collection_complete','category':'success','reason':None}
    monkeypatch.setattr(fps,'create_provider',lambda llm,ledger=None:Provider(llm,ledger))
    monkeypatch.setattr(fps,'run_observation',fake_run)
    for i in (1,2,3):fps.run_campaign(cfg,'pilot',f'{i}/3')
    jobs=[j for v in seen.values() for j in v]
    assert sorted(seen)==['cost_ledger-1of3.jsonl','cost_ledger-2of3.jsonl','cost_ledger-3of3.jsonl']
    assert len(jobs)==len(set(jobs))==12 and not (tmp_path/'observations.json').exists()
    with pytest.raises(ValueError):fps.parse_shard('4/3')
