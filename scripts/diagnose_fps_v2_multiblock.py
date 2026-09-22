"""Post-hoc diagnostic only: would the LAST fenced block of multi-block responses pass?

The registered rule (multiple fenced blocks = format_error) is unchanged; this
evaluates the last block offline, without model calls, to size that rule's effect.

Usage: python scripts/diagnose_fps_v2_multiblock.py fps_v2.yaml main
"""
from collections import Counter
from pathlib import Path
import re
import sys

from rttdist.experiment_io import read_json, write_json, timestamp
from rttdist.fps_execution import evaluate
from rttdist.fps_experiment import load_config

FENCE=re.compile(r'```[^\n`]*\n(.*?)```',re.S)

def main(config_path,phase):
    cfg=load_config(config_path);root=Path(cfg['output_root'])/phase
    rows=[]
    for path in sorted(root.glob('*/*/attempt-*/observation.json')):
        r=read_json(path)
        if r['status']!='format_error':continue
        last=r['steps'][-1];step=path.parent/f"step-{last['step']:02}"
        text=read_json(step/'response.json')['body']['choices'][0]['message'].get('content') or ''
        blocks=FENCE.findall(text)
        if len(blocks)<2:continue
        value=evaluate(blocks[-1].strip('\n'),last['language'],Path(cfg['corpus_root'])/r['problem_id'],
                       step/'posthoc_last_block'/'evaluation',cfg['runtime'])
        rows.append({'problem_id':r['problem_id'],'route':r['route'],'attempt':r['attempt'],'step':last['step'],
                     'language':last['language'],'blocks':len(blocks),'last_block_status':value['status']})
        print(rows[-1],flush=True)
    by=Counter((x['language'],x['last_block_status']) for x in rows)
    write_json(root/'diagnostics_multiblock.json',{'at':timestamp(),'rows':rows,'by_language_status':{f'{k[0]}:{k[1]}':v for k,v in by.items()}})
    print(by)

if __name__=='__main__':main(sys.argv[1],sys.argv[2])
