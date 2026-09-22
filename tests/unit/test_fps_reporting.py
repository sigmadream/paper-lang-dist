import pytest
from rttdist.fps_reporting import summarize,wilson,distribution,PENALTY,default_pairs

ROUTES=[['cpp','haskell'],['cpp','prolog'],['haskell','cpp'],['haskell','prolog'],['prolog','cpp'],['prolog','haskell']]

def rec(pid,route,attempt,category,d_n=None,status='translation_budget_reached'):
    out={'category':category,'success':category=='success','d_n':d_n,'reached_step':2 if d_n else None,'reached_roundtrip':None,'sym_adj':None}
    return {'problem_id':pid,'route':route,'attempt':attempt,'status':status,'category':category,'success':out['success'],'d_n':d_n,
            'outcomes':{'0.85':out},'evaluable':category!='invalid','fps_size_at_stop':d_n or 11,'translation_steps':2,'duplicate_steps':0,
            'cost_usd':None,'at':'t','steps':[]}

def test_zero_success_has_uncertainty_and_no_conditional_distance():
    records=[rec(str(i),'cpp-via-prolog',n,'fps_limit',status='max_distance_reached') for i in range(15) for n in range(1,6)]
    r=summarize(records,[str(i) for i in range(15)],200,42,ROUTES,5,[.85],.85)
    s=r['routes']['cpp-via-prolog']
    assert s['p_sf']==0 and s['bootstrap_degenerate'] and s['bootstrap95']==[0,0]
    assert s['wilson95_pooled'][1]>0 and s['d_n']['n']==0 and s['d_plus']==PENALTY
    assert s['planned']==75==s['recorded']==s['categories']['fps_limit'] and s['incomplete']==0

def test_equal_weight_problem_mean_differs_from_pooled_with_invalid():
    records=[rec('a','cpp-via-haskell',1,'success',3)]+[rec('a','cpp-via-haskell',n,'invalid',status='infrastructure_error') for n in range(2,6)]
    records+=[rec('b','cpp-via-haskell',n,'budget') for n in range(1,6)]
    r=summarize(records,['a','b'],100,1,ROUTES,5,[.85],.85)
    s=r['routes']['cpp-via-haskell']
    assert s['p_sf']==0.5 and s['p_sf_pooled']==pytest.approx(1/6) and s['invalid']==4 and s['valid']==6
    assert s['d_n']['mean']==3 and s['d_n_problems']==1
    assert s['d_plus']==pytest.approx((3+PENALTY)/2)
    assert s['per_problem']['a']['p_sf']==1 and s['per_problem']['b']['d_plus']==PENALTY

def test_missing_is_not_an_observed_failure():
    r=summarize([],['p'],20,42,ROUTES,5,[.85],.85)
    s=r['routes']['cpp-via-haskell']
    assert s['p_sf'] is None and s['incomplete']==5 and s['categories']['functional_failure']==0
    assert all(c['common_n']==0 and c['mean_difference'] is None for c in r['paired_comparisons'])

def test_paired_common_problems_and_threshold_ranking():
    records=[]
    for pid in 'abc':
        records.append(rec(pid,'cpp-via-haskell',1,'success',3))
        records.append(rec(pid,'haskell-via-cpp',1,'success',5))
    records[-1]=rec('c','haskell-via-cpp',1,'budget')
    r=summarize(records,list('abc'),50,3,ROUTES,1,[.85],.85)
    comp={(c['left'],c['right'],c['metric']):c for c in r['paired_comparisons']}
    d=comp[('cpp-via-haskell','haskell-via-cpp','d_n')]
    assert d['common_n']==2 and d['mean_difference']==-2 and d['left_mean_common']==3 and d['right_mean_common']==5
    p=comp[('cpp-via-haskell','haskell-via-cpp','p_sf')]
    assert p['common_n']==3 and p['mean_difference']==pytest.approx(1/3) and p['family']==3
    assert r['ranking']['p_sf_desc'][:2]==['cpp-via-haskell','haskell-via-cpp']
    assert r['ranking_stable_across_thresholds']=={'p_sf_desc':True,'d_n_asc':True}
    assert default_pairs([['cpp','python'],['cpp','haskell']])==[]

def test_wilson_and_distribution_edge_cases():
    assert wilson(0,0) is None and wilson(0,5)[0]==0
    assert distribution([None,None])['n']==0 and distribution([2,4])['mean']==3
