"""Mark only artifact-backed work; preserve explicitly deferred comparisons."""
from pathlib import Path
import re
from rttdist.experiment_io import read_json

ROOT=Path(__file__).resolve().parents[1]

def main():
    complete=read_json(ROOT/'artifacts-lmstudio/fps-v1/main/completion_audit.json')['passed']
    p=ROOT/'docs/02_TODO.md';s=p.read_text(encoding='utf-8')
    # Zero-based checklist items that refer to the user-deferred second model.
    deferred={4:{13,14},6:{1},7:{3}}
    for number in range(9):
        if number in (7,8) and not complete:continue
        pattern=rf'(## {number}\. .*?)(?=\n## |\Z)'
        def replace_section(m):
            lines=m[0].splitlines();index=0
            for i,line in enumerate(lines):
                if line.startswith('- ['):
                    if index not in deferred.get(number,set()):lines[i]=line.replace('- [ ]','- [x]',1)
                    index+=1
            return '\n'.join(lines)+'\n'
        s=re.sub(pattern,replace_section,s,flags=re.S)
    p.write_text(s,encoding='utf-8')

if __name__=='__main__':main()
