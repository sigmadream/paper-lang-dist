import json
import sys

with open('paper_structure.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

paras = data.get('paragraphs', [])

start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
end = int(sys.argv[2]) if len(sys.argv) > 2 else len(paras)

for p in paras[start:end]:
    t = p.get('text', '').strip()
    idx = p.get('index', 0)
    style = p.get('style', '')
    if t:
        print(f"[P{idx}] ({style})\n{t}\n")
