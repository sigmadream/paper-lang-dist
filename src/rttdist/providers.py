"""Shared chat-completion transport; only transient infrastructure is retried.

Authentication values and headers never enter persisted requests or errors.
New non-compatible providers implement complete(payload, folder) with this
same persisted response contract and register in create_provider().

Cost accounting (v1/abs_EXPERIMENT.md 4장): when `pricing` is configured, every
newly received response adds usage x price to a JSON-lines ledger, and
`cost_cap_usd` refuses further network calls once the ledger total reaches it.
Cached responses are replayed without charge.
"""
import json
import os
from pathlib import Path
import re
import time
from typing import Protocol
from urllib import request, error, parse

from rttdist.experiment_io import digest, read_json, write_json, timestamp

class ProviderError(RuntimeError):
    pass

class CostCapReached(ProviderError):
    pass

WIRE_OPTIONS={'temperature','top_p','max_tokens','seed','thinking','reasoning_effort'}
# Values accepted by the commandcode.ai gateway (it rejects "none" and "minimal").
REASONING_EFFORTS=('low','medium','high','xhigh','max')
ENV_NAME=re.compile(r'[A-Za-z_][A-Za-z0-9_]{0,63}')
# Cloudflare-fronted gateways (e.g. commandcode.ai) reject urllib's default
# "Python-urllib/x.y" agent with error 1010, so every request names the client.
USER_AGENT='rttdist/2.0'
# 520-524 are Cloudflare origin-connection errors: transient, no response was generated.
RETRYABLE_STATUS=(408,429,500,502,503,504,520,521,522,523,524)
ACCOUNTING_KEYS=('pricing','cost_cap_usd','expected_model')


class Provider(Protocol):
    """Provider adapters return body, actual_model, usage and latency_seconds.

    The folder identifies a logical call, not a prompt hash. Implementations
    must replay a durable response there and must not persist credentials.
    """
    def complete(self, payload: dict, folder: Path) -> dict: ...


PROVIDER_FACTORIES = {}


def register_provider(name, factory):
    """Register an adapter factory(config, ledger=None) without editing runners."""
    if name in PROVIDER_FACTORIES:
        raise ValueError(f'Provider already registered: {name}')
    PROVIDER_FACTORIES[name] = factory

def usage_cost(usage, pricing):
    """USD for one response, or None when usage or pricing is unavailable."""
    if not usage or not pricing: return None
    prompt=usage.get('prompt_tokens') or 0
    completion=usage.get('completion_tokens') or 0
    details=usage.get('prompt_tokens_details') or {}
    cached=min(details.get('cached_tokens') or 0,prompt)
    rate_in=float(pricing.get('input_per_million',0))
    rate_out=float(pricing.get('output_per_million',0))
    rate_cached=float(pricing.get('cached_input_per_million',rate_in))
    return ((prompt-cached)*rate_in+cached*rate_cached+completion*rate_out)/1e6

def model_matches(actual, expected):
    """Gateways may return versioned or prefixed ids; accept containment either way."""
    if not isinstance(actual,str) or not actual.strip(): return False
    a=actual.strip().lower();e=str(expected).strip().lower()
    return a==e or e in a or a in e

class CompatibleProvider:
    def __init__(self, config, ledger=None):
        self.config=dict(config)
        self.wire={k:v for k,v in self.config.items() if k not in ACCOUNTING_KEYS}
        endpoint=parse.urlsplit(config['endpoint'])
        if endpoint.scheme not in ('http','https') or not endpoint.netloc or endpoint.username or endpoint.password or endpoint.query:
            raise ValueError('Endpoint must be HTTP(S), without credentials or query parameters')
        allowed=set(WIRE_OPTIONS)
        if config['provider']=='lmstudio': allowed|={'top_k','repeat_penalty'}
        generation=config.get('generation',{})
        unknown=set(generation)-allowed
        if unknown: raise ValueError(f'Unsupported generation options: {sorted(unknown)}')
        thinking=generation.get('thinking')
        if thinking is not None and not (isinstance(thinking,dict) and thinking.get('type') in ('enabled','disabled')):
            raise ValueError('thinking must be a mapping {"type": "enabled"|"disabled"}')
        effort=generation.get('reasoning_effort')
        if effort is not None and effort not in REASONING_EFFORTS:
            raise ValueError(f'reasoning_effort must be one of {list(REASONING_EFFORTS)}')
        key_env=config.get('api_key_env')
        if key_env is not None and not (isinstance(key_env,str) and ENV_NAME.fullmatch(key_env)):
            # Never echo the value: a common mistake is pasting the secret itself here.
            raise ValueError('api_key_env must be the NAME of an environment variable (e.g. CMD_API_KEY), not the key itself')
        self.pricing=config.get('pricing')
        self.cost_cap=config.get('cost_cap_usd')
        if self.cost_cap is not None and not self.pricing: raise ValueError('cost_cap_usd requires pricing')
        if self.pricing and not {'input_per_million','output_per_million'}<=set(self.pricing):
            raise ValueError('pricing requires input_per_million and output_per_million')
        self.ledger=Path(ledger) if ledger else None
        self.total_cost=0.0;self.calls=0
        self.charges={}
        self.ledger_entries=[]
        if self.ledger and self.ledger.exists():
            for line in self.ledger.read_text(encoding='utf-8').splitlines():
                if line.strip():
                    entry=json.loads(line)
                    call_id=entry.get('call_id') or digest(str(Path(entry['folder']).resolve()))
                    if call_id in self.charges: continue
                    self.ledger_entries.append(entry)
                    self.charges[call_id]=entry['cost_usd']
                    self.total_cost+=entry['cost_usd'];self.calls+=1

    @property
    def cap_reached(self):
        return self.cost_cap is not None and self.total_cost>=self.cost_cap

    def _record_cost(self, folder, result):
        call_id=digest(str(Path(folder).resolve()))
        if call_id in self.charges:
            result['cost_usd']=self.charges[call_id]
            return
        cost=result.get('cost_usd')
        if cost is None:cost=usage_cost(result.get('usage'),self.pricing)
        result['cost_usd']=cost
        if cost is None: return
        self.charges[call_id]=cost
        self.total_cost+=cost;self.calls+=1
        if self.ledger:
            self.ledger.parent.mkdir(parents=True,exist_ok=True)
            self.ledger_entries.append({'call_id':call_id,'folder':str(folder),'usage':result['usage'],'cost_usd':cost,
                                         'total_cost_usd':self.total_cost,'at':timestamp()})
            temporary=self.ledger.with_suffix('.jsonl.tmp')
            temporary.write_text(''.join(json.dumps(entry,ensure_ascii=False)+'\n' for entry in self.ledger_entries),encoding='utf-8')
            os.replace(temporary,self.ledger)

    def complete(self, payload, folder):
        folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
        contract={'provider':self.wire,'payload':payload}
        reqpath=folder/'request.json'
        if reqpath.exists() and read_json(reqpath)!=contract:
            raise ValueError('Stored model request changed; use a new run')
        write_json(reqpath,contract)
        target=folder/'response.json'
        if target.exists():
            result=read_json(target)
            before=dict(result)
            self._record_cost(folder,result)
            if result!=before:write_json(target,result)
            return result
        if (folder/'response_body.txt').exists():
            # A crash after receiving a response must not cause another generation.
            raw=(folder/'response_body.txt').read_text(encoding='utf-8')
            try:
                body=json.loads(raw)
                if not isinstance(body,dict):raise ValueError('Response must be an object')
            except ValueError: raise ProviderError('Malformed response preserved; no regeneration') from None
            result={'body':body,'latency_seconds':None,'received_at':None,
                    'actual_model':body.get('model'),'usage':body.get('usage'),
                    'requested_generation':self.config.get('generation',{}),
                    'applied_generation':None,'applied_generation_reason':'Recovered response; effective options not reported'}
            write_json(target,result)
            self._record_cost(folder,result)
            write_json(target,result)
            return result
        if self.cap_reached:
            raise CostCapReached(f'Cost cap {self.cost_cap} USD reached after {self.calls} calls ({self.total_cost:.4f} USD)')
        headers={'Content-Type':'application/json','User-Agent':USER_AGENT}
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
                if not isinstance(body,dict):raise ValueError('Response must be an object')
                result={'body':body,'latency_seconds':time.monotonic()-start,'received_at':timestamp(),
                        'actual_model':body.get('model'),'usage':body.get('usage'),
                        'requested_generation':self.config.get('generation',{}),
                        'applied_generation':None,'applied_generation_reason':'API does not echo effective decoding options'}
                write_json(target,result)
                self._record_cost(folder,result)
                write_json(target,result)
                return result
            except error.HTTPError as exc:
                code=exc.code
                errors.append({'attempt':len(errors)+1,'http_status':code,'at':timestamp()})
                write_json(errors_path,errors)
                if code not in RETRYABLE_STATUS or attempt==self.config['retries']:
                    raise ProviderError(f'HTTP {code}; response body withheld to avoid credential leakage') from None
            except (error.URLError, TimeoutError) as exc:
                errors.append({'attempt':len(errors)+1,'type':type(exc).__name__,'at':timestamp()})
                write_json(errors_path,errors)
                if attempt==self.config['retries']: raise ProviderError(type(exc).__name__) from None
            except (ValueError,KeyError) as exc:
                raise ProviderError('Malformed response preserved; no regeneration') from None
            time.sleep(min(2**attempt,8))

def create_provider(config, ledger=None):
    factory = PROVIDER_FACTORIES.get(config['provider'])
    if factory is None:
        raise ValueError(f"Unknown provider: {config['provider']}")
    return factory(config, ledger=ledger)


register_provider('lmstudio', CompatibleProvider)
register_provider('openai_compatible', CompatibleProvider)
