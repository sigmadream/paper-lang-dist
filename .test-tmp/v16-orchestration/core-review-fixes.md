# core 독립 검토 결함 수정 보고

독립 검토 보고서와 재현 로그를 읽고 담당 결함 세 건을 수정하였습니다. 수정은 core 파일과 관련 테스트에 한정하였으며 공급자 파일·코퍼스 검증기·독립 계산기 소스는 변경하지 않았습니다. 실제 API 호출, 자격 증명 열람, git add·commit, 하위 작업자 생성은 수행하지 않았습니다.

## 수정 파일

- `src/rttdist/hops_experiment.py`
- `tests/integration/test_hops_deadlines.py`
- `tests/integration/test_v16_freeze.py`
- `tests/unit/test_hops_validation_provenance.py`

## 시간 제한과 재개

공급자 응답 수신 후, 기능 평가 후, 인접 유사도 후, 원본 유사도 후에 경과 시간을 검사합니다. 처리 결과 저장이 끝난 뒤 상태 전이 직전에도 검사합니다. 10번째 탐색 단계와 12번째 확인 단계를 포함하여 제한을 넘긴 결과는 새 도달·확인 통과로 인정하지 않습니다. 기존에 확정한 임계치 결과와 확인 결과는 보존합니다.

처리 근거는 `processed.json`, 상태 반영 직전 최종 판정은 별도 `decision.json`에 원자적으로 기록합니다. 최종 판정이 없는 처리 캐시는 재개 시 현재 예산 아래에서 다시 판정하며, 저장된 최종 판정이 있으면 그 결과를 복원합니다. 따라서 처리 결과만 재생하여 제한을 우회할 수 없습니다. 시간 초과 응답의 원문·사용량·비용과 단계 기록은 보존하며, 저장된 응답을 다시 생성하거나 과금하지 않습니다.

단계별·관측별 시간 체크포인트에 단조 시각을 기록하여 충돌부터 재개까지 경과한 시간도 계산합니다. 10홉 확정 직후 충돌한 경우에도 다음 확인 구간의 300초 예산이 새로 시작하지 않습니다. 재개 시 시계가 과거로 바뀌어 경과 시간을 신뢰할 수 없으면 `observation_clock_unavailable`로 중단하며, 이 사유도 다음 재개에 유지합니다.

최초 시간 제한 재현은 16개 모두 실패하였습니다. 2·4·10·12홉에서 응답·평가·인접 측정·원본 측정을 각각 늦추는 입력을 사용하였고, 이미 도달한 임계치 보존·후속 확인 미확인·응답 비용 보존·처리 캐시 재개 시 추가 호출 없음까지 검증하였습니다. 추가로 10홉 저장 후 충돌, 평가 중 충돌 후 원응답 재사용, 시계 초기화와 연속 재개, 처리 캐시 저장 중 제한 초과를 재현하여 보완하였습니다.

## 파일럿의 분석 완전성

동결은 12개 관측의 구조 감사와 별도로 설정의 세 임계치 모두에서 `complete_by_threshold` 값이 참인지 요구합니다. 필드 누락과 단일 임계치의 불완전성도 거부합니다. 기능 실패와 hop_limit은 유효한 관측 결과이므로 성공률이나 순위를 동결 조건으로 사용하지 않습니다.

최초 재현에서 불완전성 다섯 경우와 모두 invalid인 실제 캠페인 감사→동결 연결 한 경우가 실패하였고, 기능 실패만 있는 유효한 캠페인 연결은 통과하였습니다. 수정 후에는 12개 모두 invalid인 실제 캠페인의 구조 감사가 참이어도 동결을 거부하고, 기능 실패만 있는 12개 유효 관측은 동결을 허용합니다.

## 검증기·독립 계산기 근거

검증 자료의 `validator_source_hashes`를 알려진 준비·검증 스크립트 두 파일의 현재 해시와 완전히 대조합니다. `independent_checks.source_hashes`도 알려진 독립 계산기 두 파일의 현재 해시와 완전히 대조합니다. 자료에 적힌 임의 경로를 읽지 않으며 해시 일부만 제공하거나 다른 경로를 지정하면 거부합니다.

독립 검증의 전체 통과 여부와 195개 기록을 확인하고, 실제 15문제×13개 평가 입력의 사례 집합과 일치하는지 검사합니다. 중복·누락·추가·알 수 없는 사례, 사례별 실패·오류, 계산 방법 근거 누락을 거부합니다. 입력 바이트 해시, 정답 바이트 해시, 정규화된 정답과 독립 계산 결과의 해시도 대조합니다.

준비·검증 스크립트와 독립 계산기 네 파일을 실행 계약의 구현 해시에 포함하였습니다. 검증기 또는 계산기 해시가 달라지면 계약 해시가 달라지며, 오래된 검증 자료로 동결·캠페인 재개를 시도하면 거부합니다.

최초 재현에서 잘못된 소스 계약·독립 근거 18개와 구현 해시 누락 한 경우가 모두 실패하였습니다. 수정 후에는 이 입력을 모두 거부하며, 별도 테스트로 현재 소스 해시 변경이 계약·동결·재개에 연결되는지 확인하였습니다. 기존 동결 테스트의 정상 모의 검증 자료도 195개 명시적 근거를 제공하도록 보완하였습니다.

현재 저장된 실제 코퍼스 검증 자료도 새 관문을 통과하였습니다. 확인된 저장 근거는 기준 구현 75개, 실행 평가 975개, 독립 근거 195개이며 이는 이번에 해당 평가 전체를 다시 실행했다는 의미는 아닙니다. 대조 결과와 소스 해시는 `core-review-validation-existing.json`에 보존하였습니다.

## 검증 명령과 증거

최종 관련 회귀검사는 178개 통과·실패 0개이며, black 검사도 수정 Python 파일 네 개에서 통과하였습니다. 보고 생성기의 기존 Matplotlib 사용 중단 예정 경고 200개는 별도로 출력되었으며 경고 필터를 추가하지 않았습니다.

```powershell
uv run --no-sync pytest tests/integration/test_hops_deadlines.py -q --tb=short
uv run --no-sync pytest tests/integration/test_v16_freeze.py -q --tb=short
uv run --no-sync pytest tests/unit/test_hops_validation_provenance.py -q --tb=short
uv run --no-sync black --check src/rttdist/hops_experiment.py tests/integration/test_hops_deadlines.py tests/integration/test_v16_freeze.py tests/unit/test_hops_validation_provenance.py
```

관련 회귀검사 명령은 다음과 같습니다. 전체 pytest는 조정자의 통합 검증을 위해 실행하지 않았습니다.

```powershell
uv run --no-sync pytest tests/unit/test_hops_config.py tests/unit/test_hops_state.py tests/unit/test_hops_validation_provenance.py tests/unit/test_fps_state.py tests/integration/test_hops_experiment.py tests/integration/test_hops_resume.py tests/integration/test_hops_deadlines.py tests/integration/test_v16_freeze.py tests/integration/test_hops_cli.py tests/integration/test_cli.py tests/unit/test_fps_providers.py tests/integration/test_provider_factory.py tests/unit/test_fps_reporting.py tests/integration/test_v16_providers.py -q --tb=short
```

- 시간 제한 최초 실패: `core-deadlines-red.log`
- 파일럿 완전성 최초 실패: `core-pilot-completeness-red.log`
- 검증 근거 최초 실패: `core-validation-provenance-red.log`
- 검증 근거와 동결의 중간 회귀 44개 통과: `core-validation-provenance-green.log`
- 최종 관련 회귀 출력: `core-review-fixes-regression.log`

## 기존 계약과 남은 제한

core 구현 변경과 검증 소스 네 파일의 해시 추가로 기존 실행 계약 해시가 바뀝니다. 기존 계약으로 새 코드를 재개하거나 기존 본 실험 동결 파일을 그대로 사용하는 것은 거부되므로, 수정된 코드로 새 campaign과 파일럿·동결 근거를 생성해 주셔야 합니다. 원자료와 과거 계약을 자동으로 덮어쓰거나 새 계약으로 승격하지 않습니다.

시간 검사는 각 호출·도구 작업이 반환된 뒤 적용합니다. 이미 진행 중인 외부 호출·하위 프로세스를 관측 예산 시점에 강제 종료하는 구현은 추가하지 않았으며, 늦게 반환된 결과의 새 성공 인정을 차단하고 근거·비용을 보존합니다.

수정 후 전체 통합 검사와 독립 재검토는 조정자께서 이어가십니다. 실제 공급자 접속과 실험은 이 작업에서 수행하지 않았습니다.
