# 연구 도구

저장소 루트에서 실행한다. 첫 번째 논문의 실험 프로토콜은 `fps-text-v2`다.

| 스크립트 | 용도 |
| --- | --- |
| `validate_fps_corpus.py` | 기준 코드와 평가 데이터 사전 검증 |
| `preflight_fps_v2.py` | 상태 동일성과 유사도 분석기 점검 |
| `freeze_fps_v2_main.py` | 파일럿 이후 본 실험 설계 동결 |
| `report_fps.py` | 기존 관측으로 통계·도표·감사 결과 재생성 |
| `verify_fps_reproducibility.py` | 네트워크를 차단한 두 번의 보고서 재생성 결과 비교 |
| `diagnose_fps_v2.py` | 종료 원인과 언어별 기능 실패 진단 |
| `diagnose_fps_v2_multiblock.py` | 다중 코드 블록 응답의 사후 진단 |
| `build_abs_paper_v2.py` | 감사된 통계로 생성 원고와 그림 작성 |

보고서 도구 두 개의 기본 설정은 `fps_v2.yaml`이며, `--config fps_v2_control.yaml`로 H1 대조 실험을 선택한다. 보고서 재생성은 기존 요약과 감사 파일을 갱신한다. 원고 생성은 `v1/paper/abs_paper.docx`와 그림을 갱신하므로 수작업 수정본을 재현하는 명령으로 사용하지 않는다.

다음 파일은 과거 연구의 자료 생성 과정이나 공통 진단을 보존하기 위해 남겨 둔다. 현재 초록의 실행 절차에 포함하지 않는다.

- `prepare_fps_corpus.py`: 최초 15문제 선정 및 기준 코드 생성 과정. 출력 경로는 당시의 `data/fps-v1`이다.
- `v1_checks.py`, `v1_diagnostics.py`, `write_result_v1.py`: 이전 SF 프로토콜의 감사·진단·표 작성 도구.
- `experiment-env.ps1`: 이전 로컬 GCC/R 환경 설정.

이미 삭제된 이전 실행 기록에 종속된 실행·상태 확인·문서 갱신 스크립트는 정리했다. 목록은 [정리 기록](../docs/CLEANUP.md)을 참고한다.
