# 보고 단계 통과율 P2 수정 근거

검토 대상은 `final-independent-review.md`의 마지막 P2와 `final-review-additional.log`의 `compile_timeout_stage_rates`입니다. 실제 평가기·홉 상태·보고 집계를 대조한 뒤 실패 재현 테스트를 먼저 실행하고 최소 수정하였습니다.

## 원인과 변경

`fps_execution.evaluate`는 `compile_timeout`을 확정된 평가 실패로 기록하지만 `hops_reporting._stage_rates`의 판정 가능 상태 목록에서 빠져 있었습니다. 따라서 기능 실패가 미확인으로 분류되어 단계 통과율 분모에서 제외되었습니다. 구현 변경은 `src/rttdist/hops_reporting.py:150`의 판정 가능 상태에 `compile_timeout` 한 항목을 추가한 것입니다. 평가기와 상태 전이 코드는 수정하지 않았습니다.

| 상태 | 실제 평가기 발생 위치 | 수정 후 단계 집계 |
| --- | --- | --- |
| `compile_timeout` | fps_execution.py:71 | 실패, 판정 가능 분모 포함 |
| `compile_error` | fps_execution.py:72 | 기존과 같이 실패, 판정 가능 분모 포함 |
| `timeout` | fps_execution.py:76 | 기존과 같이 실패, 판정 가능 분모 포함 |
| `runtime_error` | fps_execution.py:76 | 기존과 같이 실패, 판정 가능 분모 포함 |
| `wrong_answer` | fps_execution.py:77 | 기존과 같이 실패, 판정 가능 분모 포함 |
| `success` | fps_execution.py:70·77 | 기존과 같이 성공, 판정 가능 분모 포함 |
| `infrastructure_error` | core의 기반시설 오류 정규화 | 기존과 같이 unavailable, 판정 가능 분모 제외 |

평가기에서 직접 생성하는 기능 실패는 위 다섯 종류이며 다른 누락은 없었습니다. 기존에 허용된 `compilation_error`와 `format_error` 처리도 유지하였습니다. 탐색과 추가 확인 단계에 같은 규칙을 적용합니다.

## 실패 재현과 통과

다음 검사를 구현 변경 전에 실행하였습니다.

```powershell
uv run --no-sync pytest tests/unit/test_hops_reporting.py::test_evaluator_functional_failures_count_in_stage_denominator tests/unit/test_hops_reporting.py::test_infrastructure_stage_is_unavailable_and_calls_are_not_hops tests/integration/test_v16_report.py::test_evaluator_compile_timeout_remains_assessed_failure_in_report -q
```

실제 결과는 `3 failed, 9 passed, 64 warnings in 1.66s`였습니다. 실패 세 건은 탐색의 compile_timeout, 확인의 compile_timeout, 실제 평가기 결과를 내보낸 보고 CSV의 분모 누락입니다. 다른 기능 실패 여덟 조합과 기반시설 오류 한 건은 수정 전에도 통과하였습니다.

실패 시 실제 집계는 `attempts=1, assessable=0, unavailable=1, passed=0, pass_rate=None`이었으며, CSV에는 assessable=0·unavailable=1·빈 pass_rate가 기록되었습니다. 수정 후 같은 명령은 `12 passed, 64 warnings in 1.34s`로 통과하였습니다. 수정 후 compile_timeout 집계는 다음과 같습니다.

```json
{
  "attempts": 1,
  "assessable": 1,
  "unavailable": 0,
  "passed": 0,
  "pass_rate": 0.0
}
```

단위 검사는 실제 평가기 기능 실패 다섯 종류×탐색/확인 두 구간의 10개 조합을 확인합니다. 기존 기반시설 오류 검사에도 attempts·passed·결측 통과율 확인을 추가하였습니다.

통합 검사는 실제 `fps_execution.evaluate`를 호출하되 외부 프로세스 실행 함수만 모의하여 compile_timeout을 생성합니다. 이 평가 결과를 summary와 보고기의 실제 `stages.csv`까지 전달하고 attempts=1·assessable=1·unavailable=0·passed=0·pass_rate=0.0을 확인합니다. 실제 컴파일러·API·SDK는 호출하지 않았습니다.

## 최종 회귀와 서식

```powershell
uv run --no-sync black src/rttdist/hops_reporting.py tests/unit/test_hops_reporting.py tests/integration/test_v16_report.py
uv run --no-sync black --check src/rttdist/hops_reporting.py tests/unit/test_hops_reporting.py tests/integration/test_v16_report.py
uv run --no-sync pytest tests/unit/test_hops_reporting.py tests/unit/test_fps_reporting.py tests/integration/test_v16_report.py -q
```

black 최종 검사는 3개 파일 모두 변경 불필요로 통과하였습니다. 관련 회귀는 `39 passed, 966 warnings in 8.66s`로 통과하였습니다. 신규 보고 단위 27개·기존 FPS 회귀 5개·보고 통합 7개이며 기존 FPS 집계 코드는 수정하지 않았습니다.

경고 966개는 기존에 확인한 Matplotlib Agg 문자 렌더링의 float x/y 사용중단 경고입니다. 이번 추가 보고 생성 검사에서 64개가 더 발생하여 기존 보고 통합의 902개와 합쳐졌으며, 경고 억제 옵션·필터를 추가하지 않았습니다. 해당 경고는 테스트 실패와 구분합니다.

## 변경 범위와 남은 작업

- `src/rttdist/hops_reporting.py`: 판정 가능 상태 한 항목 추가
- `tests/unit/test_hops_reporting.py`: 실패 상태 10조합과 기반시설 오류 분모 회귀
- `tests/integration/test_v16_report.py`: 실제 평가기→summary→CSV 연결 회귀
- 이 수정 근거 문서

이번 P2 수정의 미완료 항목은 없습니다. 공유 작업본의 core 시간 제한·동결 수정 및 provider 작업과 함께 실행하는 전체 pytest는 요청대로 조정자의 최종검사로 남겨 두었습니다. 실제 API 호출·인증 열람·git add/commit·새 worktree·하위 작업자 생성은 수행하지 않았습니다.
