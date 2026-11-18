# GLM-5.3 보존 결과와 프로토콜 감사 안내

2026-11-17 사용자 지시에 따라 JPlag 측정 불가 3건을 이번 결과 정리에서는 실패로 집계하고 별도 사유로 표시했습니다. 해당 코드는 각 13개 기능 검사를 통과했지만 유사도 측정에 실패했으므로, 기능 실패와 구별하여 `measurement_failure`로 기록합니다. 이는 수집 후 확정한 집계 규칙이며 기존 동결 계약과 원관측은 보존합니다. HTTP 524 뒤 재전송의 감사 판정도 유지합니다. 아래 결과는 기술통계이며 확증적 결론으로 확대하지 않습니다. 추가 측정과 나머지 실험은 내일로 미루고 실제 API 실행은 중지 상태를 유지합니다.

## 캠페인과 근거 위치

- 캠페인: `commandcode-glm53-v16-20261117`
- 동결 계약: `ce8b51ee546d54b5e8eb15ee901ee689a40f410538f9bdbc7f6e6f4ae5b373ca`
- [본 실험 동결](commandcode-glm53-v16-20261117/main_design.json), [실행 계획](execution-plan.md), [실행 소스와 설정 해시](source-manifest.json), [동결 당시 소스 사본](execution-sources/)
- [본 실험 관측·생성물](commandcode-glm53-v16-20261117/main/), [수집 summary](commandcode-glm53-v16-20261117/main/summary.json), [구조·완전성 감사](commandcode-glm53-v16-20261117/main/completion_audit.json)
- [공식 보고 summary](commandcode-glm53-v16-20261117/main/report/summary.json), [공식 한국어 설명](commandcode-glm53-v16-20261117/main/report/summary.md), [임계치 표](commandcode-glm53-v16-20261117/main/report/thresholds.csv), [확인 표](commandcode-glm53-v16-20261117/main/report/confirmation.csv), [재귀군 표](commandcode-glm53-v16-20261117/main/report/recursive_groups.csv)
- [지표 그림](commandcode-glm53-v16-20261117/main/report/metrics.png), [지표 PDF](commandcode-glm53-v16-20261117/main/report/metrics.pdf), [프로토콜 그림](commandcode-glm53-v16-20261117/main/report/protocol.png), [그림 입력](commandcode-glm53-v16-20261117/main/report/figure_inputs.csv)
- [재현 결과](commandcode-glm53-v16-20261117/main/report/reproducibility.json), [재현 묶음](commandcode-glm53-v16-20261117/main/report/reproducibility_bundle/), [모델 증거](commandcode-glm53-v16-20261117/main/report/model_metadata.json), [호출·사용량 표](commandcode-glm53-v16-20261117/main/report/call_usage.csv)
- 원장: [사전 점검](commandcode-glm53-v16-20261117/preflight/provider_ledger.jsonl), [파일럿](commandcode-glm53-v16-20261117/pilot/provider_ledger.jsonl), [본 실험](commandcode-glm53-v16-20261117/main/provider_ledger.jsonl), [본 실험 상태](commandcode-glm53-v16-20261117/main/provider_ledger.jsonl.state.json)
- [524 사고 설명](incident-524.md), [전체 장부 감사 JSON](incident-524.json), [원관측과 감사 후 값의 연결](audit-derived.json), [감사 전후 임계치 표](glm53-audit-thresholds.csv), [감사 전후 확인 표](glm53-audit-confirmation.csv)
- [이번 실패 집계 규칙·원자료 해시·재계산 결과](glm53-failure-policy.json), [기존 판정·524 감사·이번 실패 집계 비교표](glm53-failure-policy-thresholds.csv)

기존 공식 summary·표·그림·관측·장부는 수정하지 않았습니다. 위 공식 보고서와 그림은 이번 실패 집계 규칙을 적용하기 전의 역사적 산출물입니다. 현재 요청을 반영한 수치는 이 문서와 별도 실패 집계 JSON·CSV를 사용해 주십시오. 기존 재현 검사는 저장 자료의 JSON·CSV·그림 입력 일치를 검증하여 통과했으며 이번 규칙 변경까지 검증한 것으로 표시하지 않습니다.

## 생성 조건과 관측 범위

요청 모델과 모든 정상응답 모델 ID는 `zai-org/GLM-5.3`으로 정확히 일치하였습니다. endpoint는 Command Code의 `/provider/v1/chat/completions`입니다. 요청은 temperature 0.6, top_p 0.95, max_tokens 16384, reasoning_effort low이며 seed는 지원 근거가 없어 보내지 않았습니다. 실효 생성 설정은 서버 미보고로 null입니다.

DeepSeek V4 Pro는 추론 모드의 공식 제약에 따라 temperature·top_p를 보내지 않는 별도 프로파일입니다. 같은 low는 같은 실효 추론량을 뜻하지 않습니다. 문제·프롬프트·평가·중단 규칙은 같지만 모델별 생성 조건은 다르므로 동등한 생성 조건의 모델 비교로 해석하지 않습니다. 기존 smoke 응답은 재사용하지 않았습니다.

파일럿은 12/12슬롯, 세 임계치 완전성과 구조 감사가 모두 참이었습니다. 본 실험은 15문제×4경로×5회로 300/300슬롯, 미저장 0, 구조 감사 통과입니다. 각 경로의 계획·저장은 75슬롯입니다. 이번 집계에서는 Haskell의 측정 실패 3건을 분모에 포함하여 주 임계치의 집계 분모를 72에서 75로 변경했습니다. 기존 동결 규칙의 분석 완전성 거짓 판정은 덮어쓰지 않습니다.

## 주 임계치 0.85의 경로별 기술통계

아래 표는 524 감사 판정에 사용자가 요청하신 측정 실패 3건의 실패 처리를 추가하여 재계산한 값입니다. P의 분모에는 기능 실패·홉 제한·이번 측정 실패를 포함하며, H는 성공 슬롯의 최초 도달 단계 평균, D는 반올림 전 H/P입니다. 성공이 없으면 H와 D는 결측입니다. 측정 실패를 포함해도 성공 횟수와 H는 바뀌지 않습니다.

| 경로 | 저장 n | 집계 분모 n | 성공 | P | H | D |
|---|---:|---:|---:|---:|---:|---:|
| C++→Python→C++ | 75 | 75 | 60 | 0.800000 | 4.866667 | 6.083333 |
| C++→Java→C++ | 75 | 75 | 47 | 0.626667 | 5.191489 | 8.284292 |
| C++→Haskell→C++ | 75 | 75 | 15 | 0.200000 | 5.866667 | 29.333333 |
| C++→Prolog→C++ | 75 | 75 | 0 | 0.000000 | 결측 | 결측 |

이번 주 임계치 분류는 성공 122건, 실패 162건, 홉 제한 16건입니다. 실패 162건은 기능 실패 159건과 별도 표시한 측정 실패 3건으로 구성됩니다. 측정 실패 3건을 번역 코드의 기능 실패라고 표현하지 않습니다.

원관측 분류는 성공 122, 기능 실패 159, 홉 제한 16, 무효 3으로 보존됩니다. 원관측의 최종 중단 상태는 기능 실패 168, 정상 수집 종료 112, 홉 제한 16, 기반시설 오류 4입니다. 최초 성공 뒤 후속 실패가 기존 성공을 지우지 않으므로 최종 중단 상태와 주 임계치 분류는 다릅니다. LC_0062의 후속 기능 실패 표시는 524 이후 응답에서 나온 값이므로 정상 첫 생성의 기능 실패로 해석하지 않습니다.

## 기존 판정과 이번 실패 집계의 구분

| 임계치 | 원관측 분모/저장 | 524 감사 후 분모/저장 | 이번 집계 분모/저장 | 별도 측정 실패 | 이번 집계의 남은 무효 |
|---|---:|---:|---:|---:|---:|
| 0.80 | 297/300 | 297/300 | 300/300 | 3 | 0 |
| 0.85 | 297/300 | 297/300 | 300/300 | 3 | 0 |
| 0.90 | 297/300 | 296/300 | 299/300 | 3 | 1 |

이번 0.80·0.85 집계는 300건을 모두 분모에 포함하지만, 사후 집계 변경을 원래 동결 규칙의 완전성 통과나 확증적 분석 승인으로 바꾸지 않습니다. 0.90에 남은 무효 1건은 HTTP 524의 생성 불명 건이며, 사용자가 지정하신 JPlag 3건의 실패 처리와 별개입니다.

LC_0062/Haskell/반복 2의 step09는 HTTP 524 후 재전송되었습니다. step08의 응답 수신 시각은 UTC 07:42:53.794440이고 0.80·0.85 최초 도달 판정이 step09 시작 전에 저장되어 있습니다. 따라서 해당 최초 성공은 보존합니다. 주 확인의 완료 예정 단계는 step10이지만 원자료에는 step01~09만 있어 524 이전 완료된 확인이 없습니다. 원관측의 확인 failed를 감사 후 unavailable로 구분합니다. 0.90의 원관측 format_error는 감사 후 생성 불명 invalid로 분리하며 이후 step09를 첫 생성의 결과로 사용하지 않습니다.

0.90 Haskell의 원관측 성공/분모는 13/72, 524 감사 후에는 13/71입니다. 여기에 이번 측정 실패 3건을 포함하면 13/74, P=0.175676, H=5.692308, D=32.402367입니다. Haskell의 세 임계치에서 분모와 P·D가 달라지며, 다른 경로의 지표와 성공 시점·H는 유지됩니다. 524 변경 근거는 [감사 연결 JSON](audit-derived.json), 이번 실패 처리의 원관측·소스 해시와 세 버전 수치는 [실패 집계 JSON](glm53-failure-policy.json)에 있습니다.

확인 표는 다음과 같습니다. Haskell의 원관측은 통과 5/실패 10/측정 불가 0/평가 가능 15였으나 감사 후 5/9/1/14이며 유지율은 5/14=0.357143입니다. Python은 30/29/1/59, Java는 20/27/0/47, Prolog는 최초 성공 0이라 유지율 결측입니다. 확인 결과도 기술통계로만 제시합니다.

## 별도 표시하는 측정 실패 3건과 확인 측정 불가

| 구분 | 문제·경로·반복 | 단계 | 원자료 |
|---|---|---:|---|
| 세 임계치에 실패 포함·기능 검사 13/13 통과 | IPOP_2609/Haskell/2 | 4 | [처리 기록](commandcode-glm53-v16-20261117/main/IPOP_2609/cpp-via-haskell/attempt-02/step-04/processed.json) |
| 세 임계치에 실패 포함·기능 검사 13/13 통과 | IPOP_2609/Haskell/4 | 8 | [처리 기록](commandcode-glm53-v16-20261117/main/IPOP_2609/cpp-via-haskell/attempt-04/step-08/processed.json) |
| 세 임계치에 실패 포함·기능 검사 13/13 통과 | IPOP_2609/Haskell/5 | 6 | [처리 기록](commandcode-glm53-v16-20261117/main/IPOP_2609/cpp-via-haskell/attempt-05/step-06/processed.json) |
| 최초 성공 보존·확인 측정 불가 | IPOP_2609/Python/3 | 6 | [처리 기록](commandcode-glm53-v16-20261117/main/IPOP_2609/cpp-via-python/attempt-03/step-06/processed.json) |

위 JPlag 실행은 고정 최소 토큰 9에 후보 7토큰으로 유효 제출이 부족하여 exit 1로 종료하였습니다. 인접·원본 유사도에 대한 동일 입력 로컬 재시도도 실패했으며 원자료 사유는 similarity_unavailable입니다. 이번 변경은 이 3건을 실패로 포함하는 집계 변경이며 유사도 0을 측정했다고 기록하지 않습니다. 최소 토큰을 낮추거나 응답을 재생성하지 않았습니다. Python 확인 불가와 524에 따른 Haskell 확인 불가는 이번 3건에 포함하지 않으며 기존 감사 판정을 유지합니다.

### 반복 2·4홉의 복원 C++ 코드

[보존 소스](commandcode-glm53-v16-20261117/main/IPOP_2609/cpp-via-haskell/attempt-02/step-04/source.cpp)와 같은 내용이며 기능 검사는 13/13 통과입니다.

```cpp
#include <iostream>
#include <numeric>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    long long g = std::gcd(a, b);
    cout << g << "\n" << a / g * b << "\n";
    return 0;
}
```

### 반복 4·8홉의 복원 C++ 코드

[보존 소스](commandcode-glm53-v16-20261117/main/IPOP_2609/cpp-via-haskell/attempt-04/step-08/source.cpp)와 같은 내용이며 기능 검사는 13/13 통과입니다.

```cpp
#include <iostream>
#include <numeric>

int main() {
    long long a, b;
    std::cin >> a >> b;
    long long g = std::gcd(a, b);
    std::cout << g << "\n";
    std::cout << (a / g) * b << "\n";
    return 0;
}
```

### 반복 5·6홉의 복원 C++ 코드

[보존 소스](commandcode-glm53-v16-20261117/main/IPOP_2609/cpp-via-haskell/attempt-05/step-06/source.cpp)와 같은 내용이며 기능 검사는 13/13 통과입니다.

```cpp
#include <iostream>
#include <numeric>

int main() {
    long long a, b;
    std::cin >> a >> b;
    long long g = std::gcd(a, b);
    std::cout << g << "\n" << a / g * b << "\n";
    return 0;
}
```

## 호출·사용량·비용

| 단계 | 논리요청 | 전송 | 정상응답 | 입력 토큰 | 출력 토큰 | 추정 USD | 불명 예약 USD |
|---|---:|---:|---:|---:|---:|---:|---:|
| 사전 점검 | 1 | 1 | 1 | 21 | 11 | 0.000077800 | 0 |
| 파일럿 | 55 | 55 | 55 | 34,488 | 12,064 | 0.086116160 | 0 |
| 본 실험 | 1,386 | 1,387 | 1,386 | 814,532 | 287,561 | 1.810113680 | 0.25 |
| 합계 | 1,442 | 1,443 | 1,442 | 849,041 | 299,636 | 1.896307640 | 0.25 |

HTTP 524 1회 외 다른 HTTP 오류와 재전송은 없었습니다. 0.25달러는 첫 전송의 생성·과금 불명을 위한 예약이며 확정 청구액이 아닙니다. 추정액+예약은 2.146307640달러이고 실제 청구액은 미보고(null)입니다. 추정에는 백만 토큰당 입력 1.40·출력 4.40·캐시 입력 0.26달러를 적용하였습니다. 입력 토큰에 포함된 캐시 입력은 사전 점검 0·파일럿 13,376·본 실험 522,368토큰입니다. 미수신 첫 전송의 토큰은 알 수 없으므로 정상응답 토큰에 합산하지 않았습니다.

정리 과정은 오프라인으로 수행했고 인증값을 읽지 않았습니다. 기존 사고 감사 당시의 원자료 30,567파일 불변과 0.85 경로표 불변 검사는 당시 524 감사만의 결과입니다. 이번 사용자 요청으로 Haskell의 집계 분모와 P·D가 추가 변경됐으며, 300개 원관측의 SHA256 불변과 수록 코드 3개·보존 소스의 일치를 별도로 확인합니다. 기존 실행 코드·동결 계약·DeepSeek 준비 설정은 바꾸지 않았습니다. MOSS 제출·모델 재호출·재측정은 수행하지 않았으며, [나머지 작업](deepseek-handoff.md)은 내일 사용자께서 재개하실 때 진행합니다.
