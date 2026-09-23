from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from rttdist.research.metrics import Metric, MetricContext, METRICS, measure, register_metric
from rttdist.research.policies import DecisionPolicy, POLICIES, register_policy
from rttdist.research.aggregation import Aggregator, AGGREGATORS, aggregate, register_aggregator
from rttdist.research.profiles import load_profile
from rttdist.research.store import exclusive_lock, StoreError


def test_metric_errors_are_observations_and_language_limits_are_explicit(tmp_path, monkeypatch):
    def broken(ctx, options):
        raise RuntimeError('plugin failure')
    monkeypatch.setitem(METRICS, 'broken', Metric('broken', '1', 'ratio', broken))
    context = MetricContext('x', 'y', 'cpp', tmp_path)
    result = measure({'id': 'broken', 'metric': 'broken'}, context)
    assert result['status'] == 'error' and result['reason'] == 'RuntimeError' and result['value'] is None
    other = MetricContext('x', 'y', 'python', tmp_path)
    assert measure({'id': 'tokens', 'metric': 'token_dice'}, other)['status'] == 'not_applicable'
    with pytest.raises(ValueError, match='registered'):
        register_metric(METRICS['broken'])


def test_custom_policy_and_aggregator_do_not_require_engine_edits(monkeypatch):
    policy = DecisionPolicy('custom', '3', lambda config: None, lambda config, origin, language, steps: {'terminal': False})
    monkeypatch.setitem(POLICIES, 'custom', policy)
    aggregate_fn = Aggregator('custom', '2', lambda rows, config: {'n': len(rows)})
    monkeypatch.setitem(AGGREGATORS, 'custom', aggregate_fn)
    profile = load_profile({'id': 'custom', 'version': 1, 'execution': {'policy': 'custom', 'max_steps': 4},
                            'analysis': {'aggregator': 'custom'}})
    assert profile['execution']['policy_version'] == '3'
    assert profile['analysis']['aggregator_version'] == '2'
    assert aggregate([{'model_id': 'm', 'route': ['cpp', 'python']}], profile['analysis'])[0]['n'] == 1


def test_nested_profile_paths_and_duplicate_yaml_keys(tmp_path):
    from rttdist.research.profiles import read_yaml
    sub = tmp_path / 'profiles';sub.mkdir()
    profile = {'extends': 'paper-abstract-v1', 'execution': {'metrics': [
        {'id': 'adjacent', 'metric': 'jplag', 'options': {'java': 'java', 'jar': '../tools/jplag.jar'}}]}}
    (sub / 'study.yaml').write_text(yaml.safe_dump(profile))
    resolved = load_profile('profiles/study.yaml', tmp_path)
    assert resolved['execution']['metrics'][0]['options']['jar'] == str(tmp_path / 'tools/jplag.jar')
    (sub / 'bad.yaml').write_text('key: 1\nkey: 2\n')
    with pytest.raises(yaml.YAMLError):
        read_yaml(sub / 'bad.yaml')


def test_os_lock_prevents_concurrent_writers_and_releases(tmp_path):
    with exclusive_lock(tmp_path):
        with pytest.raises(StoreError, match='locked'):
            with exclusive_lock(tmp_path):
                pytest.fail('Acquired a duplicate lock')
    with exclusive_lock(tmp_path):
        pass
