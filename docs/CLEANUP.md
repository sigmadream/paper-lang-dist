# 첫 번째 초록 완료 후 저장소 정리

정리일: 2026-09-22.

`v1/`의 초록·수정본·백업, 15문제 데이터, 계획과 결과를 보존한다. `artifacts-commandcode/`의 원본 응답·생성 소스·평가 기록·JPlag 결과·요약·설계 동결 기록도 보존한다. 작업 시작 전에 이미 있던 소스 수정과 `artifacts-lmstudio/`, `data/fps-v1/`, 과거 `docs/` 자료 삭제 내역은 유지했다.

삭제 범위:

- 실험 평가에서 생성된 실행 파일 2,120개, 오브젝트 파일 796개, Haskell 인터페이스 파일 796개, Java 클래스 파일 216개.
- 로컬 `.cache/`, `.pytest_cache/`와 프로젝트의 Python 바이트코드 캐시. 설치된 `.venv/`, `.tools/`는 유지한다.
- 입력 데이터와 실행 기록이 이미 없어진 `fps_v1.yaml`.
- 이전 FPS 실험 전용 도구: `analyze_fps_cases.py`, `build_fps_abstract.py`, `calibrate_fps_similarity.py`, `configure_fps.py`, `freeze_fps_main.py`, `update_fps_todo.py`, `write_fps_result.py`.
- 이전 SF 실험의 일회성 실행·상태 관리 도구: `amend_v2_to_single.py`, `finish_v2.py`, `run_v1_main.py`, `run_v2.py`, `run_v2_single.py`, `v1_status.py`, `v2_quick_report.py`, `v2_status.py`.

삭제한 설정과 스크립트는 모두 기존 Git 추적 파일이며 변경 이력에서 확인할 수 있다. 최초 데이터 생성 코드와 범용 감사·진단 도구는 [scripts/README.md](../scripts/README.md)에 구분해 남겼다.

README를 현재 논문과 유효한 경로 중심으로 다시 작성했다. `report_fps.py`의 기본 설정을 `fps_v2.yaml`로 바꾸고 `verify_fps_reproducibility.py`에 동일한 기본값과 `--config` 옵션을 추가했다. `.gitignore`에는 캐시와 실험 컴파일 산출물, 일부 LaTeX 중간 파일 규칙을 추가했다. 평가 정답 `.out`이나 연구 실행 `.log`, 논문 `.pdf`를 포괄적으로 제외하지 않는다.

데이터와 실험 폴더의 경로를 유지해 동결된 설정과 감사 기록의 참조를 보존한다. 실행 파일 삭제 이후에도 저장된 평가 기록을 이용한 감사와 통계 집계가 가능하다. 재컴파일 방법과 평가 캐시 동작은 [실험 기록 안내](../artifacts-commandcode/README.md)를 참고한다.

검증 결과:

- 기존 연구 자료 43,386개 파일의 SHA-256이 정리 전후 모두 일치했다.
- 원본 기록으로 완료 감사를 다시 계산하여 파일럿 90건, H2 본 실행 450건, H1 비교 300건 모두 통과했다. 기존 감사·요약 파일은 갱신하지 않았다.
- 전체 테스트에서 209개 통과, Haskell 실행 권한 문제로 4개 실패했다. 권한과 임시 경로를 조정한 뒤 해당 통합 테스트 파일의 12개 테스트가 모두 통과했다.
- 새로 작성한 안내 문서의 내부 링크와 보고서 CLI 옵션을 확인했다.
- 컴파일 산출물·불필요한 파일·기존 캐시를 합쳐 약 9.41GiB를 삭제했다. 이번 검증에 사용한 임시 폴더도 제거했다.
