"""Rebuild twice and compare all reported numerical data with HTTP disabled."""
from pathlib import Path
import argparse
from unittest.mock import patch
from rttdist.fps_experiment import load_config
from rttdist.fps_reporting import report
from rttdist.experiment_io import digest,read_json,write_json

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default='fps_v2.yaml')
    args=parser.parse_args()
    cfg=load_config(args.config);root=Path(cfg['output_root'])/'main'
    with patch('urllib.request.urlopen',side_effect=AssertionError('Reporting attempted a network request')):
        first=report(cfg,'main')
        csv_first=(root/'observations.csv').read_bytes()
        second=report(cfg,'main')
        assert first==second and csv_first==(root/'observations.csv').read_bytes()
    assert read_json(root/'completion_audit.json')['passed']
    write_json(root/'reproducibility.json',{'passed':True,'network_disabled':True,'summary_exactly_equal':True,
        'csv_exactly_equal':True,'summary_sha256':digest((root/'summary.json').read_bytes()),
        'csv_sha256':digest(csv_first),'reporter_sha256':digest(Path('src/rttdist/fps_reporting.py').read_bytes())})
    print('Numerical report reproduced identically without network calls')

if __name__=='__main__':main()
