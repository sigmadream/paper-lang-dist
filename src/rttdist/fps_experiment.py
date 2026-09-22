"""Versioned similarity/FPS experiment, protocol v2 (v1/abs_PLAN.md, v1/abs_EXPERIMENT.md 4장).

Differences from fps-text-v1: N repeated attempts per (problem, route) with a
per-attempt seed, several thresholds recorded while translation continues to
the largest one, configurable routes (control languages as intermediates),
cost ledger with a hard cap, and tolerant response-model matching.
"""
from itertools import permutations
from pathlib import Path
import json
import random
import time
import urllib.request

import yaml

from rttdist.experiment_io import digest, read_json, write_json, timestamp
from rttdist.extract import extract_single_file_source_text, SourceExtractionError
from rttdist.fps_execution import evaluate, EXTENSIONS
from rttdist.fps_state import FPSState, threshold_key
from rttdist.jplag_similarity import measure
from rttdist.providers import create_provider, ProviderError, CostCapReached, model_matches

EXPERIMENT_VERSION='fps-text-v2'
PROMPT_VERSION='fps.translation.v2'
DEFAULT_LANGUAGES=('cpp','haskell','prolog')
SYSTEM = ('Translate the supplied program to the requested language, preserving its complete '
          'stdin/stdout behavior for every valid input in the specification. Return exactly one '
          'complete source file in one fenced code block, with no explanation. Use only the '
          'standard libraries shipped with the specified toolchain. C++: C++17 with main(). '
          'Haskell: GHC, module Main and main :: IO (). Prolog: SWI-Prolog, define main/0; '
          'the evaluator invokes main; do not add initialization directives. '
          'Python: Python 3, one script that reads stdin and writes stdout. '
          'Java: Java 17, one file declaring public class Main with public static void main. '
          'Preserve required algorithmic constraints and output ordering. Do not hard-code examples.')

def parse_route(value):
    if isinstance(value,str): value=value.split('-via-')
    if len(value)!=2: raise ValueError(f'Invalid route {value!r}')
    return [str(value[0]),str(value[1])]

def load_config(path):
    path=Path(path).resolve()
    cfg=yaml.safe_load(path.read_text(encoding='utf-8'))
    if cfg['experiment_version']!=EXPERIMENT_VERSION: raise ValueError('Wrong FPS experiment version')
    for name in ['corpus_root','output_root','validation']:
        cfg[name]=str((path.parent/cfg[name]).resolve())
    if not 0<=cfg['threshold']<=1: raise ValueError('Invalid threshold')
    thresholds=sorted({float(v) for v in cfg.get('thresholds') or []}|{float(cfg['threshold'])})
    if any(not 0<=v<=1 for v in thresholds): raise ValueError('Invalid thresholds')
    cfg['thresholds']=thresholds
    if cfg['max_fps_size']!=10 or cfg['max_translation_steps']<2: raise ValueError('Invalid limits')
    if type(cfg['repeats']) is not int or cfg['repeats']<1: raise ValueError('repeats must be a positive integer')
    if not 10<=len(cfg['problem_ids'])<=20: raise ValueError('Need 10 to 20 common problems')
    if any(p not in cfg['problem_ids'] for p in cfg.get('pilot_problem_ids',[])): raise ValueError('Pilot problems must be in problem_ids')
    routes=[parse_route(r) for r in (cfg.get('routes') or [list(p) for p in permutations(DEFAULT_LANGUAGES,2)])]
    for a,b in routes:
        if a==b or a not in EXTENSIONS or b not in EXTENSIONS: raise ValueError(f'Invalid route {a}->{b}')
        if a not in cfg['runtime']['tools'] or b not in cfg['runtime']['tools']: raise ValueError(f'Route {a}->{b} needs runtime tools for both languages')
    if len({tuple(r) for r in routes})!=len(routes): raise ValueError('Duplicate routes')
    cfg['routes']=routes
    create_provider(cfg['llm'])
    return cfg

def corpus_hashes(cfg):
    corpus=Path(cfg['corpus_root'])
    paths=[corpus/'selection.json']
    for pid in cfg['problem_ids']:
        paths.extend(p for p in (corpus/pid).rglob('*') if p.is_file())
    return {str(p.relative_to(corpus)):digest(p.read_bytes()) for p in sorted(paths)}

def freeze(cfg,phase):
    validation=read_json(cfg['validation'])
    if not validation['passed']: raise ValueError('Reference validation gate has not passed')
    hashes=corpus_hashes(cfg)
    if any(validation['file_hashes'].get(k)!=v for k,v in hashes.items()):
        raise ValueError('Corpus changed since reference validation')
    if cfg['runtime']!=validation['runtime']: raise ValueError('Runtime changed since validation')
    if digest(Path(cfg['similarity']['jar']).read_bytes())!=cfg['similarity']['jar_sha256']:
        raise ValueError('Similarity JAR changed')
    folder=Path(cfg['output_root'])/phase
    folder.mkdir(parents=True,exist_ok=True)
    root=Path(__file__).resolve().parent
    contract={'config':cfg,'phase':phase,'corpus_hashes':hashes,'prompt_version':PROMPT_VERSION,
              'system_prompt':SYSTEM,'implementation_hashes':{p.name:digest(p.read_bytes()) for p in
                [root/'fps_experiment.py',root/'fps_execution.py',root/'fps_state.py',root/'providers.py',root/'jplag_similarity.py',root/'extract.py']}}
    path=folder/'contract.json'
    if path.exists():
        if read_json(path)!=contract: raise ValueError('Run contract changed; never resume with changed conditions')
    else:
        write_json(path,contract)
        write_json(folder/'started.json',{'at':timestamp()})
        metadata={'provider':cfg['llm']['provider'],'model':cfg['llm']['model'],'details':None}
        if cfg['llm']['provider']=='lmstudio':
            try:
                endpoint=cfg['llm']['endpoint'].rstrip('/').removesuffix('/v1')+'/api/v0/models'
                with urllib.request.urlopen(endpoint,timeout=10) as stream:
                    models=json.load(stream)
                metadata['details']=next((m for m in models.get('data',[]) if m['id']==cfg['llm']['model']),None)
            except Exception as exc: metadata['unavailable_reason']=type(exc).__name__
        write_json(folder/'model_metadata.json',metadata)
    return contract,folder

def prompt(problem,source,a,b):
    examples=[]
    seen=set()
    for p in sorted((problem/'prompt_examples').glob('*.inp')):
        pair=(p.read_text(encoding='utf-8'),p.with_suffix('.out').read_text(encoding='utf-8'))
        if pair not in seen:
            examples.append({'input':pair[0],'output':pair[1]});seen.add(pair)
        if len(examples)>=2:break
    return [{'role':'system','content':SYSTEM}, {'role':'user','content':
        f'Source language: {a}\nTarget language: {b}\nSpecification:\n'+problem.joinpath('statement.md').read_text(encoding='utf-8')+
        '\nPublic examples:\n'+json.dumps(examples,ensure_ascii=False)+'\nSource code:\n'+source}]

def attempt_generation(cfg,attempt):
    """Per-attempt decoding options: the configured seed is offset by the attempt index."""
    generation=dict(cfg['llm']['generation'])
    if generation.get('seed') is not None: generation['seed']=int(generation['seed'])+attempt-1
    return generation

def run_observation(cfg,pid,a,b,folder,provider,attempt=1):
    problem=Path(cfg['corpus_root'])/pid
    origin=(problem/('reference.'+EXTENSIONS[a])).read_text(encoding='utf-8')
    current,previous=origin,origin
    state=FPSState(a,origin,cfg['threshold'],cfg['max_fps_size'],cfg['max_translation_steps'],thresholds=cfg.get('thresholds'))
    generation=attempt_generation(cfg,attempt)
    expected_model=cfg['llm'].get('expected_model') or cfg['llm']['model']
    status=None;adjacent=None;reason=None
    steps=[];started=time.monotonic()
    for j in range(1,cfg['max_translation_steps']+1):
        target=b if j%2 else a
        source_language=a if j%2 else b
        stepfolder=folder/f'step-{j:02}'
        payload={'model':cfg['llm']['model'],'messages':prompt(problem,current,source_language,target),**generation}
        try:
            response=provider.complete(payload,stepfolder)
        except ProviderError as exc:
            status='infrastructure_error'
            reason='cost_cap_reached' if isinstance(exc,CostCapReached) else 'provider_error'
            write_json(stepfolder/'infrastructure_error.json',{'error':str(exc),'reason':reason,'at':timestamp()})
            break
        try:
            choice=response['body']['choices'][0]
            text=choice['message']['content']
            source=extract_single_file_source_text(text,preserve_unfenced=True)
        except (KeyError,IndexError,TypeError,SourceExtractionError):
            status='format_error';state.all_functional=False
            steps.append({'step':j,'language':target,'status':status,'fps_size':len(state.states),'termination':status})
            break
        state_item=state.add(target,source)
        (stepfolder/('source.'+EXTENSIONS[target])).write_text(source,encoding='utf-8',newline='')
        evaluation=evaluate(source,target,problem,stepfolder/'evaluation',cfg['runtime'])
        item={**state_item,'evaluation_status':evaluation['status'],'finish_reason':choice.get('finish_reason'),
              'response_model':response['actual_model'],'response_usage':response['usage'],
              'cost_usd':response.get('cost_usd'),'latency_seconds':response['latency_seconds'],
              'sym_adj':None,'sym_origin':None,'sym_status':None}
        if not model_matches(response['actual_model'],expected_model):
            status='infrastructure_error';reason='unexpected_response_model';item['reason']=reason;item['termination']=status
            steps.append(item);write_json(stepfolder/'step.json',item);break
        restored=target==a
        available=True
        if evaluation['status']=='success' and len(state.states)<=cfg['max_fps_size'] and restored:
            adj=measure(previous,source,stepfolder/'sym_adj',config=cfg['similarity'])
            orig=measure(origin,source,stepfolder/'sym_origin',config=cfg['similarity'])
            item.update(sym_adj=adj['value'],sym_origin=orig['value'],sym_status=adj['status'])
            adjacent=adj['value']
            available=adj['status']=='measured'
        status=state.decide(evaluation['status'],restored,adjacent,available)
        item['termination']=status
        item['thresholds_reached']=[k for k,v in state.reached.items() if v['step']==j]
        steps.append(item);write_json(stepfolder/'step.json',item)
        if status:break
        current=source
        if restored:previous=source
        if time.monotonic()-started>cfg['observation_wall_seconds']:
            status='infrastructure_error';reason='observation_wall_clock';break
    outcomes=state.outcomes(status)
    measured_any=any(s.get('sym_status')=='measured' for s in steps)
    if not measured_any and state.similarity_unavailable_steps and status in ('translation_budget_reached','max_distance_reached'):
        # Every restored step was unmeasurable: the attempt cannot be judged (v1/abs_PLAN.md 2.4, 무효).
        reason=reason or 'similarity_unavailable'
        for o in outcomes.values():
            if not o['success']: o['category']='invalid'
    primary=outcomes[threshold_key(cfg['threshold'])]
    evaluable=primary['category']!='invalid'
    by_step={s['step']:s for s in steps}
    reach=by_step.get(primary['reached_step'],{}) if primary['reached_step'] else {}
    record={'problem_id':pid,'route':a+'-via-'+b,'seed_language':a,'target_language':b,'attempt':attempt,
            'seed':generation.get('seed'),'status':status,'reason':reason,'evaluable':evaluable,
            'category':primary['category'],'success':primary['success'],'d_n':primary['d_n'],
            'reached_step':primary['reached_step'],'reached_roundtrip':primary['reached_roundtrip'],
            'sym_adj':primary['sym_adj'],'sym_origin_at_reach':reach.get('sym_origin'),
            'outcomes':outcomes,'primary_threshold':threshold_key(cfg['threshold']),
            'functional':state.all_functional if evaluable else None,
            'fps_size_at_stop':len(state.states),'fps_limit_exceeded':len(state.states)>cfg['max_fps_size'],
            'similarity_unavailable_steps':state.similarity_unavailable_steps,
            'completed_roundtrips':state.completed_roundtrips,'translation_steps':len(steps),
            'duplicate_steps':sum(1 for s in steps if s.get('duplicate')),
            'cost_usd':sum(s['cost_usd'] for s in steps if s.get('cost_usd') is not None) if any(s.get('cost_usd') is not None for s in steps) else None,
            'states':[{'language':k[0],'sha256':k[1],'first_seen_step':v} for k,v in state.states.items()],
            'steps':steps,'at':timestamp()}
    write_json(folder/'observation.json',record)
    return record

def attempt_folder(root,pid,a,b,attempt):
    return root/pid/(a+'-via-'+b)/f'attempt-{attempt:02}'

def parse_shard(value):
    """'i/k' (1-based) -> (i,k); None runs every job in one process."""
    if value is None:return None
    i,k=(int(x) for x in str(value).split('/'))
    if not 1<=i<=k:raise ValueError('Shard must be i/k with 1<=i<=k')
    return i,k

def run_campaign(cfg,phase,shard=None):
    if phase not in ('pilot','main'):raise ValueError('Invalid phase')
    shard=parse_shard(shard)
    contract,root=freeze(cfg,phase)
    llm=dict(cfg['llm']);suffix=''
    if shard:
        # Each shard keeps its own ledger and an equal share of the cap, so the sum never exceeds the cap.
        suffix=f'-{shard[0]}of{shard[1]}'
        if llm.get('cost_cap_usd') is not None:llm['cost_cap_usd']=llm['cost_cap_usd']/shard[1]
    provider=create_provider(llm,ledger=root/f'cost_ledger{suffix}.jsonl')
    ids=cfg['pilot_problem_ids'] if phase=='pilot' else cfg['problem_ids']
    if phase=='main':
        gate=Path(cfg['output_root'])/'main_design.json'
        if not gate.exists() or not read_json(gate)['approved_for_main']:
            raise ValueError('Review pilot and freeze main_design.json before main')
    jobs=[(pid,a,b,attempt) for pid in ids for a,b in cfg['routes'] for attempt in range(1,cfg['repeats']+1)]
    random.Random(cfg['schedule_seed']).shuffle(jobs)
    write_json(root/'schedule.json',jobs)
    if shard:jobs=[job for index,job in enumerate(jobs) if index%shard[1]==shard[0]-1]
    records=[];stopped=None
    for pid,a,b,attempt in jobs:
        folder=attempt_folder(root,pid,a,b,attempt)
        folder.mkdir(parents=True,exist_ok=True)
        record=folder/'observation.json'
        if record.exists() and read_json(record)['status'] not in ('infrastructure_error',None):
            value=read_json(record)
        else:
            if provider.cap_reached: stopped='cost_cap_reached';break
            value=run_observation(cfg,pid,a,b,folder,provider,attempt)
        records.append(value)
        write_json(root/f'progress{suffix}.json',{'at':timestamp(),'phase':phase,'planned':len(jobs),'processed':len(records),
                                         'cost_usd':provider.total_cost,'cost_cap_usd':provider.cost_cap,
                                         'last':{'problem_id':pid,'route':a+'-via-'+b,'attempt':attempt,'status':value['status'],'category':value['category']}})
        print(phase,len(records),len(jobs),pid,a,b,attempt,value['status'],value['category'],f'{provider.total_cost:.4f}USD',flush=True)
        if value.get('reason')=='cost_cap_reached': stopped='cost_cap_reached';break
    if not shard:write_json(root/'observations.json',records)
    if stopped: print(f'Campaign stopped: {stopped} ({provider.total_cost:.4f} USD of cap {provider.cost_cap})',flush=True)
    return records
