"""Materialize the 15-problem fps-v2 corpus references.

Haskell and Prolog references were authored for the original v1 15-problem design
and kept inline in scripts/prepare_fps_corpus.py. This script writes them into
data/fps-v2/<problem>/reference.{hs,pl} so the corpus carries its own sources, and
reports which languages still have no reference for each selected problem.

Usage: python scripts/materialize_fps_v2_references.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

import prepare_fps_corpus as corpus  # noqa: E402

CORPUS = ROOT / 'data' / 'fps-v2'
LANGUAGES = {'cpp': 'cpp', 'c': 'c', 'java': 'java', 'python': 'py', 'haskell': 'hs', 'prolog': 'pl'}


def main():
    import json
    selected = [p['problem_id'] for p in json.loads((CORPUS / 'selection.json').read_text(encoding='utf-8'))['problems']]
    missing_hs, missing_pl = [], []
    for pid in selected:
        if pid in corpus.HS:
            (CORPUS / pid / 'reference.hs').write_text(corpus.HS[pid], encoding='utf-8', newline='\n')
        else:
            missing_hs.append(pid)
        if pid in corpus.PL:
            (CORPUS / pid / 'reference.pl').write_text(corpus.PL_IO + corpus.PL[pid], encoding='utf-8', newline='\n')
        else:
            missing_pl.append(pid)
    print('haskell missing:', missing_hs or 'none')
    print('prolog  missing:', missing_pl or 'none')
    for pid in selected:
        present = [lang for lang, ext in LANGUAGES.items() if (CORPUS / pid / f'reference.{ext}').is_file()]
        print(f'{pid:12} {len(present)}/6  {",".join(present)}')


if __name__ == '__main__':
    main()
