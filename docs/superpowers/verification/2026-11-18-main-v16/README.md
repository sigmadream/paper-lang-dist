# v1.6 실험 자료 통합과 복원

## 보존 범위

| 범위 | 보존 파일 | 원본 바이트 |
| --- | ---: | ---: |
| .env.example | 1 | 784 |
| .test-tmp | 114 | 633,767 |
| artifacts-rtt-v1.6 | 137,156 | 10,185,952,646 |
| configs | 18 | 23,966 |
| data | 692 | 3,556,001 |
| docs | 4 | 76,294 |
| papers | 64 | 60,504 |
| pyproject.toml | 1 | 865 |
| scripts | 13 | 162,601 |
| src | 8 | 169,080 |
| tests | 31 | 215,583 |
| uv.lock | 1 | 167,743 |
| 전체 | 138,103 | 10,191,019,834 |

응답 원문과 정규화 응답, 생성 소스, 관측·평가·JPlag 산출물, 실행 로그, 원장과 계약, 동결 소스 및 공식 보고·재현 묶음, 기준 코퍼스를 보존했습니다. 과거 해시 지도와 Flash 최신 인계 목록에서 지정한 컴파일 파생물은 해당 원장의 재검증을 위해 보존했습니다. 필수 임시 검토 기록은 인계 목록의 명시 경로와 문서·해시 지도의 참조를 따라 선택하여 원래 경로 그대로 저장했습니다.

## 제외 범위

- 환경 또는 캐시 디렉터리 596경로
- 현재 자료에서 참조되지 않은 임시 작업 결과 754경로
- 저장 코드와 도구로 재생성할 수 있는 컴파일 파생물 85경로

인증 파일과 개인 환경, Python 바이트코드 및 캐시를 커밋 범위에서 제외했습니다. 참조 근거에 사용되지 않은 선택적 컴파일 결과는 저장된 코드와 도구로 재생성할 수 있습니다. 제외된 파일은 기존 작업 위치에 보존됩니다. 키나 개인키 형식의 탐지 근거는 경로 단위로만 기록합니다.

## 큰 원본 복원

| 복원할 원본 경로 | 원본 바이트 | 조각 수 | 압축 바이트 |
| --- | ---: | ---: | ---: |
| artifacts-rtt-v1.6/live-commandcode-20261117/commandcode-glm53-v16-20261117/main/report/reproducibility_bundle/observations.json | 143,805,076 | 1 | 6,560,037 |
| artifacts-rtt-v1.6/live-commandcode-20261117/commandcode-glm53-v16-20261117/main/report/summary.json | 146,811,750 | 1 | 6,671,248 |
| artifacts-rtt-v1.6/live-commandcode-20261117/commandcode-glm53-v16-20261117/main/summary.json | 146,811,750 | 1 | 6,706,468 |
| artifacts-rtt-v1.6/live-ds41f-20261118/commandcode-ds41-flash-v16-20261118/main/report/reproducibility_bundle/observations.json | 197,422,514 | 1 | 10,292,518 |
| artifacts-rtt-v1.6/live-ds41f-20261118/commandcode-ds41-flash-v16-20261118/main/report/summary.json | 201,611,028 | 1 | 10,428,392 |
| artifacts-rtt-v1.6/live-ds41f-20261118/commandcode-ds41-flash-v16-20261118/main/summary.json | 201,611,028 | 1 | 10,466,276 |

Git 단일 파일 한도에 가까운 보존 원본은 gzip 조각으로 나누어 저장했습니다. 압축 조각의 순서, 크기와 SHA-256 및 원본의 SHA-256은 인벤토리의 분할 보관 항목을 확인해 주십시오. 저장소 루트에서 아래 명령을 실행하면 모든 원본을 원래 경로로 복원합니다. 경로를 인수로 주면 해당 원본만 복원합니다. 기존 파일은 해시를 검사하여 그대로 두며, 해시가 다르면 오류로 종료합니다.

```powershell
uv run --no-sync python scripts/restore_v16_preservation.py
```

기존 실험 인벤토리와 동결 manifest에는 원래 경로와 원래 해시가 유지됩니다. 요약 JSON, 재현 입력 등의 원래 경로를 참조하는 명령은 복원 후 실행해 주십시오.

## 검증 결과

1. 기존 감사·동결·재현 지도와 새 인계 목록에서 SHA-256 참조 388,334건을 원본 및 동결 사본과 대조했습니다. 현재 공유 코드로 개정된 과거 소스는 당시 사본의 위치와 해당 해시를 인벤토리에 기록했습니다.
2. 저장 대상 바이트와 선택된 로그의 인증값·인증 패턴 감사를 수행했습니다. .env.example의 자격 증명 항목은 비어 있습니다. 기존 실험의 비밀정보 감사 결과도 보존합니다.
3. 직접 저장하는 파일은 Git blob을 계산해 인덱스와 대조했습니다. 분할 보관 대상은 조각을 다시 연결한 뒤 압축을 풀어 원본 SHA-256을 대조했습니다.
4. 전체 pytest 557개 통과, 종료 코드 0을 확인했습니다. 경고 1,166개는 Matplotlib 사용 중단 예정 경고입니다. 변경 Python 파일 46개의 black 검사는 종료 코드 0입니다.

[통합 인벤토리와 해시](inventory.json), [pytest 실제 원출력](pytest.log), [pytest 종료 코드](pytest.exitcode), [Python 서식 검사 원출력](black.log)

## 별도 체크아웃의 계약 검사

현재 작업 공간에서 전체 검사를 통과한 뒤 별도 main 체크아웃에서 첫 재검사를 실행했습니다. 동결 YAML에 기록한 Orca 호스트의 절대 출력 경로가 현재 체크아웃의 출력 경로와 달라 계약 검사 두 건이 실패했습니다. 최초 재검사는 종료 코드 1, 555개 통과, 2개 실패였습니다. [최초 main 재검사 원출력](pytest-main-initial.log), [종료 코드](pytest-main-initial.exitcode)

- `tests/integration/test_deepseek_flash_runner.py::test_new_campaign_keeps_problem_protocol_and_uses_api_provider`
- `tests/integration/test_deepseek_restart_runner.py::test_new_campaign_keeps_problem_protocol_and_uses_api_provider`

[추가 pytest 픽스처](../../../../tests/integration/conftest.py)는 위 두 테스트에서만 동결된 출력 경로의 마지막 두 구성 요소를 실제 캠페인 경로와 대조한 뒤 시험용 출력 루트를 현재 체크아웃과 맞춥니다. 스케줄, 정확 모델·공급자·생성 옵션·예산 검사는 기존 코드로 실행합니다. 기존 실행기와 동결 테스트 파일, YAML, 검토 자료는 기존 바이트 그대로 보존하며 실제 실행기의 출력 경로 관문도 유지됩니다.

보완 후 Orca와 main 양쪽에서 전체 pytest를 각각 다시 실행하여 557개 통과, Matplotlib 경고 1,166개, 종료 코드 0을 확인했습니다. 양쪽에서 세 실행 소스 manifest의 195개 참조를 확인했습니다. 이전 GLM 공유 코드의 당시 버전 두 파일은 각 체크아웃의 동결 사본과 일치했습니다. [Orca 재검사 로그](pytest-orca-final.log), [Orca 종료 코드](pytest-orca-final.exitcode), [main 재검사 로그](pytest-main-final.log), [main 종료 코드](pytest-main-final.exitcode), [픽스처 보완 범위와 SHA-256 확인](checkout-fixture-hashes.json)
