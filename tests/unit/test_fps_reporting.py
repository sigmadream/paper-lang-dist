import pytest
from rttdist.fps_reporting import summarize,wilson,distribution

def test_zero_success_has_uncertainty_and_no_conditional_distance():
    records=[{'problem_id':str(i),'route':'cpp-via-prolog','evaluable':True,'success':False,
              'functional':True,'status':'max_distance_reached','d_n':None,'sym_final':None,'sym_adj':None} for i in range(15)]
    result=summarize(records,[str(i) for i in range(15)],2000,42)
    s=result['routes']['cpp-via-prolog']
    assert s['p_sf']==0 and s['p_functional']==1
    assert s['wilson95'][1]>.2
    assert s['bootstrap_degenerate'] and s['bootstrap95']==[0,0]
    assert s['d_n']['n']==0 and s['d_n']['median'] is None
    assert s['planned']==s['success']+s['evaluation_failure']+s['unevaluated']+s['incomplete']

def test_missing_is_not_an_observed_failure():
    result=summarize([],['p'],20,42)
    s=result['routes']['cpp-via-haskell']
    assert s['p_sf'] is None and s['incomplete']==1 and s['evaluation_failure']==0
    assert all(c['common_n']==0 and c['mean_difference'] is None for c in result['paired_comparisons'])
