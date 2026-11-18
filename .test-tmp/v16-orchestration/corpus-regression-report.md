# 평가 입력·코퍼스 회귀 검사 보고

## 원인

실제 저장소 정리 후 problem_v1·problem_v1.5 디렉터리는 제거되었지만 두 prepared_dataset 테스트는 과거 경로를 계속 사용하고 있었습니다. 수정 전 아래 명령에서 두 테스트가 FileNotFoundError로 실패하였으며 나머지 42개 검사는 통과하였습니다.

`uv run pytest tests/integration/test_evaluation_inputs.py tests/unit/test_v16_corpus.py::test_all_references_and_cases_are_required -q`

- test_prepared_dataset_loads_all_520_evaluation_cases
- test_prepared_v1_5_dataset_loads_all_65_evaluation_cases

매니페스트 누락 기대값 문제는 이전 작업에서 validation.file_hashes에 manifest.json 자체를 포함하도록 수정되어 있었습니다. 이번 수정 전 실행에서도 test_all_references_and_cases_are_required가 통과하는 것을 확인하였으며 해당 파일은 이번 작업에서 추가 변경하지 않았습니다.

## 변경 파일과 검사 범위

변경 파일은 tests/integration/test_evaluation_inputs.py 하나입니다. 전체 검사에는 현재 problem/dataset-index.json의 40문제를 사용하고 520개 평가 사례 검사를 유지하였습니다. 기존 5문제 검사도 같은 인덱스에서 다음 ID만 선택하여 정확히 65개 평가 사례를 확인하도록 수정하였습니다.

- LC_0338
- IPOP_9012
- LC_0283
- LC_0053
- LC_0547

5문제 목록과 순서는 실제 `git show 3ac2044d:problem_v1.5/dataset-index.json` 조회 결과에서 확인하였습니다. 테스트 실행 시 git 조회에 의존하지 않도록 확인한 목록을 직접 기록하였습니다. 문제별 13개 평가 쌍, 명세·C++ 기준 구현 경로, 공개 예시 디렉터리와 평가 디렉터리의 분리, 공개 입력·평가 입력 중복 거부 검증을 유지하였습니다. 문제 본문·자료·생산 코드·코퍼스 구현에는 변경이 없으며 테스트 skip이나 가짜 자료 복원도 없었습니다.

## 검증 결과

- `uv run pytest tests/integration/test_evaluation_inputs.py tests/unit/test_v16_corpus.py -q`: 54개 통과, 38.86초
- 위 결과에 test_all_references_and_cases_are_required와 코퍼스 테스트 11개 전체 포함
- 실제 평가 입력 520개와 기존 하위집합 65개를 계속 읽고 공개 예시·평가 분리 검증 수행
- `uv run black --check tests/integration/test_evaluation_inputs.py tests/unit/test_v16_corpus.py`: 두 파일 통과
- `git diff --check -- tests/integration/test_evaluation_inputs.py`: 통과
- `git diff --name-only -- problem`: 변경 파일 없음

전체 테스트 결과는 실행 종료 후 아래에 기록합니다.

`uv run pytest -q`의 최종 결과는 374개 통과·실패 0개·skip 0개이며 96.07초가 걸렸습니다. test_v16_report.py에서 MatplotlibDeprecationWarning 902개가 출력되었으며 scripts/report_v16.py의 103행·139행에서 float 좌표의 향후 지원 중단을 알리는 경고입니다. 해당 보고 코드 수정은 이번 소유 범위에 포함하지 않아 경고를 그대로 보고합니다. 요청한 회귀 수정에서 남은 실패는 없습니다.
