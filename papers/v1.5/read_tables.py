import json

with open('paper_structure.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for t in data.get('tables', []):
    print(f"=== TABLE {t['table_index']} ===")
    for row in t.get('rows', []):
        print(row)
    print()
