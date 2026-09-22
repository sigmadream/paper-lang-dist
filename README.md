# RTT 언어 거리 연구

왕복 번역(RTT)의 고정점과 기능 보존을 이용해 프로그래밍 언어 사이의 거리를 관찰하는 연구 저장소다. 첫 번째 논문(초록)은 완료되었으며, 원고·데이터·계획·결과는 [v1/](v1/README.md)에 정리되어 있다.

먼저 [초록 PDF](v1/paper/abs_paper.pdf), [원고와 수정본](v1/paper/), [실험 결과](v1/abs_RESULT.md)를 참고한다. 논문 폴더 `v1`과 실험 프로토콜 `fps-text-v2`는 서로 다른 버전 이름이다.

| 경로 | 역할 |
| --- | --- |
| [v1/](v1/README.md) | 완료된 첫 번째 초록과 15문제 연구 데이터 |
| [artifacts-commandcode/](artifacts-commandcode/README.md) | 원본 응답, 생성 코드, 평가 결과, 통계와 완료 감사 |
| [fps_v2.yaml](fps_v2.yaml) | H2: C++·Haskell·Prolog 사이 6개 방향 실험 설정 |
| [fps_v2_control.yaml](fps_v2_control.yaml) | H1: Python·Java 대조 경로와 처리 경로 비교 설정 |
| [src/rttdist/](src/rttdist/) | RTT 실행기, 평가기, 유사도와 보고서 구현 |
| [scripts/](scripts/README.md) | 사전 검증, 보고서·원고 생성, 진단 도구 |
| [tests/](tests/) | 단위·통합 테스트와 테스트 자료 |
| [problem/](problem/README.md) | 기존 40문제 데이터와 데이터 생성·검증 자료 |
| [ref/](ref/) | 참고 논문 |
| [graph/](graph/), [presentation/](presentation/) | 과거 분석 코드와 발표 자료 |

본 실험 H2는 450관측, H1 비교는 300관측이다. H2에는 파일럿 90관측이 포함되고 H1에는 H2의 처리 경로 150관측이 재사용된다. 수치의 해석 범위와 한계는 [결과 문서](v1/abs_RESULT.md)에 기록되어 있다.

개발 환경은 Python 3.14 이상과 `uv`를 사용한다.

```powershell
uv sync --extra analysis
uv run python -m pytest -q
```

기존 실행 기록으로 보고서를 다시 생성하려면 다음 명령을 사용한다. 모델 API를 호출하지 않지만 해당 폴더의 요약·도표·감사 파일은 갱신된다.

```powershell
uv run python scripts/report_fps.py --config fps_v2.yaml --phase main
uv run python scripts/report_fps.py --config fps_v2_control.yaml --phase main
```

두 번의 보고서 생성 결과가 일치하는지 확인하는 도구도 같은 설정을 받는다.

```powershell
uv run python scripts/verify_fps_reproducibility.py --config fps_v2.yaml
uv run python scripts/verify_fps_reproducibility.py --config fps_v2_control.yaml
```

새 실험을 실행할 때는 설정을 복사하고 별도 출력 경로를 지정한다. YAML의 실행 도구와 JPlag 경로는 실험 당시 Windows 환경의 절대 경로다. 현재 환경에 맞게 수정한 뒤 기준 코드 검증과 사전 점검을 거쳐야 한다. API 인증은 `CMD_API_KEY` 환경 변수를 사용한다. 완료된 실험의 동결 설정과 기록은 보존한다.

`lmstudio_abs.yaml`, `lmstudio_v2.yaml`은 이전 SF 실험 및 호환성 테스트용이다. `problem/`, R 환경(`renv/`, `renv.lock`, `.Rprofile`)과 과거 발표 자료도 연구 이력으로 유지한다. `.venv/`, `.tools/`는 로컬 실행 환경이다. JPlag JAR는 현재 설정에서 직접 참조하므로 유지한다.

[저장소 정리 기록](docs/CLEANUP.md)에 삭제 범위와 보존 기준을 기록했다. 평가 정답인 `.out`, 논문 PDF, 원본 실험 로그는 보존 대상이다.
