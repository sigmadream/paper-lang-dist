from rttdist.fps_state import FPSState, source_hash, category
import pytest

def test_identity_is_exact_except_line_endings():
    assert source_hash('a\r\nb\r')==source_hash('a\nb\n')
    assert source_hash('a b')!=source_hash('a  b')
    assert source_hash('a')!=source_hash('a\n')
    s=FPSState('cpp','same');s.add('prolog','same')
    assert len(s.states)==2

@pytest.mark.parametrize('restored,expected',[('A',2),('A1',3)])
def test_first_roundtrip_distance(restored,expected):
    s=FPSState('cpp','A');s.add('prolog','B');s.add('cpp',restored)
    assert s.decide('success',True,.85)=='collection_complete'
    o=s.outcome('collection_complete')
    assert o['success'] and o['d_n']==expected==len(s.states) and o['reached_step']==2

def test_duplicates_and_cycles():
    s=FPSState('cpp','A',max_translation_steps=6)
    for language,source in [('prolog','B'),('cpp','A1'),('prolog','B'),('cpp','A1')]:s.add(language,source)
    assert len(s.states)==3
    assert s.history[-1]['first_seen_step']==2
    assert s.decide('success',True,.85)=='collection_complete'
    assert s.outcome('collection_complete')['d_n']==3 and s.reached['0.85']['step']==4

@pytest.mark.parametrize('score,expected',[(.849999,None),(.85,'collection_complete'),(.850001,'collection_complete')])
def test_threshold_uses_unrounded_adjacent(score,expected):
    s=FPSState('cpp','A');s.add('prolog','B');s.add('cpp','A1')
    assert s.decide('success',True,score)==expected

def test_failure_overrides_similarity_and_distance():
    s=FPSState('cpp','A',max_fps_size=2);s.add('prolog','B');s.add('cpp','A1')
    assert s.decide('wrong_answer',True,1)=='wrong_answer'
    o=s.outcome('wrong_answer')
    assert o['category']=='functional_failure' and not o['success'] and o['d_n'] is None

def test_fps_ten_and_eleven_boundaries():
    s=FPSState('cpp','A')
    for i in range(9):s.add('prolog',str(i))
    assert s.decide('success',False) is None
    assert s.decide('success',True,.85)=='collection_complete'
    s.add('prolog','new')
    assert s.decide('success',False)=='max_distance_reached'
    assert s.decide('success',True,1)=='max_distance_reached'
    t=FPSState('cpp','A')
    for i in range(10):t.add('prolog',str(i))
    assert t.decide('success',True,1)=='max_distance_reached'
    assert t.outcome('max_distance_reached')['category']=='fps_limit'

def test_budget_without_fps_growth_and_missing_similarity_continues():
    s=FPSState('cpp','A',max_translation_steps=4)
    for _ in range(2):s.add('prolog','B');s.add('cpp','A')
    assert len(s.states)==2
    assert s.decide('success',True,.2)=='translation_budget_reached'
    assert s.all_functional and s.outcome('translation_budget_reached')['category']=='budget'
    t=FPSState('cpp','A');t.add('prolog','B');t.add('cpp','A1')
    assert t.decide('success',True,None,False) is None
    assert t.similarity_unavailable_steps==1 and not t.reached

def test_ten_can_repeat_below_threshold_without_incrementing():
    s=FPSState('cpp','A')
    for i in range(9):s.add('prolog',str(i))
    s.add('cpp','A')
    assert s.decide('success',True,.3) is None
    assert len(s.states)==10
    s.add('prolog','0')
    assert s.decide('success',False) is None and len(s.states)==10

def test_multiple_thresholds_continue_until_largest_and_primary_is_fixed():
    s=FPSState('cpp','A',threshold=.85,thresholds=[.8,.85,.9])
    assert s.thresholds==[.8,.85,.9]
    s.add('prolog','B');s.add('cpp','A1')
    assert s.decide('success',True,.86) is None
    assert set(s.reached)=={'0.80','0.85'} and s.reached['0.85']['fps_size']==3
    s.add('prolog','B2');s.add('cpp','A2')
    assert s.decide('wrong_answer',True,.95)=='wrong_answer'
    o=s.outcomes('wrong_answer')
    assert o['0.85']['success'] and o['0.85']['d_n']==3 and o['0.85']['reached_step']==2 and o['0.85']['sym_adj']==.86
    assert o['0.80']['success'] and o['0.90']['category']=='functional_failure' and o['0.90']['d_n'] is None

def test_largest_threshold_completes_collection():
    s=FPSState('cpp','A',thresholds=[.8,.85,.9]);s.add('prolog','B');s.add('cpp','A1')
    assert s.decide('success',True,.92)=='collection_complete'
    assert all(o['success'] and o['d_n']==3 for o in s.outcomes('collection_complete').values())

def test_category_mapping():
    assert category('compile_error')=='functional_failure' and category('format_error')=='functional_failure'
    assert category('max_distance_reached')=='fps_limit' and category('translation_budget_reached')=='budget'
    assert category('infrastructure_error')=='invalid' and category(None)=='invalid'
