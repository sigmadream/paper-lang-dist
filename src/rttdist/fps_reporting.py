"""Rebuild FPS v2 tables, intervals, paired comparisons and figures without model calls.

Aggregation follows v1/abs_PLAN.md 3.2: the problem is the sampling unit,
route P_sf is the equal-weight mean of per-problem rates, d_n is pooled over
successful attempts, and intervals come from problem-level bootstrap.
"""
from collections import Counter
import csv
from itertools import combinations
import json
import math
from pathlib import Path

import numpy as np

from rttdist.experiment_io import read_json, write_json, timestamp, digest
from rttdist.fps_state import source_hash, threshold_key, FUNCTIONAL_FAILURES
from rttdist.fps_execution import canonical_output, EXTENSIONS
from rttdist.extract import extract_single_file_source_text

PENALTY=11
CATEGORIES=['success','functional_failure','fps_limit','budget','invalid']

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

def outcome(record,key):
    return record['outcomes'][key]

def route_summary(records,ids,route,key,draws,repeats):
    per_problem={}
    for pid in ids:
        rs=[r for r in records if r['route']==route and r['problem_id']==pid]
        outs=[outcome(r,key) for r in rs]
        valid=[o for o in outs if o['category']!='invalid']
        ok=[o for o in valid if o['success']]
        per_problem[pid]={'recorded':len(rs),'valid':len(valid),'success':len(ok),
                          'p_sf':len(ok)/len(valid) if valid else None,
                          'd_n':[o['d_n'] for o in ok],
                          'd_n_mean':float(np.mean([o['d_n'] for o in ok])) if ok else None,
                          'd_plus':(sum(o['d_n'] for o in ok)+PENALTY*(len(valid)-len(ok)))/len(valid) if valid else None}
    rate_by_id={pid:p['p_sf'] for pid,p in per_problem.items() if p['p_sf'] is not None}
    rates=list(rate_by_id.values())
    bs=[]
    for sample in draws:
        vals=[rate_by_id[ids[i]] for i in sample if ids[i] in rate_by_id]
        if vals:bs.append(float(np.mean(vals)))
    all_d=[d for p in per_problem.values() for d in p['d_n']]
    dplus=[p['d_plus'] for p in per_problem.values() if p['d_plus'] is not None]
    routed=[r for r in records if r['route']==route and r['problem_id'] in ids]
    cats=Counter(outcome(r,key)['category'] for r in routed)
    valid_total=sum(p['valid'] for p in per_problem.values());success_total=sum(p['success'] for p in per_problem.values())
    return {'planned':len(ids)*repeats,'recorded':len(routed),'incomplete':len(ids)*repeats-len(routed),
            'valid':valid_total,'success':success_total,'invalid':cats.get('invalid',0),
            'categories':{c:cats.get(c,0) for c in CATEGORIES},'statuses':dict(Counter(r['status'] for r in routed)),
            'p_sf':float(np.mean(rates)) if rates else None,'p_sf_problems':len(rates),
            'p_sf_pooled':success_total/valid_total if valid_total else None,'wilson95_pooled':wilson(success_total,valid_total),
            'bootstrap95':np.quantile(bs,[.025,.975]).tolist() if bs else None,'bootstrap_degenerate':len(set(bs))==1 if bs else None,
            'd_n':distribution(all_d),'d_n_problems':sum(1 for p in per_problem.values() if p['d_n']),
            'd_plus':float(np.mean(dplus)) if dplus else None,'d_plus_penalty':PENALTY,
            'fps_size_at_stop_failures':distribution([r['fps_size_at_stop'] for r in routed if not outcome(r,key)['success']]),
            'duplicate_steps':sum(r.get('duplicate_steps',0) for r in routed),
            'translation_steps':sum(r['translation_steps'] for r in routed),
            'cost_usd':sum(r['cost_usd'] for r in routed if r.get('cost_usd') is not None) if any(r.get('cost_usd') is not None for r in routed) else None,
            'per_problem':per_problem}

def ranking(routes_summary):
    by_p=sorted((r for r in routes_summary if routes_summary[r]['p_sf'] is not None),key=lambda r:-routes_summary[r]['p_sf'])
    by_d=sorted((r for r in routes_summary if routes_summary[r]['d_n']['mean'] is not None),key=lambda r:routes_summary[r]['d_n']['mean'])
    return {'p_sf_desc':by_p,'d_n_asc':by_d}

def paired(records,ids,pairs,key,draws,family):
    comparisons=[]
    for left,right in pairs:
        summaries={}
        for route in (left,right):
            per={}
            for pid in ids:
                outs=[outcome(r,key) for r in records if r['route']==route and r['problem_id']==pid]
                valid=[o for o in outs if o['category']!='invalid'];ok=[o for o in valid if o['success']]
                per[pid]={'p_sf':len(ok)/len(valid) if valid else None,'d_n':float(np.mean([o['d_n'] for o in ok])) if ok else None}
            summaries[route]=per
        for metric in ['p_sf','d_n']:
            values={pid:summaries[left][pid][metric]-summaries[right][pid][metric] for pid in ids
                    if summaries[left][pid][metric] is not None and summaries[right][pid][metric] is not None}
            common=sorted(values)
            boot=[]
            for sample in draws:
                ds=[values[ids[i]] for i in sample if ids[i] in values]
                if ds:boot.append(float(np.mean(ds)))
            left_common=[summaries[left][p][metric] for p in common];right_common=[summaries[right][p][metric] for p in common]
            comparisons.append({'left':left,'right':right,'metric':metric,'common_n':len(common),'common_problem_ids':common,
                'left_mean_common':float(np.mean(left_common)) if common else None,'right_mean_common':float(np.mean(right_common)) if common else None,
                'mean_difference':float(np.mean(list(values.values()))) if values else None,
                'bootstrap95':np.quantile(boot,[.025,.975]).tolist() if boot else None,
                'bonferroni95':np.quantile(boot,[.025/family,1-.025/family]).tolist() if boot else None,'family':family,
                'bootstrap_valid_replicates':len(boot),'bootstrap_degenerate':len(set(boot))==1 if boot else None,
                'unavailable_reason':None if values else 'No common problems with the metric defined on both routes'})
    return comparisons

def default_pairs(routes):
    names=[a+'-via-'+b for a,b in routes]
    pairs=[]
    for a,b in combinations(sorted({l for r in routes for l in r}),2):
        left=a+'-via-'+b;right=b+'-via-'+a
        if left in names and right in names:pairs.append([left,right])
    return pairs

def summarize(records,ids,replicates,seed,routes,repeats,thresholds,primary,pairs=None):
    rng=np.random.default_rng(seed)
    draws=rng.integers(0,len(ids),size=(replicates,len(ids))) if ids else np.zeros((0,0),dtype=int)
    names=[a+'-via-'+b for a,b in routes]
    keys=[threshold_key(v) for v in thresholds];pkey=threshold_key(primary)
    pairs=[list(p) for p in (pairs or default_pairs(routes))]
    family=max(1,len(pairs))
    by_threshold={k:{route:route_summary(records,ids,route,k,draws,repeats) for route in names} for k in keys}
    result={'primary_threshold':pkey,'thresholds':keys,'routes':by_threshold[pkey],'ranking':ranking(by_threshold[pkey]),
            'paired_comparisons':paired(records,ids,pairs,pkey,draws,family),
            'by_threshold':{k:{'routes':by_threshold[k],'ranking':ranking(by_threshold[k])} for k in keys}}
    result['ranking_stable_across_thresholds']={m:len({tuple(result['by_threshold'][k]['ranking'][m]) for k in keys})==1 for m in ('p_sf_desc','d_n_asc')}
    return result

def audit(cfg,phase,records):
    root=Path(cfg['output_root'])/phase
    ids=cfg['pilot_problem_ids'] if phase=='pilot' else cfg['problem_ids']
    keys=[threshold_key(v) for v in cfg['thresholds']];top=cfg['thresholds'][-1];pkey=threshold_key(cfg['threshold'])
    expected={(p,a+'-via-'+b,n) for p in ids for a,b in cfg['routes'] for n in range(1,cfg['repeats']+1)}
    actual={(r['problem_id'],r['route'],r['attempt']) for r in records}
    issues=[]
    if len(actual)!=len(records):issues.append('Duplicate observation key')
    if expected!=actual:issues.append('Expected observation set differs')
    for r in records:
        folder=root/r['problem_id']/r['route']/f'attempt-{r["attempt"]:02}'
        problem=Path(cfg['corpus_root'])/r['problem_id']
        case_count=len(list((problem/'evaluation').glob('*.inp')))
        origin=(problem/('reference.'+EXTENSIONS[r['seed_language']])).read_text(encoding='utf-8')
        seen={(r['seed_language'],source_hash(origin)):0}
        previous=origin;all_functional=True;completed=0;derived_stop=None;reached={};unavailable=0;measured_any=False
        for item in r['steps']:
            step=folder/f'step-{item["step"]:02}'
            if derived_stop is not None:issues.append('Translation continued after terminal outcome')
            if item.get('status')=='format_error':all_functional=False;derived_stop='format_error';continue
            if item.get('reason')=='unexpected_response_model':derived_stop='infrastructure_error';continue
            response=read_json(step/'response.json')
            source=(step/('source.'+EXTENSIONS[item['language']])).read_text(encoding='utf-8')
            extracted=extract_single_file_source_text(response['body']['choices'][0]['message']['content'],preserve_unfenced=True)
            if source_hash(extracted)!=source_hash(source):issues.append('Saved source differs from received response')
            key=(item['language'],source_hash(source))
            first=seen.setdefault(key,item['step'])
            if (len(seen)!=item['fps_size'] or first!=item['first_seen_step'] or
                source_hash(source)!=item['source_sha256'] or item['duplicate']!=(first!=item['step'])):
                issues.append(f'{r["problem_id"]}/{r["route"]}/{r["attempt"]}: invalid state accounting')
            evaluation=read_json(step/'evaluation/evaluation.json')
            all_functional &= evaluation['status']=='success'
            restored=item['language']==r['seed_language']
            if evaluation['status']=='success' and restored:completed+=1
            if evaluation['status']!='success':derived_stop=evaluation['status']
            elif len(seen)>cfg['max_fps_size']:derived_stop='max_distance_reached'
            else:
                if restored:
                    if item['sym_adj'] is None:unavailable+=1
                    else:
                        measured_any=True
                        for value in cfg['thresholds']:
                            k=threshold_key(value)
                            if k not in reached and item['sym_adj']>=value:reached[k]={'step':item['step'],'fps_size':len(seen),'sym_adj':item['sym_adj']}
                        if threshold_key(top) in reached:derived_stop='collection_complete'
                if derived_stop is None and item['step']>=cfg['max_translation_steps']:derived_stop='translation_budget_reached'
            if item.get('termination')!=derived_stop:issues.append('Step termination disagrees with protocol')
            if evaluation['status']=='success' and (len(evaluation['cases'])!=case_count or any(c['status']!='success' for c in evaluation['cases'])):
                issues.append('Incomplete successful functionality check')
            if evaluation['contract']['source']!=digest(source.encode('utf-8')):issues.append('Evaluation source mismatch')
            for case in evaluation['cases']:
                expected_out=(problem/'evaluation'/(case['case']+'.out')).read_text(encoding='utf-8')
                derived=('timeout' if case['timed_out'] else 'runtime_error' if case['exit_code']!=0 else
                         'success' if canonical_output(case['stdout'])==canonical_output(expected_out) else 'wrong_answer')
                if derived!=case['status']:issues.append('Case status differs from recorded program output')
            if restored and evaluation['status']=='success':
                for name,left in [('sym_adj',previous),('sym_origin',origin)]:
                    if item.get(name) is None:continue
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
        if unavailable!=r['similarity_unavailable_steps']:issues.append('Similarity-unavailable count mismatch')
        if r['status'] not in ('infrastructure_error',None) and derived_stop!=r['status']:issues.append('Final stop differs from derived protocol outcome')
        if r['fps_limit_exceeded']!=(len(seen)>cfg['max_fps_size']):issues.append('FPS limit flag mismatch')
        if r['evaluable'] and all_functional!=r['functional']:issues.append('Functional indicator mismatch')
        invalid_by_similarity=not measured_any and unavailable>0 and r['status'] in ('translation_budget_reached','max_distance_reached')
        for k in keys:
            o=r['outcomes'].get(k)
            if o is None:issues.append(f'Missing outcome for threshold {k}');continue
            hit=reached.get(k)
            if bool(hit)!=o['success']:issues.append(f'Threshold {k} success flag disagrees with reach record')
            if hit and (o['d_n']!=hit['fps_size'] or o['reached_step']!=hit['step'] or o['sym_adj']!=hit['sym_adj'] or hit['fps_size']>cfg['max_fps_size']):
                issues.append(f'Threshold {k} success values disagree with reach record')
            if not hit:
                if o['d_n'] is not None or o['reached_step'] is not None:issues.append('Failure has success-conditional values')
                derived_cat=('invalid' if r['status'] in ('infrastructure_error',None) or invalid_by_similarity else
                             'functional_failure' if r['status'] in FUNCTIONAL_FAILURES else
                             'fps_limit' if r['status']=='max_distance_reached' else
                             'budget' if r['status']=='translation_budget_reached' else 'invalid')
                if o['category']!=derived_cat:issues.append(f'Threshold {k} category {o["category"]} differs from derived {derived_cat}')
        p=r['outcomes'].get(pkey,{})
        if (r['success'],r['d_n'],r['category'])!=(p.get('success'),p.get('d_n'),p.get('category')):issues.append('Primary fields differ from primary outcome')
        if r['evaluable']!=(r['category']!='invalid'):issues.append('Evaluable flag mismatch')
    return {'at':max((r['at'] for r in records),default=None),'expected':len(expected),'observed':len(records),'all_evaluable':all(r['evaluable'] for r in records),
            'passed':not issues and all(r['evaluable'] for r in records),'issues':issues,
            'observation_files_sha256':{str(p.relative_to(root)):digest(p.read_bytes()) for p in root.glob('*/*/attempt-*/observation.json')}}

def figures(records,summary,folder,thresholds):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    routes=list(summary['routes']);labels=[r.replace('-via-',' via ') for r in routes]
    fig,axs=plt.subplots(2,2,figsize=(13,9))
    for i,route in enumerate(routes):
        s=summary['routes'][route]
        if s['p_sf'] is not None:
            ci=s['bootstrap95'] or [s['p_sf'],s['p_sf']];p=s['p_sf']
            axs[0,0].errorbar(i,p,yerr=[[max(0,p-ci[0])],[max(0,ci[1]-p)]],fmt='o',capsize=4,color='tab:blue')
        rr=[r for r in records if r['route']==route and r['success']]
        if rr:axs[0,1].scatter([i]*len(rr),[r['d_n'] for r in rr],alpha=.5)
        ps=[summary['by_threshold'][k]['routes'][route]['p_sf'] for k in thresholds]
        axs[1,0].plot(thresholds,[np.nan if v is None else v for v in ps],marker='o',label=labels[i])
        for r in records:
            if r['route']==route:
                points=[(x['step']//2,x['sym_adj']) for x in r['steps'] if x.get('sym_adj') is not None]
                if points:axs[1,1].plot(*zip(*points),alpha=.35,marker='.',color=f'C{i}')
    for ax in [axs[0,0],axs[0,1]]:
        ax.set_xticks(range(len(routes)),labels,rotation=28,ha='right');ax.grid(axis='y',alpha=.2)
    axs[0,0].set(ylabel='P_sf (problem-level bootstrap 95%)',ylim=(-.05,1.05))
    axs[0,1].set(ylabel='Successful FPS size d_n',ylim=(1,11))
    axs[1,0].set(xlabel='Threshold',ylabel='P_sf by threshold',ylim=(-.05,1.05));axs[1,0].legend(fontsize=7)
    axs[1,1].set(xlabel='Completed round trip',ylabel='Adjacent restored similarity',ylim=(-.05,1.05))
    for value in thresholds:axs[1,1].axhline(float(value),color='black',linestyle='--',linewidth=.8)
    fig.tight_layout();fig.savefig(folder/'distributions.png',dpi=180);fig.savefig(folder/'distributions.pdf');plt.close(fig)

def read_ledger(folder):
    """Totals over the unsharded ledger and every shard ledger (cost_ledger-ikk.jsonl)."""
    paths=sorted(Path(folder).glob('cost_ledger*.jsonl'))
    if not paths:return None
    entries=[json.loads(l) for path in paths for l in path.read_text(encoding='utf-8').splitlines() if l.strip()]
    return {'calls':len(entries),'total_cost_usd':sum(e['cost_usd'] for e in entries),
            'prompt_tokens':sum((e['usage'] or {}).get('prompt_tokens') or 0 for e in entries),
            'completion_tokens':sum((e['usage'] or {}).get('completion_tokens') or 0 for e in entries)}

def report(cfg,phase):
    root=Path(cfg['output_root'])/phase
    records=[read_json(p) for p in sorted(root.glob('*/*/attempt-*/observation.json'))]
    ids=cfg['pilot_problem_ids'] if phase=='pilot' else cfg['problem_ids']
    args=cfg['analysis'];pairs=args.get('comparison_pairs')
    def run(subset):return summarize(records,subset,args['bootstrap_replicates'],args['bootstrap_seed'],cfg['routes'],cfg['repeats'],cfg['thresholds'],cfg['threshold'],pairs)
    summary=run(ids)
    if phase=='main':
        summary['excluding_pilot_problems']=run([i for i in ids if i not in cfg.get('pilot_problem_ids',[])])
        selection=read_json(Path(cfg['corpus_root'])/'selection.json')['problems']
        groups={p.get('group') for p in selection}-{None}
        if groups:summary['by_problem_group']={g:run([p['problem_id'] for p in selection if p.get('group')==g and p['problem_id'] in ids]) for g in sorted(groups)}
    planned=len(ids)*len(cfg['routes'])*cfg['repeats']
    summary.update(phase=phase,at=max((r['at'] for r in records),default=None),planned=planned,recorded=len(records),
                   model=cfg['llm']['model'],repeats=cfg['repeats'],cost=read_ledger(root))
    verification=audit(cfg,phase,records)
    summary['complete']=verification['passed'] and len(records)==planned
    write_json(root/'completion_audit.json',verification)
    write_json(root/'summary.json',summary)
    fields=['problem_id','route','attempt','seed','status','reason','category','evaluable','success','d_n','reached_step','sym_adj','sym_origin_at_reach',
            'functional','fps_size_at_stop','similarity_unavailable_steps','completed_roundtrips','translation_steps','duplicate_steps','cost_usd']
    with (root/'observations.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader()
        for r in records:writer.writerow({k:r.get(k) for k in fields})
    def val(x):return 'NA' if x is None else f'{x:.3f}'
    def ci(x):return 'NA' if x is None else ','.join(val(v) for v in x)
    cost=summary['cost'];cost_text='NA' if not cost else f'{cost["total_cost_usd"]:.4f} USD, {cost["calls"]} calls'
    lines=['# FPS 실험 결과 (v2)','',f'모델: {summary["model"]}; 단계: {phase}; 주 임계값 {summary["primary_threshold"]}; N={cfg["repeats"]}; 계획 {planned}, 기록 {len(records)}; 감사 통과 {verification["passed"]}; 비용 {cost_text}.','',
           '## 주 지표','','| 경로 | 성공/유효 | P_sf 문제 평균 [부트스트랩 95%] | P_sf 합산 | d_n 평균 (n, 문제 수) | d_n 중앙값 [Q1,Q3] | d+ (벌점 11) |',
           '| --- | --- | --- | --- | --- | --- | --- |']
    for route,s in summary['routes'].items():
        d=s['d_n']
        lines.append(f'| {route} | {s["success"]}/{s["valid"]} | {val(s["p_sf"])} [{ci(s["bootstrap95"])}] | {val(s["p_sf_pooled"])} | {val(d["mean"])} ({d["n"]}, {s["d_n_problems"]}) | {val(d["median"])} [{val(d["q1"])},{val(d["q3"])}] | {val(s["d_plus"])} |')
    lines+=['','## 진단 정보','','| 경로 | 계획 | 기록 | 성공 | 기능 실패 | 상한 초과 | 예산 소진 | 무효 | 실패 시도 FPS 중앙값 | 상태 재등장 단계 | 편도 번역 수 |','| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for route,s in summary['routes'].items():
        c=s['categories']
        lines.append(f'| {route} | {s["planned"]} | {s["recorded"]} | {c["success"]} | {c["functional_failure"]} | {c["fps_limit"]} | {c["budget"]} | {c["invalid"]} | {val(s["fps_size_at_stop_failures"]["median"])} | {s["duplicate_steps"]} | {s["translation_steps"]} |')
    lines+=['','## 임계값별 결과','','| 임계값 | '+' | '.join(summary['routes'])+' |','| --- | '+' | '.join('---' for _ in summary['routes'])+' |']
    for k in summary['thresholds']:
        rs=summary['by_threshold'][k]['routes']
        lines.append(f'| {k} P_sf | '+' | '.join(val(rs[r]['p_sf']) for r in rs)+' |')
        lines.append(f'| {k} d_n 평균 | '+' | '.join(val(rs[r]['d_n']['mean']) for r in rs)+' |')
    stable=summary['ranking_stable_across_thresholds']
    lines+=['',f'경로 순위 유지: P_sf {stable["p_sf_desc"]}, d_n {stable["d_n_asc"]}.','','## 대응 비교 (공통 문제)','',
            '| 왼쪽 | 오른쪽 | 지표 | 공통 문제 수 | 왼쪽 평균 | 오른쪽 평균 | 차이 | 부트스트랩 95% | Bonferroni 95% |','| --- | --- | --- | ---: | --- | --- | --- | --- | --- |']
    for c in summary['paired_comparisons']:
        lines.append(f'| {c["left"]} | {c["right"]} | {c["metric"]} | {c["common_n"]} | {val(c["left_mean_common"])} | {val(c["right_mean_common"])} | {val(c["mean_difference"])} | [{ci(c["bootstrap95"])}] | [{ci(c["bonferroni95"])}] |')
    lines+=['','성공 조건부 d_n에는 실패를 대입하지 않는다. d+는 실패 시도에 벌점 11을 준 보조 점수다. 구간은 문제 단위 부트스트랩이며 문제별 P_sf의 동일 가중 평균을 재표집한다.',
            '전체 분모, 무효 사유, 임계값별 세부, 예비 문제 제외 분석은 summary.json을 따른다.']
    (root/'summary.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    figures(records,summary,root,summary['thresholds'])
    print('Report:',root/'summary.md','Audit:',verification['passed'])
    return summary
