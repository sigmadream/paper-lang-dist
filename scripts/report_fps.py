import argparse
from rttdist.fps_experiment import load_config
from rttdist.fps_reporting import report

parser=argparse.ArgumentParser()
parser.add_argument('--config',default='fps_v2.yaml')
parser.add_argument('--phase',choices=['pilot','main'],required=True)
args=parser.parse_args()
report(load_config(args.config),args.phase)
