import io
import json
from pathlib import Path
import pytest
from urllib.error import HTTPError
from rttdist.providers import create_provider, ProviderError, CostCapReached, model_matches, usage_cost

def config(provider='lmstudio'):
    return {'provider':provider,'endpoint':'http://localhost:1234/v1','model':'test',
            'generation':{'temperature':0},'request_timeout':1,'retries':1,'api_key_env':None}

def test_compatible_provider_rejects_nonportable_options():
    c=config('openai_compatible');c['generation']['top_k']=1
    with pytest.raises(ValueError,match='Unsupported generation'):create_provider(c)

def test_thinking_option_accepted_and_validated():
    c=config('openai_compatible');c['generation']['thinking']={'type':'disabled'}
    create_provider(c)
    c['generation']['thinking']={'type':'off'}
    with pytest.raises(ValueError,match='thinking'):create_provider(c)

def test_reasoning_effort_accepted_and_validated():
    c=config('openai_compatible');c['generation']['reasoning_effort']='low'
    create_provider(c)
    c['generation']['reasoning_effort']='none'
    with pytest.raises(ValueError,match='reasoning_effort'):create_provider(c)

def test_response_reused_with_missing_usage_and_no_secret(tmp_path,monkeypatch):
    c=config('openai_compatible');c['api_key_env']='FPS_TEST_KEY'
    monkeypatch.setenv('FPS_TEST_KEY','sentinel-secret')
    calls=[]
    def send(req,timeout):
        calls.append(req)
        return io.BytesIO(json.dumps({'model':'test','choices':[]}).encode())
    monkeypatch.setattr('rttdist.providers.request.urlopen',send)
    p=create_provider(c)
    a=p.complete({'model':'test'},tmp_path);b=p.complete({'model':'test'},tmp_path)
    assert a==b and len(calls)==1 and a['usage'] is None and a['cost_usd'] is None
    assert all('sentinel-secret' not in f.read_text() for f in tmp_path.glob('*.json'))
    assert calls[0].get_header('User-agent')=='rttdist/2.0'

def test_auth_error_not_retried_and_body_not_logged(tmp_path,monkeypatch):
    calls=[]
    def send(req,timeout):
        calls.append(req)
        raise HTTPError(req.full_url,401,'secret echoed by server',{},None)
    monkeypatch.setattr('rttdist.providers.request.urlopen',send)
    with pytest.raises(ProviderError,match='401'):create_provider(config()).complete({},tmp_path)
    assert len(calls)==1
    assert 'secret echoed' not in (tmp_path/'api_errors.json').read_text()

def test_transient_retry_does_not_replace_received_response(tmp_path,monkeypatch):
    calls=[]
    def send(req,timeout):
        calls.append(req)
        if len(calls)==1:raise HTTPError(req.full_url,503,'temporary',{},None)
        return io.BytesIO(b'{"model":"test","usage":null}')
    monkeypatch.setattr('rttdist.providers.request.urlopen',send)
    monkeypatch.setattr('rttdist.providers.time.sleep',lambda n:None)
    p=create_provider(config());p.complete({},tmp_path);p.complete({},tmp_path)
    assert len(calls)==2 and len(json.loads((tmp_path/'api_errors.json').read_text()))==1

def test_cloudflare_520_is_retried(tmp_path,monkeypatch):
    calls=[]
    def send(req,timeout):
        calls.append(req)
        if len(calls)==1:raise HTTPError(req.full_url,520,'origin error',{},None)
        return io.BytesIO(b'{"model":"test","usage":null}')
    monkeypatch.setattr('rttdist.providers.request.urlopen',send)
    monkeypatch.setattr('rttdist.providers.time.sleep',lambda n:None)
    create_provider(config()).complete({},tmp_path)
    assert len(calls)==2

def test_crash_after_receipt_reuses_bytes_and_changed_payload_rejected(tmp_path,monkeypatch):
    (tmp_path/'response_body.txt').write_text('{"model":"test"}')
    monkeypatch.setattr('rttdist.providers.request.urlopen',lambda *a,**kw:pytest.fail('Unexpected model call'))
    p=create_provider(config());r=p.complete({},tmp_path)
    assert r['latency_seconds'] is None and r['actual_model']=='test'
    with pytest.raises(ValueError,match='changed'):p.complete({'model':'different'},tmp_path)

def test_usage_cost_counts_cached_prompt_tokens():
    pricing={'input_per_million':1.0,'output_per_million':4.0,'cached_input_per_million':0.25}
    usage={'prompt_tokens':1000,'completion_tokens':500,'prompt_tokens_details':{'cached_tokens':200}}
    assert usage_cost(usage,pricing)==pytest.approx((800*1.0+200*0.25+500*4.0)/1e6)
    assert usage_cost(None,pricing) is None and usage_cost(usage,None) is None

def test_cost_ledger_and_cap_block_new_calls_but_replay_cached(tmp_path,monkeypatch):
    c=config('openai_compatible');c['pricing']={'input_per_million':1.0,'output_per_million':2.0};c['cost_cap_usd']=0.0035
    calls=[]
    def send(req,timeout):
        calls.append(req)
        return io.BytesIO(json.dumps({'model':'test','choices':[],'usage':{'prompt_tokens':1000,'completion_tokens':500}}).encode())
    monkeypatch.setattr('rttdist.providers.request.urlopen',send)
    ledger=tmp_path/'ledger.jsonl'
    p=create_provider(c,ledger)
    a=p.complete({'model':'test','n':1},tmp_path/'a')
    assert a['cost_usd']==pytest.approx(0.002) and p.total_cost==pytest.approx(0.002) and not p.cap_reached
    p.complete({'model':'test','n':2},tmp_path/'b')
    assert p.cap_reached and len(calls)==2
    with pytest.raises(CostCapReached):p.complete({'model':'test','n':3},tmp_path/'c')
    assert p.complete({'model':'test','n':1},tmp_path/'a')==a and len(calls)==2
    q=create_provider(c,ledger)
    assert q.total_cost==pytest.approx(0.004) and q.calls==2 and q.cap_reached
    assert 'cost_cap_usd' not in (tmp_path/'a'/'request.json').read_text()

def test_pasted_secret_in_api_key_env_is_rejected_without_echo():
    c=config('openai_compatible');secret='sk-'+'x'*90
    c['api_key_env']=secret
    with pytest.raises(ValueError) as info:create_provider(c)
    assert secret not in str(info.value) and 'NAME of an environment variable' in str(info.value)
    c['api_key_env']='CMD_API_KEY';create_provider(c)

def test_cap_requires_pricing():
    c=config('openai_compatible');c['cost_cap_usd']=1
    with pytest.raises(ValueError,match='pricing'):create_provider(c)

def test_model_matches_tolerates_prefixes_and_versions():
    assert model_matches('zai-org/GLM-5.3','zai-org/GLM-5.3')
    assert model_matches('GLM-5.3','zai-org/GLM-5.3')
    assert model_matches('zai-org/GLM-5.3-20260901','zai-org/GLM-5.3')
    assert not model_matches('other-model','zai-org/GLM-5.3')
    assert not model_matches(None,'zai-org/GLM-5.3') and not model_matches('','x')
