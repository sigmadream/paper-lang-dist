import io
import json
from pathlib import Path
import pytest
from urllib.error import HTTPError
from rttdist.providers import create_provider, ProviderError

def config(provider='lmstudio'):
    return {'provider':provider,'endpoint':'http://localhost:1234/v1','model':'test',
            'generation':{'temperature':0},'request_timeout':1,'retries':1,'api_key_env':None}

def test_compatible_provider_rejects_nonportable_options():
    c=config('openai_compatible');c['generation']['top_k']=1
    with pytest.raises(ValueError,match='Unsupported generation'):create_provider(c)

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
    assert a==b and len(calls)==1 and a['usage'] is None
    assert all('sentinel-secret' not in f.read_text() for f in tmp_path.glob('*.json'))

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

def test_crash_after_receipt_reuses_bytes_and_changed_payload_rejected(tmp_path,monkeypatch):
    (tmp_path/'response_body.txt').write_text('{"model":"test"}')
    monkeypatch.setattr('rttdist.providers.request.urlopen',lambda *a,**kw:pytest.fail('Unexpected model call'))
    p=create_provider(config());r=p.complete({},tmp_path)
    assert r['latency_seconds'] is None and r['actual_model']=='test'
    with pytest.raises(ValueError,match='changed'):p.complete({'model':'different'},tmp_path)
