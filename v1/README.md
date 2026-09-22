# 첫 번째 논문 초록

첫 번째 논문(초록)이 완료된 시점의 원고와 연구 자료다. 폴더 이름 `v1`은 논문 버전이고, 설정과 실행 기록의 `fps-text-v2` / `fps-v2`는 실험 프로토콜 버전이다.

| 자료 | 위치 |
| --- | --- |
| 초록 원고와 수정본, 작성 양식 | [paper/](paper/) |
| 생성된 초록 PDF | [abs_paper.pdf](paper/abs_paper.pdf) |
| 생성된 초록 Word | [abs_paper.docx](paper/abs_paper.docx) |
| 지표와 종료 규칙 | [abs_PLAN.md](abs_PLAN.md) |
| 실험 설계와 실행 절차 | [abs_EXPERIMENT.md](abs_EXPERIMENT.md) |
| 최종 실험 결과와 해석 | [abs_RESULT.md](abs_RESULT.md) |
| 15문제, 3개 언어 기준 코드와 평가 입출력 | [data/](data/) |
| H2 설정 / H1 설정 | [fps_v2.yaml](../fps_v2.yaml) / [fps_v2_control.yaml](../fps_v2_control.yaml) |
| 원본 실행 기록 | [artifacts-commandcode/](../artifacts-commandcode/) |

`paper/`의 한글 파일명 Word 문서(v1.0, v1.1, v1.2, v1.2b)와 `.backups/`는 수작업 편집 이력으로 보존한다. `abs_paper.docx`와 PDF는 생성 원고이며, 한글 파일명 수정본과 동일하다고 가정하지 않는다. 생성 이력은 `abs_paper_provenance.json`에 있다.

데이터, 원고와 실험 기록의 경로는 동결된 설정과 감사 기록에서 참조하므로 유지한다. 새 실험은 별도의 설정과 출력 경로를 사용한다.
