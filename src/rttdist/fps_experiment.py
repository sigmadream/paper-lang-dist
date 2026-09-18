"""Versioned similarity/FPS experiment, isolated from legacy hash protocols."""
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
from rttdist.fps_state import FPSState
from rttdist.jplag_similarity import measure
from rttdist.providers import create_provider, ProviderError

PROMPT_VERSION='fps.translation.v1'
SYSTEM = ('Translate the supplied program to the requested language, preserving its complete '
          'stdin/stdout behavior for every valid input in the specification. Return exactly one '
          'complete source file in one fenced code block, with no explanation. Use only the '
          'standard libraries shipped with the specified toolchain. C++: C++17 with main(). '
          'Haskell: GHC, module Main and main :: IO (). Prolog: SWI-Prolog, define main/0; '
          'the evaluator invokes main; do not add initialization directives. Preserve required '
          'algorithmic constraints and output ordering. Do not hard-code examples.')

def load_config(path):
    path=Path(path).resolve()
    cfg=yaml.safe_load(path.read_text(encoding='utf-8'))
    if cfg['experiment_version']!='fps-text-v1': raise ValueError('Wrong FPS experiment version')
    for name in ['corpus_root','output_root','validation']:
        cfg[name]=str((path.parent/cfg[name]).resolve())
    if not 0<=cfg['threshold']<=1: raise ValueError('Invalid threshold')
    if cfg['max_fps_size']!=10 or cfg['max_translation_steps']<2: raise ValueError('Invalid limits')
    if cfg['repeats']!=1: raise ValueError('This registered campaign uses R=1')
    if not 10<=len(cfg['problem_ids'])<=20: raise ValueError('Need 10 to 20 common problems')
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

def run_observation(cfg,pid,a,b,folder,provider):
    problem=Path(cfg['corpus_root'])/pid
    origin=(problem/('reference.'+EXTENSIONS[a])).read_text(encoding='utf-8')
    current,previous=origin,origin
    state=FPSState(a,origin,cfg['threshold'],cfg['max_fps_size'],cfg['max_translation_steps'])
    status=None;adjacent=None;origin_sym=None
    steps=[];started=time.monotonic()
    for j in range(1,cfg['max_translation_steps']+1):
        target=b if j%2 else a
        source_language=a if j%2 else b
        stepfolder=folder/f'step-{j:02}'
        payload={'model':cfg['llm']['model'],'messages':prompt(problem,current,source_language,target),
                 **cfg['llm']['generation']}
        try:
            response=provider.complete(payload,stepfolder)
        except ProviderError as exc:
            status='infrastructure_error'
            write_json(stepfolder/'infrastructure_error.json',{'error':str(exc),'at':timestamp()})
            break
        try:
            choice=response['body']['choices'][0]
            text=choice['message']['content']
            source=extract_single_file_source_text(text,preserve_unfenced=True)
        except (KeyError,IndexError,TypeError,SourceExtractionError):
            status='format_error';state.all_functional=False
            steps.append({'step':j,'language':target,'status':status,'fps_size':len(state.states)})
            break
        state_item=state.add(target,source)
        (stepfolder/('source.'+EXTENSIONS[target])).write_text(source,encoding='utf-8',newline='')
        evaluation=evaluate(source,target,problem,stepfolder/'evaluation',cfg['runtime'])
        item={**state_item,'evaluation_status':evaluation['status'],'finish_reason':choice.get('finish_reason'),
              'response_model':response['actual_model'],'response_usage':response['usage'],
              'latency_seconds':response['latency_seconds'], 'sym_adj':None,'sym_origin':None}
        if response['actual_model']!=cfg['llm']['model']:
            status='infrastructure_error';item['reason']='unexpected_response_model'
            steps.append(item);write_json(stepfolder/'step.json',item);break
        restored=target==a
        if evaluation['status']=='success' and len(state.states)<=cfg['max_fps_size'] and restored:
            adj=measure(previous,source,stepfolder/'sym_adj',config=cfg['similarity'])
            orig=measure(origin,source,stepfolder/'sym_origin',config=cfg['similarity'])
            item.update(sym_adj=adj['value'],sym_origin=orig['value'])
            adjacent,origin_sym=adj['value'],orig['value']
            available=adj['status']==orig['status']=='measured'
        else: available=True
        status=state.decide(evaluation['status'],restored,adjacent,available)
        item['termination']=status
        steps.append(item);write_json(stepfolder/'step.json',item)
        if status:break
        current=source
        if restored:previous=source
        if time.monotonic()-started>cfg['observation_wall_seconds']:
            status='infrastructure_error';break
    success=status=='success'
    evaluable=status not in ('infrastructure_error','similarity_unavailable',None)
    record={'problem_id':pid,'route':a+'-via-'+b,'seed_language':a,'target_language':b,
            'status':status,'evaluable':evaluable,'success':success,
            'functional':state.all_functional if evaluable else None,
            'd_n':len(state.states) if success else None,'fps_size_at_stop':len(state.states),
            'fps_limit_exceeded':len(state.states)>cfg['max_fps_size'],
            'sym_final':origin_sym if success else None,'sym_adj':adjacent if success else None,
            'completed_roundtrips':state.completed_roundtrips,'translation_steps':len(steps),
            'states':[{'language':k[0],'sha256':k[1],'first_seen_step':v} for k,v in state.states.items()],
            'steps':steps,'at':timestamp()}
    write_json(folder/'observation.json',record)
    return record

def run_campaign(cfg,phase):
    if phase not in ('pilot','main'):raise ValueError('Invalid phase')
    contract,root=freeze(cfg,phase)
    provider=create_provider(cfg['llm'])
    ids=cfg['pilot_problem_ids'] if phase=='pilot' else cfg['problem_ids']
    if phase=='main':
        gate=Path(cfg['output_root'])/'main_design.json'
        if not gate.exists() or not read_json(gate)['approved_for_main']:
            raise ValueError('Review pilot and freeze main_design.json before main')
    jobs=[(pid,a,b) for pid in ids for a,b in permutations(EXTENSIONS,2)]
    random.Random(cfg['schedule_seed']).shuffle(jobs)
    write_json(root/'schedule.json',jobs)
    records=[]
    for pid,a,b in jobs:
        folder=root/pid/(a+'-via-'+b)
        folder.mkdir(parents=True,exist_ok=True)
        record=folder/'observation.json'
        if record.exists() and read_json(record)['status'] not in ('infrastructure_error',None):
            value=read_json(record)
        else:
            value=run_observation(cfg,pid,a,b,folder,provider)
        records.append(value)
        write_json(root/'progress.json',{'at':timestamp(),'phase':phase,'planned':len(jobs),
                                        'processed':len(records),'last':{'problem_id':pid,'route':a+'-via-'+b,'status':value['status']}})
        print(phase,len(records),len(jobs),pid,a,b,value['status'],flush=True)
    write_json(root/'observations.json',records)
    return records
