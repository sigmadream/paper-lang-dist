# N01 시계 역행 중단 기록 보존 수정 보고

최종 재검토서 `final-re-review.md`, `re-review-reproductions.json`의 `new_clock_abort_persistence`, 원검토 로그를 읽고 동일한 연속 충돌을 실패 테스트로 재현한 뒤 수정하였습니다. 공급자 파일이나 다른 담당 소스는 변경하지 않았으며 API 호출·자격 증명 열람·git add·commit·하위 작업자 생성은 수행하지 않았습니다.

## 변경 파일과 원인

- `src/rttdist/hops_experiment.py`
- `tests/integration/test_hops_clock_abort.py`

기존 응답 없는 조기 중단 분기는 시계 역행을 감지한 뒤 상태를 중단하고 반복을 종료하였지만, 영구 저장은 마지막 observation.json에 의존하였습니다. 해당 저장이 충돌하고 다음 시각이 이전 체크포인트보다 커지면 시계 역행 감지가 사라졌습니다. 기존 응답·처리 캐시가 있는 분기는 checkpoint에서 사유를 저장하여 같은 증상이 나타나지 않았습니다.

## 최소 수정

시계 역행을 감지하면 반복 진입과 상태 중단 전에 관측 폴더의 `clock_abort.json`에 `reason=observation_clock_unavailable`을 기록합니다. 기존 `write_json`의 임시 파일·원자적 교체를 사용하며 최종 관측 저장과 독립된 기록입니다.

이후 재개는 이 표식의 존재를 시계 신뢰 불가 상태에 포함합니다. 따라서 timing.json의 이전 체크포인트보다 새 시각이 커지더라도 중단 사실이 유지됩니다. 이미 확정한 단계는 기존 결정 파일로 복원하고, 새 요청은 허용하지 않습니다. 기존 상태 전이·공급자·평가·비용 처리 구조는 유지하였습니다.

## 실패에서 통과로 전환한 검증

최초 테스트는 여섯 사례 중 두 개 실패·네 개 통과였습니다. 실패한 두 사례는 확정 단계가 한 홉 또는 두 홉이고 다음 단계 응답이 없는 경우입니다. 저장 응답 또는 processed가 존재하는 네 대조 사례는 기존에도 통과하였습니다.

테스트는 다음 순서를 실제 임시 파일과 모의 시계·공급자로 수행합니다.

1. 시각 100에서 한 홉 또는 두 홉의 유효 결정과 공급자 응답을 저장한 뒤 충돌시킵니다. 대조 사례에서는 다음 단계의 응답 또는 처리 캐시 저장 직후 충돌시킵니다.
2. 시각 0으로 재개하여 시계 역행 중단을 확인하고, 최종 observation.json을 저장하기 직전에 다시 충돌시킵니다.
3. 시각 101로 다시 재개하고 같은 최종 저장 충돌을 반복합니다. 중단 사유가 계속 유지되며 추가 공급자 호출은 없습니다.
4. 시각 102에서 최종 저장을 허용한 뒤 한 번 더 재개합니다. 중단 사유와 기존 임계치 판정이 동일하며 공급자 호출 수가 늘지 않습니다.

수정 후 여섯 사례가 모두 통과하였습니다. 기존 공급자 응답 파일과 유효 decision 파일의 바이트가 그대로 유지되고, 총 비용이 저장된 호출 수×0.25와 일치하는 것도 확인하였습니다. 두 홉에서 이미 확정한 주 임계치 성공은 보존하고, 미도달 임계치는 invalid로 유지합니다.

## 실행 명령과 결과

```powershell
uv run --no-sync pytest tests/integration/test_hops_clock_abort.py -q --tb=short
```

- 수정 전: 2 failed, 4 passed, 종료 코드 1
- 수정 후: 6 passed, 종료 코드 0
- 로그: `core-n01-red.log`, `core-n01-green.log`

```powershell
uv run --no-sync pytest tests/integration/test_hops_clock_abort.py tests/integration/test_hops_deadlines.py tests/integration/test_hops_resume.py tests/unit/test_hops_state.py tests/unit/test_fps_state.py -q --tb=short
uv run --no-sync black --check src/rttdist/hops_experiment.py tests/integration/test_hops_clock_abort.py
```

- 관련 회귀: 57 passed, 실패 0개, 종료 코드 0
- black: 두 파일 통과, 종료 코드 0
- 회귀 로그: `core-n01-regression.log`

## 계약 변경과 한계

core 소스 변경으로 기존 실행 계약의 구현 해시가 바뀝니다. 기존 계약은 자동 승격하지 않으며, 이전 코드 계약으로 새 코드를 재개하려 하면 기존 계약 검사에서 거부됩니다.

이 수정은 확인된 시계 역행 중단 사실의 보존에 한정합니다. 별도 호스트·부팅 식별이나 시간 기준 지원을 추가하지 않았으며, 진행 중인 외부 작업의 강제 종료도 추가하지 않았습니다. 전체 pytest와 후속 독립 검토는 조정자 지시에 따라 실행하지 않고 남겨두었습니다.
