from rttdist.research.profiles import load_profile
from rttdist.research.policies import POLICIES
from rttdist.research.aggregation import aggregate


def step(index, source, score=.9, status='success'):
    return {'index': index, 'target_language': 'python' if index % 2 else 'cpp', 'source': source,
            'status': status, 'measurements': {'adjacent': {'status': 'measured', 'value': score}}}


def test_fps_state_count_is_distinct_from_hops_and_primary_survives_later_failure():
    cfg = load_profile('fps-v2')['execution']
    result = POLICIES['fps'].decide(cfg, 'A', 'cpp', [step(1, 'B'), step(2, 'A1', .86), step(3, 'bad', status='compile_error')])
    assert result['success'] and result['reached_step'] == 2 and result['unique_state_count'] == 3
    assert result['outcomes']['0.90']['category'] == 'functional_failure'


def test_strict_fixed_point_confirmation_and_oscillation():
    cfg = load_profile('strict-fixed-point-v1')['execution']
    cfg['confirmations'] = 1
    origin = 'int main(){return 0;}'
    decide = POLICIES['normalized_fixed_point'].decide
    steps = [step(1, 'B'), step(2, origin)]
    assert not decide(cfg, origin, 'cpp', steps)['terminal']
    assert decide(cfg, origin, 'cpp', steps + [step(3, 'B'), step(4, origin)])['success']
    assert decide(cfg, origin, 'cpp', steps + [step(3, 'B'), step(4, 'int main(){return 1;}')])['status'] == 'confirmation_failed'


def test_problem_weighting_and_invalid_denominators_are_explicit():
    def row(pid, success, category='success', hops=2):
        return {'model_id': 'm', 'route': ['cpp', 'python'], 'problem_id': pid, 'decision': {
            'terminal': True, 'category': category, 'status': category, 'success': success,
            'reached_step': hops if success else None, 'unique_state_count': 3 if success else None}}
    rows = [row('p', True), row('q', False, 'functional_failure'), row('q', False, 'functional_failure'), row('z', False, 'invalid')]
    config = {'aggregator': 'hop_distance', 'weighting': 'problem', 'bootstrap_samples': 30, 'seed': 1}
    result = aggregate(rows, config)[0]
    assert result['valid'] == 3 and result['success_rate'] == .5 and result['pooled_success_rate'] == 1 / 3
    assert result['hop_adjusted_distance'] == 4
    assert result['bootstrap95']['success_rate']['valid_replicates'] <= 30


def test_fps_analysis_can_select_only_collected_threshold_outcomes():
    cfg = load_profile('fps-v2')
    decision = POLICIES['fps'].decide(cfg['execution'], 'A', 'cpp', [step(1, 'B'), step(2, 'A1', .86), step(3, 'bad', status='compile_error')])
    rows = [{'model_id': 'm', 'route': ['cpp', 'python'], 'problem_id': 'p', 'decision': decision}]
    primary = aggregate(rows, cfg['analysis'])[0]
    upper = aggregate(rows, {**cfg['analysis'], 'outcome_threshold': .9})[0]
    assert primary['success_rate'] == 1 and primary['mean_unique_state_count'] == 3
    assert upper['success_rate'] == 0 and upper['mean_unique_state_count'] is None
    assert upper['penalized_state_distance'] == 11
