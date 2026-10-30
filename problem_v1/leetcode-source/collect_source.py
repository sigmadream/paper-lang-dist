"""Collect provenance and public example data, without copying solution code."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess


def main():
    parser=argparse.ArgumentParser();parser.add_argument('checkout',type=Path)
    args=parser.parse_args(); checkout=args.checkout.resolve();out=Path(__file__).resolve().parent
    commit=subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
    assert commit=='b9d7d2c234c39b3b3c67eded0c125e2841685b29', 'Use the recorded source commit'
    repo='https://github.com/DhanushNehru/Leetcode'
    inventory={'repository':repo,'commit':commit,'default_branch':'main',
               'license_file_found':False,'file_count':0,'files':[]}
    for p in sorted(checkout.rglob('*')):
        if not p.is_file() or '.git' in p.relative_to(checkout).parts:continue
        rel=p.relative_to(checkout).as_posix()
        if p.name.lower().startswith(('license','copying')):inventory['license_file_found']=True
        inventory['files'].append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    inventory['file_count']=len(inventory['files'])
    public={'repository':repo,'commit':commit,'role':'public examples for source inventory only; excluded from evaluation-v2-a',
            'independently_validated':False, 'problems':[]}
    for p in sorted(checkout.glob('*/README.md')):
        text=p.read_text(encoding='utf-8');rel=p.relative_to(checkout).as_posix();examples=[]
        blocks=re.findall(r'<pre[^>]*>(.*?)</pre>',text,re.S|re.I)
        blocks+=re.findall(r'<div class="example-block">(.*?)</div>',text,re.S|re.I)
        for block in blocks:
            plain=html.unescape(re.sub(r'<[^>]+>','',block)).strip()
            match=re.search(r'Input:\s*(.*?)\s*Output:\s*(.*?)(?:\s*Explanation:.*)?$',plain,re.S)
            if match:examples.append({'input':match.group(1).strip(),'output':match.group(2).strip()})
        if examples:
            public['problems'].append({'source_directory':p.parent.name,'source_path':rel,
                'source_url':f'{repo}/blob/{commit}/{rel}',
                'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'examples':examples})
    public['problem_count']=len(public['problems'])
    public['example_count']=sum(len(p['examples']) for p in public['problems'])
    for name,data in [('inventory.json',inventory),('public_examples.json',public)]:
        (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'{inventory["file_count"]} source files; {public["problem_count"]} problems; {public["example_count"]} public examples')


if __name__=='__main__':main()
