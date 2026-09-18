"""Shared chat-completion transport; only transient infrastructure is retried.

Authentication values and headers never enter persisted requests or errors.
New non-compatible providers implement complete(payload, folder) with this
same persisted response contract and register in create_provider().
"""
import json
import os
from pathlib import Path
import time
from urllib import request, error, parse

from rttdist.experiment_io import digest, read_json, write_json, timestamp

class ProviderError(RuntimeError):
    pass

class CompatibleProvider:
    def __init__(self, config):
        self.config=dict(config)
        endpoint=parse.urlsplit(config['endpoint'])
        if endpoint.scheme not in ('http','https') or not endpoint.netloc or endpoint.username or endpoint.password or endpoint.query:
            raise ValueError('Endpoint must be HTTP(S), without credentials or query parameters')
        allowed={'temperature','top_p','max_tokens','seed'}
        if config['provider']=='lmstudio': allowed|={'top_k','repeat_penalty'}
        unknown=set(config.get('generation',{}))-allowed
        if unknown: raise ValueError(f'Unsupported generation options: {sorted(unknown)}')

    def complete(self, payload, folder):
        folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
        contract={'provider':self.config,'payload':payload}
        reqpath=folder/'request.json'
        if reqpath.exists() and read_json(reqpath)!=contract:
            raise ValueError('Stored model request changed; use a new run')
        write_json(reqpath,contract)
        target=folder/'response.json'
        if target.exists(): return read_json(target)
        if (folder/'response_body.txt').exists():
            # A crash after receiving a response must not cause another generation.
            raw=(folder/'response_body.txt').read_text(encoding='utf-8')
            try: body=json.loads(raw)
            except ValueError: raise ProviderError('Malformed response preserved; no regeneration') from None
            result={'body':body,'latency_seconds':None,'received_at':None,
                    'actual_model':body.get('model'),'usage':body.get('usage'),
                    'requested_generation':self.config.get('generation',{}),
                    'applied_generation':None,'applied_generation_reason':'Recovered response; effective options not reported'}
            write_json(target,result)
            return result
        headers={'Content-Type':'application/json'}
        key_env=self.config.get('api_key_env')
        if key_env:
            key=os.environ.get(key_env)
            if not key: raise ProviderError(f'Missing API key environment variable {key_env}')
            headers['Authorization']='Bearer '+key
        errors_path=folder/'api_errors.json'
        errors=read_json(errors_path) if errors_path.exists() else []
        for attempt in range(self.config['retries']+1):
            start=time.monotonic()
            try:
                req=request.Request(self.config['endpoint'].rstrip('/')+'/chat/completions',
                                    data=json.dumps(payload,ensure_ascii=False).encode('utf-8'),headers=headers)
                with request.urlopen(req,timeout=self.config['request_timeout']) as stream:
                    raw=stream.read().decode('utf-8')
                # Preserve received bytes before parsing: malformed output is not regenerated.
                (folder/'response_body.txt').write_text(raw,encoding='utf-8')
                body=json.loads(raw)
                result={'body':body,'latency_seconds':time.monotonic()-start,'received_at':timestamp(),
                        'actual_model':body.get('model'),'usage':body.get('usage'),
                        'requested_generation':self.config.get('generation',{}),
                        'applied_generation':None,'applied_generation_reason':'API does not echo effective decoding options'}
                write_json(target,result)
                return result
            except error.HTTPError as exc:
                code=exc.code
                errors.append({'attempt':len(errors)+1,'http_status':code,'at':timestamp()})
                write_json(errors_path,errors)
                if code not in (408,429,500,502,503,504) or attempt==self.config['retries']:
                    raise ProviderError(f'HTTP {code}; response body withheld to avoid credential leakage') from None
            except (error.URLError, TimeoutError) as exc:
                errors.append({'attempt':len(errors)+1,'type':type(exc).__name__,'at':timestamp()})
                write_json(errors_path,errors)
                if attempt==self.config['retries']: raise ProviderError(type(exc).__name__) from None
            except (ValueError,KeyError) as exc:
                raise ProviderError('Malformed response preserved; no regeneration') from None
            time.sleep(min(2**attempt,8))

def create_provider(config):
    if config['provider'] not in ('lmstudio','openai_compatible'):
        raise ValueError('Provider must be lmstudio or openai_compatible')
    return CompatibleProvider(config)
