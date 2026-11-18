# Command Code 두 모델 실제 API 연동 검증

검증일은 2026-11-17입니다. GLM-5.3과 DeepSeek V4 Pro 모두 인증·OK 응답, 정확한 모델 ID 확인, C++→Python→C++ 및 C++→Haskell→C++ 생성과 단계별 13개 평가를 통과했습니다. 두 모델 합계 10개 논리 요청·10개 전송을 수행했으며 재시도는 없었습니다. 8개 생성물의 총 104개 사례가 모두 통과했습니다.

이 자료의 phase는 `integration_smoke`이며 `main_reusable=false`입니다. 본 실험·12슬롯 파일럿 전체·본 실험 동결·고정점 판정·통계 분석은 수행하지 않았습니다. 이 결과는 해당 두 문제의 기능 검사와 공급자 연결 근거이며 모델 간 우열이나 본 실험 완료를 뜻하지 않습니다.

## 모델·주소·옵션 근거

[Command Code 공급자 문서](https://commandcode.ai/docs/provider)와 공개 [실시간 모델 목록](https://api.commandcode.ai/provider/v1/models)에서 아래 모델 ID 및 `/chat/completions`, `/responses` 지원을 확인했습니다. 확인한 두 모델의 목록은 [catalog.json](catalog.json)에 저장했습니다. 생성 요청은 모두 `https://api.commandcode.ai/provider/v1/chat/completions`에 보냈습니다.

| 대상 | 요청 ID | 응답 ID | 모델 검증 |
|---|---|---|---|
| GLM-5.3 | `zai-org/GLM-5.3` | `zai-org/GLM-5.3` | 5개 응답 모두 exact |
| DeepSeek V4 Pro | `deepseek/deepseek-v4-pro` | `deepseek/deepseek-v4-pro` | 5개 응답 모두 exact |

Flash 모델이나 자동 대체는 사용하지 않았습니다. 설정에는 공식 원 공급자의 짧은 모델 이름만 명시적 별칭으로 허용했으나 이번에는 별칭을 사용한 응답도 없었습니다. 두 모델의 10개 응답은 모두 `finish_reason=stop`이며 HTTP 오류나 불명 시간 초과는 없었습니다.

연동 점검 프로파일의 번역 출력 상한은 4096, OK 요청 출력 상한은 1024이며 요청 `reasoning_effort`는 `low`입니다. [DeepSeek 공식 문서](https://api-docs.deepseek.com/guides/thinking_mode/)의 V4 Pro 추론 옵션과 [Z.AI 공식 문서](https://docs.z.ai/guides/capabilities/thinking-mode)의 GLM-5.3 추론 제약을 확인했습니다. 두 모델에 같은 low를 요청했다고 동일한 실제 추론량이라고 해석하지 않습니다. 서버가 실효 생성 설정을 보고하지 않아 `effective_generation`은 null입니다.

본 실험 공통 설정의 출력 상한 16384·temperature 0.6·top_p 0.95·seed와 다릅니다. 점검 설정은 temperature·top_p·seed를 요청하지 않으며, 특히 DeepSeek의 추론 모드에서는 temperature와 top_p가 적용되지 않을 수 있다는 공식 제약을 고려했습니다. 이 프로파일을 본 실험의 동등 조건으로 재사용하지 않습니다.

## 실제 평가 결과

| 모델 | 문제·왕복 경로 | 중간 언어 | 복원 C++ | 결과 |
|---|---|---|---|---|
| GLM-5.3 | LC_0053, C++→Python→C++ | 13/13 | 13/13 | 통과 |
| GLM-5.3 | IPOP_1992 쿼드트리, C++→Haskell→C++ | 13/13 | 13/13 | 통과 |
| DeepSeek V4 Pro | LC_0053, C++→Python→C++ | 13/13 | 13/13 | 통과 |
| DeepSeek V4 Pro | IPOP_1992 쿼드트리, C++→Haskell→C++ | 13/13 | 13/13 | 통과 |

각 단계는 단일 코드 추출, 실제 컴파일 또는 구문 검사, 고정된 13개 평가 입력 실행을 거쳤습니다. 사례 제한 5초·컴파일 제한 180초와 공통 설정의 실제 C++·Python·GHC 경로를 사용했습니다. 모델에는 명세·최대 2개 공개 예제·현재 소스만 전달했으며 13개 비공개 평가 입력이나 정답은 전달하지 않았습니다. 복원 요청에는 직전 생성 소스를 사용했습니다.

요약은 [summary.json](summary.json), 독립적으로 원문 응답·장부·평가 파일을 다시 읽어 집계한 대조표는 [verification.json](verification.json)에 있습니다. 모델별 세부 결과는 [GLM 결과](glm53/result.json)와 [DeepSeek 결과](deepseek_v4_pro/result.json)에 있습니다. 각 모델 폴더에는 `preflight/response.json`, 문제별 `step-01/02/response_body.txt`, 정규화 `response.json`, `source.*`, `evaluation/evaluation.json`과 컴파일·실행 산출물이 있습니다. 응답 ID·모델 근거·사용량·요청 및 전송 설정·원문 경로도 보존했습니다.

## 호출·사용량·비용

| 모델 | 논리 요청/상한 | 전송/상한 | 입력 토큰 | 출력 토큰 | 장부 비용 추정(USD) |
|---|---|---|---|---|---|
| GLM-5.3 | 5/6 | 5/6 | 2760 | 830 | 0.00707824 |
| DeepSeek V4 Pro | 5/6 | 5/6 | 2585 | 2851 | 0.01470216 |
| 합계 | 10/12 | 10/12 | 5345 | 3681 | 0.02178040 |

요청 구성은 모델마다 OK 점검 1개와 번역 4개입니다. 실제 수신 횟수와 장부의 전송 기록도 각각 5개이며 재생 응답은 추가 과금으로 기록하지 않았습니다. GLM의 API 지연 합계는 약 8.57초, DeepSeek는 약 40.31초이며 컴파일·평가 시간을 포함한 전체 경과 시간과 구분합니다.

[공식 단가 문서](https://commandcode.ai/docs/resources/pricing-limits)에 따라 GLM은 백만 토큰당 입력 1.40달러·출력 4.40달러·캐시 입력 0.26달러를 사용했습니다. DeepSeek는 비혼잡 시간 할인 단가 대신 보수적인 피크 입력 1.32달러·출력 3.96달러·캐시 입력 0.044달러를 적용했습니다. 실제 응답의 사용량과 캐시 토큰을 바탕으로 계산했으며 모든 장부의 `cost_source`는 `estimated`입니다. 공급자 응답은 달러 청구액을 보고하지 않았으므로 실제 계정 청구액으로 단정하지 않습니다.

각 모델의 별도 공유 장부에 1달러 상한·요청별 0.15달러 예약·최대 6개 논리 요청·최대 6개 전송·재시도 0을 적용했습니다. 두 모델 합계 달러 상한은 2달러이며, 최대 12개 요청의 명시적 예약 합계도 1.8달러입니다. 최대 입력은 보수적 바이트 기반 16384토큰, 번역 출력은 4096토큰으로 제한했습니다. 불명 응답은 자동 재생성하지 않도록 기존 어댑터의 보호를 유지했습니다.

장부는 [GLM 장부](glm53/provider_ledger.jsonl)와 [DeepSeek 장부](deepseek_v4_pro/provider_ledger.jsonl)에 있으며 예약·전송 상태는 인접 `.state.json` 파일에 있습니다. 사용량·비용 추정 누락 요청은 0개입니다.

## 인증 보호와 로컬 오류 수정

인증값은 사용자께서 지정하신 원본 `.env`를 `uv run --env-file`로 하위 프로세스에만 주입했습니다. 키·인증 헤더·환경 파일 내용은 출력하거나 복사하지 않았습니다. 점검 프로세스는 키를 메모리에 보관하고 실제 API 요청 동안에만 명명된 환경 변수에 두었습니다. 생성 프로그램과 컴파일러에는 인증 환경을 상속하지 않도록 환경을 제한했습니다.

첫 GLM 실행은 실제 API 5회와 52개 기능 평가가 모두 통과한 뒤, 마지막 비밀정보 검사에서 Windows의 1바이트 잠금 파일을 읽으려 하여 `PermissionError`로 종료했습니다. 이는 모델·API·과금 실패가 아닌 점검 스크립트의 로컬 오류였습니다. 잠금 파일을 포함한 크기가 작은 파일을 읽지 않도록 수정했고, 실패 재현 테스트를 통과시켰습니다. 이후 재개에서는 저장된 GLM 응답과 평가 캐시를 재사용하여 GLM API를 추가 호출하지 않았습니다. 두 번째 실행에서 DeepSeek의 새 5회만 전송했습니다.

완료 시 전체 저장 자료를 실제 키의 바이트열로 검사하여 유출 없음(`secret_audit_passed=true`)을 확인했습니다. API 오류는 없으므로 HTTP 오류 원인 분류나 재시도는 실제로 발생하지 않았습니다. 향후 오류가 발생하면 HTTP 상태·표준화된 원인·자동 재시도 불가 여부만 기록하고 응답 불명 요청은 재생성하지 않습니다.

## 실행 명령과 회귀 검증

실제 최초 실행 명령은 다음과 같습니다. GLM의 마지막 로컬 검사 오류는 위에 별도로 기록했습니다.

```powershell
uv run --env-file 'C:/Users/sigma/works/paper-lang-dist/.env' --no-sync python scripts/integration_commandcode.py --model glm53
```

수정 후 GLM 캐시 재개와 DeepSeek의 새 실제 호출을 수행한 명령은 다음과 같으며 종료 코드 0, 두 모델 모두 통과를 반환했습니다.

```powershell
uv run --env-file 'C:/Users/sigma/works/paper-lang-dist/.env' --no-sync python scripts/integration_commandcode.py --model all
```

`uv run --no-sync pytest tests/unit/test_provider_protocols.py tests/unit/test_provider_ledger.py tests/unit/test_v16_model_config.py tests/integration/test_provider_recovery.py tests/integration/test_v16_providers.py tests/integration/test_commandcode_smoke.py tests/unit/test_fps_providers.py tests/integration/test_provider_factory.py tests/integration/test_fps_experiment.py -q`는 66개 모두 통과했습니다. 새 테스트는 요청 5개 제한, Flash·과도한 호출 예산 거부, 평가 프로세스의 키 비상속, 잠금 파일을 포함한 비밀정보 검사와 유출 탐지를 검증합니다.

`uv run --no-sync black --check scripts/integration_commandcode.py tests/integration/test_commandcode_smoke.py`는 2개 파일 모두 통과했습니다. 전체 오프라인 `uv run --no-sync pytest -q`는 392개 통과·실패 0개·기존 Matplotlib 관련 경고 1102개였으며 92.77초가 걸렸습니다. 결과는 [offline-regression.txt](offline-regression.txt)에 있습니다. 회귀 테스트에는 실제 인증값을 주입하지 않았습니다. 이후 별도 담당자들의 core·보고기 수정이 진행 중임을 전달받았으므로 전체 변경의 최종 회귀 판정은 조정자가 다시 수행합니다.

## 실행 근거와 계약 분리

각 모델의 `smoke_contract.json`과 각 요청의 `request.json`에는 실행에 사용한 공급자 설정·요청값·runtime·phase를 보존했습니다. 각 평가 JSON의 계약에는 실제 평가 입력·출력 파일 해시와 생성 소스 해시가 있습니다. [source_evidence.json](source_evidence.json)에 10개 수신 시각·8개 평가 계약·Python 버전과 실행 관련 소스·설정·의존성 파일 12개의 SHA-256을 추가로 기록하고, 해당 내용을 `execution_sources/` 아래에 복사했습니다. 인증 파일이나 인증값은 포함하지 않았습니다.

이 소스 묶음은 실제 호출 완료 후 캡처한 자료라는 시점을 명시했습니다. GLM 최초 실행과 DeepSeek 실행 사이의 스크립트 수정은 마지막 비밀정보 검사의 잠금 파일 읽기 오류를 고친 내용이며 생성·평가 로직과 요청 계약은 같았습니다. 이번 독립 실행기는 `hops_experiment`의 캠페인 실행·동결이나 보고기 집계 함수를 호출하지 않습니다. 다른 담당자의 core·보고기 변경 전후 계약을 같은 본 실험 계약으로 간주하거나 이 연동 응답을 본 실험에 재사용하지 않습니다.

## 변경 파일과 남은 사항

- `configs/v1.6/providers/commandcode_glm53.yaml`
- `configs/v1.6/providers/commandcode_deepseek_v4_pro.yaml`
- `scripts/integration_commandcode.py`
- `tests/integration/test_commandcode_smoke.py`
- `artifacts-rtt-v1.6/integration-commandcode/`의 본 보고서·원문·생성물·평가·장부·검증 요약

공급자 공통 코드나 core·보고기의 동작은 변경하지 않았습니다. git commit과 새 worktree 생성도 수행하지 않았습니다. 이번 범위에서 두 모델의 실제 연동·왕복·13사례 평가 완료를 막는 연결 문제는 없습니다. 본 실험용 생성 프로파일 검증과 12슬롯 파일럿·본 실험 실행은 이번 작업에 포함하지 않았으며 수행하지 않았습니다.
