import json
from pathlib import Path
import pytest
from rttdist import fps_experiment as fps
from rttdist.experiment_io import write_json

class ReplayProvider:
    def __init__(self, outputs): self.outputs=iter(outputs);self.calls=0
    def complete(self,payload,folder):
        p=Path(folder)/'response.json'
        if p.exists():return json.loads(p.read_text())
        self.calls+=1
        response={'body':{'choices':[{'message':{'content':next(self.outputs)},'finish_reason':'stop'}]},
                  'actual_model':'test','usage':None,'latency_seconds':.1}
        write_json(p,response)
        return response

@pytest.fixture
def setup(tmp_path,monkeypatch):
    problem=tmp_path/'corpus'/'p';problem.mkdir(parents=True)
    (problem/'reference.cpp').write_text('A')
    (problem/'statement.md').write_text('Problem')
    monkeypatch.setattr(fps,'evaluate',lambda *args:{'status':'success'})
    monkeypatch.setattr(fps,'measure',lambda *args,**kw:{'status':'measured','value':.9})
    cfg={'corpus_root':str(tmp_path/'corpus'),'threshold':.85,'max_fps_size':10,'max_translation_steps':20,
         'llm':{'model':'test','generation':{}},'runtime':{},'similarity':{},'observation_wall_seconds':30}
    folder=tmp_path/'observation';folder.mkdir()
    return cfg,folder

def test_replay_and_conditional_distance(setup):
    cfg,folder=setup;p=ReplayProvider(['B','A1'])
    first=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    second=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert first['d_n']==second['d_n']==3
    assert first['states']==second['states']
    assert p.calls==2

def test_intermediate_failure_stops_and_has_no_distance(setup,monkeypatch):
    cfg,folder=setup;p=ReplayProvider(['bad'])
    monkeypatch.setattr(fps,'evaluate',lambda *args:{'status':'compile_error'})
    r=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert p.calls==1 and r['evaluable'] and not r['functional']
    assert r['d_n'] is None and r['sym_final'] is None and r['fps_size_at_stop']==2

def test_origin_score_does_not_stop_and_intermediate_limit_has_no_return(setup,monkeypatch):
    cfg,folder=setup
    # First restored source duplicates x0, so the tenth new state arrives on an odd step.
    p=ReplayProvider(['B1','A','B2','A2','B3','A3','B4','A4','B5','A5','B6'])
    monkeypatch.setattr(fps,'measure',lambda a,b,folder,**kw:{'status':'measured','value':1 if folder.name=='sym_origin' else .1})
    r=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert r['status']=='max_distance_reached' and r['fps_size_at_stop']==11
    assert p.calls==11 and r['steps'][-1]['language']=='prolog'
    assert r['functional'] and not r['success'] and r['d_n'] is None

def test_unavailable_is_not_zero(setup,monkeypatch):
    cfg,folder=setup;p=ReplayProvider(['B','A1'])
    monkeypatch.setattr(fps,'measure',lambda *args,**kw:{'status':'unavailable','value':None})
    r=fps.run_observation(cfg,'p','cpp','prolog',folder,p)
    assert r['status']=='similarity_unavailable' and not r['evaluable']
