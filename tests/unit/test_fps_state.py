from rttdist.fps_state import FPSState, source_hash
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
    assert s.decide('success',True,.85)=='success'
    assert len(s.states)==expected

def test_duplicates_and_cycles():
    s=FPSState('cpp','A',max_translation_steps=6)
    for language,source in [('prolog','B'),('cpp','A1'),('prolog','B'),('cpp','A1')]:s.add(language,source)
    assert len(s.states)==3
    assert s.history[-1]['first_seen_step']==2
    assert s.decide('success',True,.85)=='success'

@pytest.mark.parametrize('score,expected',[(.849999,None),(.85,'success'),(.850001,'success')])
def test_threshold_uses_unrounded_adjacent(score,expected):
    s=FPSState('cpp','A');s.add('prolog','B');s.add('cpp','A1')
    assert s.decide('success',True,score)==expected

def test_failure_overrides_similarity_and_distance():
    s=FPSState('cpp','A',max_fps_size=2);s.add('prolog','B');s.add('cpp','A1')
    assert s.decide('wrong_answer',True,1)=='wrong_answer'

def test_fps_ten_and_eleven_boundaries():
    s=FPSState('cpp','A')
    for i in range(9):s.add('prolog',str(i))
    assert s.decide('success',False) is None
    assert s.decide('success',True,.85)=='success'
    s.add('prolog','new')
    assert s.decide('success',False)=='max_distance_reached'
    assert s.decide('success',True,1)=='max_distance_reached'

def test_budget_without_fps_growth_and_missing_similarity():
    s=FPSState('cpp','A',max_translation_steps=4)
    for _ in range(2):s.add('prolog','B');s.add('cpp','A')
    assert len(s.states)==2
    assert s.decide('success',True,.2)=='translation_budget_reached'
    assert s.all_functional
    assert s.decide('success',True,None,False)=='similarity_unavailable'

def test_ten_can_repeat_below_threshold_without_incrementing():
    s=FPSState('cpp','A')
    for i in range(9):s.add('prolog',str(i))
    s.add('cpp','A')
    assert s.decide('success',True,.3) is None
    assert len(s.states)==10
    s.add('prolog','0')
    assert s.decide('success',False) is None and len(s.states)==10
