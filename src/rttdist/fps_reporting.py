"""Rebuild FPS tables, intervals, paired comparisons and figures without model calls."""
from collections import Counter
import csv
from itertools import permutations, combinations
import math
from pathlib import Path

import numpy as np

from rttdist.experiment_io import read_json, write_json, timestamp, digest
from rttdist.fps_state import source_hash
from rttdist.fps_execution import canonical_output
from rttdist.extract import extract_single_file_source_text

LANGUAGES=['cpp','haskell','prolog']

def wilson(k,n):
    if not n:return None
    z=1.959963984540054;p=k/n;den=1+z*z/n
    mid=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [max(0,mid-half),min(1,mid+half)]

def distribution(values):
    a=np.asarray([v for v in values if v is not None],dtype=float)
    if not len(a):return {'n':0,'median':None,'q1':None,'q3':None,'mean':None}
    return {'n':len(a),'median':float(np.median(a)),'q1':float(np.quantile(a,.25)),
            'q3':float(np.quantile(a,.75)),'mean':float(np.mean(a))}

def summarize(records,ids,replicates,seed):
    rng=np.random.default_rng(seed)
    draws=rng.integers(0,len(ids),size=(replicates,len(ids)))
    routes={}
    for a,b in permutations(LANGUAGES,2):
        route=a+'-via-'+b
        indexed={r['problem_id']:r for r in records if r['route']==route and r['problem_id'] in ids}
        rs=list(indexed.values());ev=[r for r in rs if r['evaluable']];ok=[r for r in ev if r['success']]
        success=np.array([float(indexed[i]['success']) if i in indexed and indexed[i]['evaluable'] else np.nan for i in ids])
        bs=[]
        for sample in draws:
            valid=success[sample];valid=valid[~np.isnan(valid)]
            if len(valid):bs.append(float(np.mean(valid)))
        routes[route]={'planned':len(ids),'recorded':len(rs),'evaluable':len(ev),'success':len(ok),
                       'evaluation_failure':len(ev)-len(ok),'unevaluated':len(rs)-len(ev),'incomplete':len(ids)-len(rs),
                       'p_sf':len(ok)/len(ev) if ev else None,
                       'p_functional':sum(r['functional'] for r in ev)/len(ev) if ev else None,
                       'p_functional_wilson95':wilson(sum(r['functional'] for r in ev),len(ev)),
                       'wilson95':wilson(len(ok),len(ev)),
                       'bootstrap95':np.quantile(bs,[.025,.975]).tolist() if bs else None,
                       'bootstrap_degenerate':len(set(bs))==1 if bs else None,
                       'statuses':dict(Counter(r['status'] for r in rs)),
                       'd_n':distribution([r['d_n'] for r in ok]),
                       'sym_final':distribution([r['sym_final'] for r in ok]),
                       'sym_adj':distribution([r['sym_adj'] for r in ok])}
    comparisons=[]
    for a,b in combinations(LANGUAGES,2):
        left=a+'-via-'+b;right=b+'-via-'+a
        index={(r['problem_id'],r['route']):r for r in records}
        for metric in ['success','d_n','sym_final']:
            differences=[]
            common=[]
            for pid in ids:
                l=index.get((pid,left));r=index.get((pid,right))
                valid=l and r and l['evaluable'] and r['evaluable']
                if metric!='success':valid=valid and l['success'] and r['success']
                if valid:common.append(pid);differences.append(float(l[metric])-float(r[metric]))
            values=dict(zip(common,differences));boot=[]
            for sample in draws:
                ds=[values[ids[i]] for i in sample if ids[i] in values]
                if ds:boot.append(float(np.mean(ds)))
            comparisons.append({'left':left,'right':right,'metric':metric,'common_n':len(common),
                'common_problem_ids':common,'mean_difference':float(np.mean(differences)) if differences else None,
                'bonferroni95_family3':np.quantile(boot,[.05/6,1-.05/6]).tolist() if boot else None,
                'bootstrap_valid_replicates':len(boot),'bootstrap_degenerate':len(set(boot))==1 if boot else None,
                'unavailable_reason':None if differences else 'No common evaluable/successful problems'})
    return {'routes':routes,'paired_comparisons':comparisons}

def audit(cfg,phase,records):
    root=Path(cfg['output_root'])/phase
    ids=cfg['pilot_problem_ids'] if phase=='pilot' else cfg['problem_ids']
    expected={(p,a+'-via-'+b) for p in ids for a,b in permutations(LANGUAGES,2)}
    actual={(r['problem_id'],r['route']) for r in records}
    issues=[]
    if len(actual)!=len(records):issues.append('Duplicate observation key')
    if expected!=actual:issues.append('Expected observation set differs')
    for r in records:
        folder=root/r['problem_id']/r['route']
        ext={'cpp':'cpp','haskell':'hs','prolog':'pl'}
        origin=(Path(cfg['corpus_root'])/r['problem_id']/('reference.'+ext[r['seed_language']])).read_text(encoding='utf-8')
        seen={(r['seed_language'],source_hash(origin)):0}
        previous=origin;all_functional=True;completed=0;derived_stop=None
        for item in r['steps']:
            step=folder/f'step-{item["step"]:02}'
            response=read_json(step/'response.json')
            if derived_stop is not None:issues.append('Translation continued after terminal outcome')
            if item.get('status')=='format_error':all_functional=False;derived_stop='format_error';continue
            source=(step/('source.'+ext[item['language']])).read_text(encoding='utf-8')
            extracted=extract_single_file_source_text(response['body']['choices'][0]['message']['content'],preserve_unfenced=True)
            if source_hash(extracted)!=source_hash(source):issues.append('Saved source differs from received response')
            key=(item['language'],source_hash(source))
            first=seen.setdefault(key,item['step'])
            if (len(seen)!=item['fps_size'] or first!=item['first_seen_step'] or
                source_hash(source)!=item['source_sha256'] or item['duplicate']!=(first!=item['step'])):
                issues.append(f'{r["problem_id"]}/{r["route"]}: invalid state accounting')
            evaluation=read_json(step/'evaluation/evaluation.json')
            all_functional &= evaluation['status']=='success'
            restored=item['language']==r['seed_language']
            if evaluation['status']=='success' and restored:completed+=1
            if evaluation['status']!='success':derived_stop=evaluation['status']
            elif len(seen)>cfg['max_fps_size']:derived_stop='max_distance_reached'
            elif restored and item['sym_adj'] is None:derived_stop='similarity_unavailable'
            elif restored and item['sym_adj']>=cfg['threshold']:derived_stop='success'
            elif item['step']>=cfg['max_translation_steps']:derived_stop='translation_budget_reached'
            if item.get('termination')!=derived_stop:issues.append('Step termination disagrees with protocol')
            if evaluation['status']=='success' and (len(evaluation['cases'])!=13 or any(c['status']!='success' for c in evaluation['cases'])):
                issues.append('Incomplete successful functionality check')
            if evaluation['contract']['source']!=digest(source.encode('utf-8')):issues.append('Evaluation source mismatch')
            for case in evaluation['cases']:
                expected=(Path(cfg['corpus_root'])/r['problem_id']/'evaluation'/(case['case']+'.out')).read_text(encoding='utf-8')
                derived=('timeout' if case['timed_out'] else 'runtime_error' if case['exit_code']!=0 else
                         'success' if canonical_output(case['stdout'])==canonical_output(expected) else 'wrong_answer')
                if derived!=case['status']:issues.append('Case status differs from recorded program output')
            if item['language']==r['seed_language'] and item['sym_adj'] is not None:
                for name,left in [('sym_adj',previous),('sym_origin',origin)]:
                    m=read_json(step/name/'measurement.json')
                    if (m['contract']['seed_sha256']!=digest(left.encode('utf-8')) or
                        m['contract']['candidate_sha256']!=digest(source.encode('utf-8')) or m['value']!=item[name]):
                        issues.append('Similarity source/value mismatch')
                    with (step/name/'result/results.csv').open(encoding='utf-8-sig',newline='') as stream:
                        raw=list(csv.DictReader(stream))
                    if len(raw)!=1 or float(raw[0]['averageSimilarity'])!=m['value']:
                        issues.append('Similarity differs from raw JPlag CSV')
                previous=source
        if len(seen)!=r['fps_size_at_stop']:issues.append('Final FPS mismatch')
        states=[{'language':k[0],'sha256':k[1],'first_seen_step':v} for k,v in seen.items()]
        if states!=r['states']:issues.append('Final state list mismatch')
        if completed!=r['completed_roundtrips']:issues.append('Completed roundtrip count mismatch')
        if r['evaluable'] and derived_stop!=r['status']:issues.append('Final stop differs from derived protocol outcome')
        if r['success']!=(r['status']=='success'):issues.append('Success flag mismatch')
        if r['fps_limit_exceeded']!=(len(seen)>cfg['max_fps_size']):issues.append('FPS limit flag mismatch')
        if r['evaluable'] and all_functional!=r['functional']:issues.append('Functional indicator mismatch')
        if r['success']:
            if not (all_functional and len(seen)<=cfg['max_fps_size'] and r['sym_adj']>=cfg['threshold'] and r['d_n']==len(seen)):
                issues.append('Invalid successful observation')
        elif r['d_n'] is not None or r['sym_final'] is not None:issues.append('Failure has success-conditional values')
    return {'at':max((r['at'] for r in records),default=None),'expected':len(expected),'observed':len(records),'all_evaluable':all(r['evaluable'] for r in records),
            'passed':not issues and all(r['evaluable'] for r in records),'issues':issues,
            'observation_files_sha256':{str(p.relative_to(root)):digest(p.read_bytes()) for p in root.glob('*/*/observation.json')}}

def figures(records,summary,folder):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    routes=list(summary['routes']);labels=[r.replace('cpp','C++').replace('haskell','Haskell').replace('prolog','Prolog').replace('-via-',' via ') for r in routes]
    fig,axs=plt.subplots(2,2,figsize=(12,8))
    for i,route in enumerate(routes):
        s=summary['routes'][route]
        if s['p_sf'] is not None:
            ci=s['wilson95'];p=s['p_sf']
            axs[0,0].errorbar(i,p,yerr=[[max(0,p-ci[0])],[max(0,ci[1]-p)]],fmt='o',capsize=4,color='tab:blue')
        rr=[r for r in records if r['route']==route and r['success']]
        for ax,key in [(axs[0,1],'d_n'),(axs[1,0],'sym_final')]:
            if rr:ax.scatter([i]*len(rr),[r[key] for r in rr],alpha=.6)
        for r in records:
            if r['route']==route:
                points=[(x['step']//2,x['sym_adj']) for x in r['steps'] if x.get('sym_adj') is not None]
                if points:axs[1,1].plot(*zip(*points),alpha=.45,marker='.',label=labels[i] if not axs[1,1].lines else None)
    for ax in [axs[0,0],axs[0,1],axs[1,0]]:
        ax.set_xticks(range(6),labels,rotation=28,ha='right');ax.grid(axis='y',alpha=.2)
    axs[0,0].set(ylabel='P_sf (Wilson 95% interval)',ylim=(-.05,1.05))
    axs[0,1].set(ylabel='Successful FPS size d_n',ylim=(1,11))
    axs[1,0].set(ylabel='Successful similarity to origin',ylim=(-.05,1.05))
    axs[1,1].set(xlabel='Completed round trip',ylabel='Adjacent restored similarity',ylim=(-.05,1.05))
    axs[1,1].axhline(.85,color='black',linestyle='--',linewidth=1)
    fig.tight_layout();fig.savefig(folder/'distributions.png',dpi=180);fig.savefig(folder/'distributions.pdf');plt.close(fig)

def report(cfg,phase):
    root=Path(cfg['output_root'])/phase
    records=[read_json(p) for p in sorted(root.glob('*/*/observation.json'))]
    ids=cfg['pilot_problem_ids'] if phase=='pilot' else cfg['problem_ids']
    args=cfg['analysis'];summary=summarize(records,ids,args['bootstrap_replicates'],args['bootstrap_seed'])
    if phase=='main':
        summary['excluding_pilot_problems']=summarize(records,[i for i in ids if i not in cfg['pilot_problem_ids']],args['bootstrap_replicates'],args['bootstrap_seed'])
        selection=read_json(Path(cfg['corpus_root'])/'selection.json')['problems']
        groups={p['group'] for p in selection}
        summary['by_problem_group']={group:summarize(records,[p['problem_id'] for p in selection if p['group']==group],
                   args['bootstrap_replicates'],args['bootstrap_seed']) for group in sorted(groups)}
    summary.update(phase=phase,at=max((r['at'] for r in records),default=None),planned=len(ids)*6,recorded=len(records),model=cfg['llm']['model'])
    verification=audit(cfg,phase,records)
    summary['complete']=verification['passed']
    write_json(root/'completion_audit.json',verification)
    write_json(root/'summary.json',summary)
    fields=['problem_id','route','status','evaluable','success','functional','d_n','fps_size_at_stop','sym_adj','sym_final','completed_roundtrips','translation_steps']
    with (root/'observations.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        for r in records:writer.writerow({k:r[k] for k in fields})
    def val(x):return 'NA' if x is None else f'{x:.3f}'
    lines=['# FPS 실험 결과', '',f'모델: {summary["model"]}; 단계: {phase}; 계획 {len(ids)*6}, 기록 {len(records)}; 감사 통과 {verification["passed"]}.','',
           '| 경로 | 성공/평가 | P_sf [Wilson 95%] | P_functional | d_n 중앙값 [Q1,Q3] | Sym_final 중앙값 |',
           '| --- | --- | --- | --- | --- | --- |']
    for route,s in summary['routes'].items():
        ci=s['wilson95'];d=s['d_n'];ci_text='NA' if ci is None else ','.join(val(v) for v in ci)
        lines.append(f'| {route} | {s["success"]}/{s["evaluable"]} | {val(s["p_sf"])} [{ci_text}] | {val(s["p_functional"])} | {val(d["median"])} [{val(d["q1"])},{val(d["q3"])}] | {val(s["sym_final"]["median"])} |')
    lines+=['','성공 조건부 값에는 실패를 0 또는 상한값으로 대입하지 않는다. bootstrap은 문제 단위 재표집이며 R=1의 실행 변동성을 추정하지 않는다.',
            '전체 분모·상태·미평가·미완료·대응 비교·퇴화 구간·예비 문제 제외 분석은 summary.json을 따른다.','',
            '| 경로 | 계획 | 성공 | 평가 실패 | 미평가 | 미완료 |', '| --- | ---: | ---: | ---: | ---: | ---: |']
    for route,s in summary['routes'].items():
        lines.append(f'| {route} | {s["planned"]} | {s["success"]} | {s["evaluation_failure"]} | {s["unevaluated"]} | {s["incomplete"]} |')
    (root/'summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    figures(records,summary,root)
    print('Report:',root/'summary.md','Audit:',verification['passed'])
    return summary
