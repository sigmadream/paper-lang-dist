"""Execute real toolchains: preserve source layout and classify failure modes."""
from pathlib import Path
import pytest

from rttdist.exec.adapters import evaluate_source
from rttdist.extract import extract_single_file_source_text
from tests.integration.test_execution_adapters import _build_problem_entry

SOURCES = {
    'haskell': 'main :: IO ()\nmain = do\n  s <- getLine\n  let n = read s :: Integer\n  print (n + 665)\n',
    'prolog': 'main :- read_line_to_string(user_input, S), number_string(N,S), X is N+665, writeln(X).\n',
}


@pytest.mark.parametrize('language', SOURCES)
@pytest.mark.parametrize('case', ['success', 'wrong_answer', 'compile_error', 'runtime_error', 'timeout'])
def test_extended_real_execution(tmp_path, language, case):
    source = SOURCES[language]
    if case == 'compile_error':
        source = {'haskell': 'main = do\n  let =', 'prolog': 'main :- (.'}[language]
    if case == 'runtime_error':
        source = {'haskell': 'main = error "boom"', 'prolog': 'main :- throw(boom).'}[language]
    if case == 'timeout':
        source = {'haskell': 'import Control.Concurrent\nmain = threadDelay 10000000',
                  'prolog': 'main :- sleep(10).'}[language]
    problem = _build_problem_entry(tmp_path, expected_output='999\n' if case == 'wrong_answer' else '666\n')
    path = tmp_path / {'haskell': 'Main.hs', 'prolog': 'main.pl'}[language]
    path.write_text(source, encoding='utf-8')
    # Give compilation its normal budget, then directly check the runtime budget.
    if case == 'timeout':
        from rttdist.exec.adapters import get_execution_adapter, _classify_fixture_result
        adapter = get_execution_adapter(language)
        compiled = adapter._compile(prepared_source_path=path, work_directory=tmp_path, timeout_seconds=30)
        assert compiled.exit_code == 0, compiled.stderr
        proc = adapter._run(prepared_source_path=path, work_directory=tmp_path, timeout_seconds=1, input_text='1\n')
        assert _classify_fixture_result(process_result=proc, expected_output='666')[0].value == 'timeout'
    else:
        result = evaluate_source(language=language, source_path=path, problem=problem,
                                 workspace_root=tmp_path / 'work', timeout_seconds=30)
        assert result.status.value == case, result


@pytest.mark.parametrize('source', [SOURCES['haskell'], 'fact(a).\nfact(b).\nmain :- writeln(a).\n'])
def test_abs_preserves_complete_unfenced_source(source):
    assert extract_single_file_source_text(source, preserve_unfenced=True) == source.strip()
