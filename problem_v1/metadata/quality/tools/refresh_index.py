"""Refresh the index after successful generation; verify case hashes first."""
import hashlib
import json
from pathlib import Path

DATA=Path(__file__).resolve().parents[3]


def main():
    path=DATA/'dataset-index.json';index=json.loads(path.read_text(encoding='utf-8'))
    total=0
    for dataset in index['datasets']:
        manifest_path=DATA/dataset['manifest']
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        assert {p['problem_id'] for p in manifest['problems']}=={p['id'] for p in dataset['problems']}
        for p in manifest['problems']:
            for c in p['cases']:
                for kind in ('input','output'):
                    assert hashlib.sha256((manifest_path.parent/c[kind]).read_bytes()).hexdigest()==c[kind+'_sha256']
        dataset['manifest_sha256']=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        dataset['evaluation_case_count']=sum(len(p['cases']) for p in manifest['problems'])
        assert dataset['evaluation_case_count']==manifest['case_count']
        total+=dataset['evaluation_case_count']
        for p in dataset['problems']:
            p['input_normalization']='line' if p['id']=='LC_0003' else 'tokens'
    index['total_evaluation_cases']=total
    index['corpus_version']='v2-a-quality-1'
    index['date']='2026-09-17'
    path.write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(f'Refreshed {index["total_problem_count"]} problems, {total} evaluation cases')


if __name__=='__main__':main()
