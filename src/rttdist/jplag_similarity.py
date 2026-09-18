"""Isolated two-submission C++ comparison, retaining every tool output."""
import csv
from pathlib import Path
import subprocess

from rttdist.experiment_io import digest, read_json, write_json

ABS = Path(__file__).resolve().parents[2] / 'docs/abs'
JAR = ABS / 'tools/jplag-6.3.0-jar-with-dependencies.jar'


def tool_config():
    java = list((ABS / 'tools').glob('jdk-25*/bin/java.exe'))
    if len(java) != 1 or not JAR.is_file():
        raise RuntimeError('Expected exactly one local Java 25 and the specified JPlag JAR')
    return {'java': str(java[0].resolve()), 'jar': str(JAR.resolve()), 'jar_sha256': digest(JAR.read_bytes()),
            'language': 'cpp', 'minimum_tokens': 9, 'normalize': False, 'similarity_field': 'averageSimilarity',
            'scale': [0, 1], 'threshold': 0, 'cluster': False, 'match_merging': False}


def measure(seed, candidate, folder, *, config=None):
    folder = Path(folder).resolve()
    config = config or tool_config()
    contract = {'seed_sha256': digest(seed.encode('utf-8')), 'candidate_sha256': digest(candidate.encode('utf-8')),
                'config': config}
    record = folder / 'measurement.json'
    if record.exists():
        previous = read_json(record)
        if previous['contract'] != contract:
            raise ValueError('JPlag cached input or settings changed')
        return previous
    for name, source in [('seed', seed), ('candidate', candidate)]:
        path = folder / 'submissions' / name / 'Main.cpp'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source, encoding='utf-8')
    command = [config['java'], '-jar', config['jar'], '-M', 'RUN', '-l', 'cpp', '-t', str(config['minimum_tokens']),
               '-m', '0', '-n', '-1', '--cluster-skip', '--csv-export', '--encoding', 'UTF-8',
               '--overwrite', '-r', str(folder / 'result'), str(folder / 'submissions')]
    result = {'contract': contract, 'command': command, 'status': 'unavailable', 'value': None,
              'reason': None, 'reference': 'seed_source', 'candidate': 'stabilized_source'}
    try:
        proc = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=90)
        result.update(exit_code=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
    except subprocess.TimeoutExpired as exc:
        result.update(reason='jplag_timeout', exit_code=None,
                      stdout=str(exc.stdout or ''), stderr=str(exc.stderr or ''))
    else:
        csv_path = folder / 'result/results.csv'
        if proc.returncode != 0:
            result['reason'] = 'jplag_error'
        elif not csv_path.exists():
            result['reason'] = 'missing_result'
        else:
            with csv_path.open(encoding='utf-8-sig', newline='') as stream:
                rows = list(csv.DictReader(stream))
            if len(rows) != 1 or {rows[0]['submissionName1'], rows[0]['submissionName2']} != {'seed', 'candidate'}:
                result['reason'] = 'pair_not_measured'
            else:
                value = float(rows[0]['averageSimilarity'])
                if not 0 <= value <= 1:
                    raise ValueError(f'JPlag result outside [0,1]: {value}')
                result.update(status='measured', value=value, reason=None, raw_csv_row=rows[0])
    write_json(record, result)
    return result
