"""Acceptance tests: extensions, model isolation, crash recovery and offline analysis."""
from copy import deepcopy
import io
import json
from pathlib import Path
import sys

import pytest
import yaml

from rttdist.experiment_io import read_json, write_json
from rttdist.research.config import resolve_config
from rttdist.research.engine import run_experiment
from rttdist.research.analysis import analyze
from rttdist.research.metrics import Metric, METRICS, register_metric
from rttdist.research.profiles import load_profile
from rttdist.research.store import StoreError


CPP = 'int main(){return 0;}\n'


@pytest.fixture
def settings(tmp_path):
    problem = tmp_path / 'corpus/p'
    for name, number in [('prompt_examples', '0'), ('evaluation', '1')]:
        directory = problem / name
        directory.mkdir(parents=True)
        (directory / '1.inp').write_text(number)
        (directory / '1.out').write_text('')
    (problem / 'statement.md').write_text('Read an integer and print nothing.')
    (problem / 'reference.cpp').write_text(CPP)
    return {'schema_version': 1, 'id': 'test', 'corpus_root': str(tmp_path / 'corpus'),
            'output_root': str(tmp_path / 'out'), 'problem_ids': ['p'], 'routes': [['cpp', 'python']],
            'repeats': 2, 'schedule_seed': 7, 'models': {
                'local': {'model': 'test-model', 'generation': {'temperature': .6, 'seed': 4}},
                'cloud': {'provider': 'openai_compatible', 'model': 'test-model', 'endpoint': 'http://example.test/v1',
                          'generation': {'temperature': .6, 'seed': 4}}},
            'profile': {'extends': 'paper-abstract-v1', 'execution': {'max_steps': 4, 'metrics': [
                {'id': 'adjacent', 'metric': 'token_dice'}]},
                'analysis': {'metrics': [{'id': 'origin', 'metric': 'token_dice', 'reference': 'origin'}], 'bootstrap_samples': 25}},
            'runtime': {'tools': {'cpp': sys.executable, 'python': sys.executable}}}


@pytest.fixture
def wire(monkeypatch):
    requests = []
    def send(request, timeout):
        payload = json.loads(request.data)
        requests.append(payload)
        body = {'model': 'test-model', 'usage': {'prompt_tokens': 20, 'completion_tokens': 10},
                'choices': [{'message': {'content': '```cpp\n' + CPP + '```'}, 'finish_reason': 'stop'}]}
        return io.BytesIO(json.dumps(body).encode())
    monkeypatch.setattr('rttdist.providers.request.urlopen', send)
    return requests


def success(*args):
    return {'status': 'success', 'cases': [{'status': 'success'}]}


def test_model_matrix_default_lmstudio_sampling_and_repetition_isolation(settings, wire):
    cfg = resolve_config(settings)
    cfg['parallel_models'] = 2
    rows = run_experiment(cfg, evaluator=success)
    assert len(rows) == 4 and len(wire) == 8
    assert {r['model_id'] for r in rows} == {'local', 'cloud'}
    assert all(r['decision']['reached_step'] == 2 for r in rows)
    assert {p['temperature'] for p in wire} == {.6}
    assert {p['seed'] for p in wire} == {4, 5}
    assert cfg['models']['local']['endpoint'] == 'http://localhost:1234/v1'
    assert run_experiment(cfg, evaluator=success, resume=True) == rows
    assert len(wire) == 8
    root = Path(cfg['output_root']) / cfg['id']
    summary = analyze(root, analysis_id='first')
    assert summary['complete'] and len(summary['groups']) == 2
    assert all(g['valid'] == 2 and g['mean_hops'] == 2 and g['hop_adjusted_distance'] == 2 for g in summary['groups'])
    assert analyze(root, analysis_id='first') == summary
    assert (root / 'analyses/first/summary.csv').is_file()
    with pytest.raises(StoreError, match='already exists'):
        run_experiment(cfg, evaluator=success)


def test_register_metric_and_reanalyze_without_network_or_execution(settings, wire, monkeypatch):
    def custom(context, options):
        return {'status': 'measured', 'value': len(context.candidate) + options['offset']}
    monkeypatch.setitem(METRICS, 'custom', Metric('custom', '7', 'characters', custom))
    cfg = resolve_config(settings)
    run_experiment(cfg, evaluator=success)
    root = Path(cfg['output_root']) / cfg['id']
    before = {p: p.read_bytes() for p in (root / 'trials').rglob('*') if p.is_file()}
    monkeypatch.setattr('rttdist.providers.request.urlopen', lambda *a, **k: pytest.fail('Network during analysis'))
    summary = analyze(root, profile={'metrics': [{'id': 'custom', 'metric': 'custom', 'options': {'offset': 3}}]}, analysis_id='custom')
    assert summary['groups'][0]['measurements']['custom']['mean'] == len(CPP.strip()) + 3
    assert before == {p: p.read_bytes() for p in (root / 'trials').rglob('*') if p.is_file()}
    assert len(wire) == 8


def test_crash_after_response_reuses_generation(settings, wire):
    settings['models'] = {'local': settings['models']['local']}
    settings['repeats'] = 1
    cfg = resolve_config(settings)
    calls = []
    def crash_once(source, language, problem, folder, runtime):
        calls.append(language)
        if language == 'python':
            raise KeyboardInterrupt('simulated process loss after response')
        return success()
    with pytest.raises(KeyboardInterrupt):
        run_experiment(cfg, evaluator=crash_once)
    assert len(wire) == 1
    rows = run_experiment(cfg, evaluator=success, resume=True)
    assert rows[0]['decision']['success'] and len(wire) == 2


def test_crash_after_result_before_seal_finishes_commit_without_generation(settings, wire, monkeypatch):
    from rttdist.research import engine
    settings['models'] = {'local': settings['models']['local']}
    settings['repeats'] = 1
    cfg = resolve_config(settings)
    original_seal = engine.seal
    def crash(folder):
        if folder.name.startswith('attempt-'):
            raise KeyboardInterrupt('crash at commit')
        return original_seal(folder)
    monkeypatch.setattr(engine, 'seal', crash)
    with pytest.raises(KeyboardInterrupt):
        run_experiment(cfg, evaluator=success)
    assert len(wire) == 2
    monkeypatch.setattr(engine, 'seal', original_seal)
    rows = run_experiment(cfg, evaluator=success, resume=True)
    assert rows[0]['decision']['success'] and len(wire) == 2


def test_functional_failure_is_counted_and_never_resampled(settings, wire):
    cfg = resolve_config(settings)
    def evaluator(source, language, *args):
        return {'status': 'wrong_answer' if language == 'python' else 'success'}
    rows = run_experiment(cfg, evaluator=evaluator)
    assert len(wire) == 4
    assert all(r['decision']['category'] == 'functional_failure' for r in rows)
    assert run_experiment(cfg, resume=True, new_attempt=True, evaluator=success) == rows
    assert len(wire) == 4
    summary = analyze(Path(cfg['output_root']) / cfg['id'])
    assert all(g['success_rate'] == 0 and g['hop_adjusted_distance'] is None and g['valid'] == 2 for g in summary['groups'])


def test_infrastructure_resume_and_explicit_new_attempt_preserve_evidence(settings, wire):
    from rttdist.providers import ProviderError
    settings['models'] = {'local': settings['models']['local']}
    settings['repeats'] = 1
    cfg = resolve_config(settings)
    class Broken:
        def complete(self, *args):
            raise ProviderError('unavailable')
    rows = run_experiment(cfg, evaluator=success, provider_factory=lambda *a, **kw: Broken())
    assert rows[0]['decision']['category'] == 'invalid'
    root = Path(cfg['output_root']) / cfg['id']
    first = root / rows[0]['artifact_path']
    before = (first / 'progress.json').read_bytes()
    rows = run_experiment(cfg, evaluator=success, resume=True, new_attempt=True)
    assert rows[0]['attempt'] == 'attempt-002' and rows[0]['decision']['success']
    assert (first / 'progress.json').read_bytes() == before
    assert len(wire) == 2


def test_tampered_artifacts_or_changed_conditions_are_rejected(settings, wire):
    cfg = resolve_config(settings)
    rows = run_experiment(cfg, evaluator=success)
    changed = deepcopy(cfg)
    changed['models']['local']['generation']['temperature'] = .8
    with pytest.raises(StoreError, match='Immutable'):
        run_experiment(changed, evaluator=success, resume=True)
    root = Path(cfg['output_root']) / cfg['id']
    source = root / rows[0]['artifact_path'] / 'step-0001/source.py'
    source.write_text('tampered')
    with pytest.raises(StoreError, match='integrity'):
        analyze(root)


def test_offline_policy_change_rejected(settings, wire):
    cfg = resolve_config(settings)
    run_experiment(cfg, evaluator=success)
    profile = deepcopy(cfg['profile'])
    profile['execution']['threshold'] = .99
    with pytest.raises(ValueError, match='cannot change execution'):
        analyze(Path(cfg['output_root']) / cfg['id'], profile=profile)


def test_analysis_tool_changes_require_a_new_analysis_id(settings, wire, tmp_path, monkeypatch):
    monkeypatch.setitem(METRICS, 'jplag', Metric('jplag', '1', 'similarity', lambda ctx, opts: {'status': 'measured', 'value': 1}))
    cfg = resolve_config(settings)
    run_experiment(cfg, evaluator=success)
    root = Path(cfg['output_root']) / cfg['id']
    jar = tmp_path / 'tool.jar';jar.write_bytes(b'version-one')
    profile = {'metrics': [{'id': 'tool', 'metric': 'jplag', 'options': {'java': sys.executable, 'jar': str(jar)}}]}
    analyze(root, profile=profile, analysis_id='tool')
    jar.write_bytes(b'version-two')
    with pytest.raises(StoreError, match='conditions changed'):
        analyze(root, profile=profile, analysis_id='tool')


def test_cli_validate_status_and_offline_analyze(settings, wire, tmp_path, capsys):
    from rttdist.cli import main
    config = tmp_path / 'config.yaml'
    config.write_text(yaml.safe_dump(settings))
    assert main(['research', 'validate', '--config', str(config)]) == 0
    assert not wire
    cfg = resolve_config(settings)
    run_experiment(cfg, evaluator=success)
    root = str(Path(cfg['output_root']) / cfg['id'])
    assert main(['research', 'status', '--experiment', root]) == 0
    assert main(['research', 'analyze', '--experiment', root, '--analysis-id', 'cli']) == 0
    assert '"mean_hops": 2' in capsys.readouterr().out


def test_real_python_execution_and_hidden_case_failure(settings, wire):
    from rttdist.fps_execution import evaluate
    cfg = resolve_config(settings)
    problem = Path(cfg['corpus_root']) / 'p'
    folder = problem.parent / 'execution'
    assert evaluate('import sys\nsys.stdin.read()\n', 'python', problem, folder / 'ok', cfg['runtime'])['status'] == 'success'
    assert evaluate('print(42)\n', 'python', problem, folder / 'bad', cfg['runtime'])['status'] == 'wrong_answer'


def test_real_python_prolog_roundtrip_and_replay(settings, monkeypatch):
    import shutil
    if not shutil.which('swipl'):
        pytest.skip('SWI-Prolog is not installed')
    from rttdist.research.replay import replay
    origin = 'import sys\nsys.stdin.read()'
    (Path(settings['corpus_root']) / 'p/reference.py').write_text(origin)
    settings['routes'] = [['python', 'prolog']]
    settings['models'] = {'local': settings['models']['local']}
    settings['repeats'] = 1
    settings['profile']['execution']['metrics'] = [{'id': 'adjacent', 'metric': 'source_identity'}]
    settings['profile']['analysis']['metrics'] = []
    cfg = resolve_config(settings)
    outputs = iter(['main :- read_line_to_string(user_input, _).', origin])
    calls = []
    def send(request, timeout):
        calls.append(request)
        return io.BytesIO(json.dumps({'model': 'test-model', 'choices': [{'message': {'content': next(outputs)}}]}).encode())
    monkeypatch.setattr('rttdist.providers.request.urlopen', send)
    rows = run_experiment(cfg)
    assert rows[0]['decision']['success'] and rows[0]['decision']['reached_step'] == 2
    assert all(step['execution']['cases'][0]['status'] == 'success' for step in rows[0]['steps'])
    assert replay(Path(cfg['output_root']) / cfg['id'])['matches_original']
    assert len(calls) == 2


def test_jplag_metric_with_real_tool(tmp_path):
    import shutil
    from rttdist.research.metrics import MetricContext, measure
    jar = Path(__file__).resolve().parents[2] / 'jplag-6.3.0-jar-with-dependencies.jar'
    if not jar.is_file() or not shutil.which('java'):
        pytest.skip('JPlag or Java is unavailable')
    source = 'int sum(int n){int s=0;for(int i=0;i<n;i++){if(i%2==0){s+=i;}else{s-=i;}}return s;}'
    metric = measure({'id': 'similarity', 'metric': 'jplag', 'options': {
        'java': shutil.which('java'), 'jar': str(jar), 'minimum_tokens': 9}},
        MetricContext(source, source, 'cpp', tmp_path / 'comparison'))
    assert metric['status'] == 'measured' and metric['value'] == 1


def test_replay_reextracts_and_reevaluates_without_model_calls(settings, wire, monkeypatch):
    from rttdist.research.replay import replay
    cfg = resolve_config(settings)
    run_experiment(cfg, evaluator=success)
    root = Path(cfg['output_root']) / cfg['id']
    before = {p: p.read_bytes() for p in (root / 'trials').rglob('*') if p.is_file()}
    monkeypatch.setattr('rttdist.providers.request.urlopen', lambda *a, **kw: pytest.fail('Model call during replay'))
    calls = []
    def evaluate_again(source, language, *args):
        calls.append(language)
        return success()
    report = replay(root, replay_id='again', evaluator=evaluate_again)
    assert report['matches_original'] and report['model_calls'] == 0 and len(calls) == 8
    assert replay(root, replay_id='again', evaluator=evaluate_again) == report
    assert len(calls) == 8
    assert before == {p: p.read_bytes() for p in (root / 'trials').rglob('*') if p.is_file()}


def test_provider_extension_uses_common_engine(settings, monkeypatch):
    from rttdist.providers import PROVIDER_FACTORIES, register_provider
    requests = []
    class Native:
        def __init__(self, config, ledger=None):
            self.config = config
        def complete(self, payload, folder):
            requests.append(payload)
            return {'body': {'choices': [{'message': {'content': CPP}}]}, 'actual_model': 'native-model',
                    'usage': None, 'latency_seconds': None}
    # Preserve registry identity shared by configuration and execution.
    monkeypatch.setitem(PROVIDER_FACTORIES, 'native-test', Native)
    settings['models'] = {'native': {'provider': 'native-test', 'model': 'native-model'}}
    cfg = resolve_config(settings)
    rows = run_experiment(cfg, evaluator=success)
    assert len(requests) == 4 and all(r['decision']['success'] for r in rows)


def test_format_error_keeps_usage_for_analysis(settings, monkeypatch):
    from rttdist.providers import CompatibleProvider
    settings['models'] = {'local': settings['models']['local']}
    settings['repeats'] = 1
    cfg = resolve_config(settings)
    body = {'model': 'test-model', 'choices': [], 'usage': {'prompt_tokens': 30, 'completion_tokens': 2}}
    monkeypatch.setattr('rttdist.providers.request.urlopen', lambda *a, **kw: io.BytesIO(json.dumps(body).encode()))
    rows = run_experiment(cfg, evaluator=success)
    assert rows[0]['decision']['category'] == 'functional_failure'
    summary = analyze(Path(cfg['output_root']) / cfg['id'], profile={'metrics': [
        {'id': 'input_tokens', 'metric': 'prompt_tokens', 'scope': 'step'}]})
    assert summary['groups'][0]['measurements']['input_tokens']['mean'] == 30


@pytest.mark.parametrize('mutation', [
    lambda s: s.update(repeats=0),
    lambda s: s['models']['local']['generation'].update(temperature=float('nan')),
    lambda s: s['models']['local'].update(api_key_env='sk-secret'),
    lambda s: s['profile']['execution'].update(threshhold=.9),
    lambda s: s['profile']['execution']['metrics'][0].update(version='99'),
])
def test_invalid_configuration_fails_before_network(settings, wire, mutation):
    mutation(settings)
    with pytest.raises(ValueError):
        resolve_config(settings)
    assert not wire
