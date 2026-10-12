# LeetCode 평가 데이터 quality-1

선정 문제 21개, 평가 입력·정답 273쌍이다. 각 문제의 `case01..10`은 이전 자료를 유지하고 `case11..13`은 품질 점검에서 추가했다. 입력 제약, 공개 예제 제외, 사례 목적, SHA-256과 정답 대조 방법은 [manifest](manifest.json)에 있다.

| 문제 | 평가 입력 |
|---|---:|
| [LC_0001](../../LC_0001/README.md) | 13 |
| [LC_0121](../../LC_0121/README.md) | 13 |
| [LC_0217](../../LC_0217/README.md) | 13 |
| [LC_0053](../../LC_0053/README.md) | 13 |
| [LC_0704](../../LC_0704/README.md) | 13 |
| [LC_0035](../../LC_0035/README.md) | 13 |
| [LC_0283](../../LC_0283/README.md) | 13 |
| [LC_0242](../../LC_0242/README.md) | 13 |
| [LC_0387](../../LC_0387/README.md) | 13 |
| [LC_0003](../../LC_0003/README.md) | 13 |
| [LC_0139](../../LC_0139/README.md) | 13 |
| [LC_0518](../../LC_0518/README.md) | 13 |
| [LC_0062](../../LC_0062/README.md) | 13 |
| [LC_0063](../../LC_0063/README.md) | 13 |
| [LC_0064](../../LC_0064/README.md) | 13 |
| [LC_0739](../../LC_0739/README.md) | 13 |
| [LC_0496](../../LC_0496/README.md) | 13 |
| [LC_0547](../../LC_0547/README.md) | 13 |
| [LC_0207](../../LC_0207/README.md) | 13 |
| [LC_0338](../../LC_0338/README.md) | 13 |
| [LC_0912](../../LC_0912/README.md) | 13 |

## 생성과 검증

평가 입력은 명세를 기준으로 자체 생성한 자료이며 공식 비공개 테스트가 아니다. 추가 입력은 seed `20260917`과 문제 번호로 고정하며 제한된 정수 입력 과제는 고정 값을 쓴다. 모델 실패에 따른 사례 선택은 하지 않았다.

작은 입력의 전수 검사와 큰 입력에 맞춘 다른 정확 알고리즘·수학적 근거를 구분한다. 문제별 구체적 방법은 각 README와 manifest에 있다. 외부 저장소 풀이와 별도로 작성한 검증 구현을 사용하고, C++17 기준 코드의 출력도 대조한다. [실행 보고서](validation_report.json)에 사례별 결과를 기록한다.

LeetCode 공개 입력 51개를 모두 기록해 평가에서 제외하고, 함수 호출형 과제를 문서화한 stdin/stdout 계약으로 변환했다. 각 문제의 공개 예제 1쌍과 평가 13쌍을 C++ 및 외부 JavaScript와 대조한다. 외부 Binary Search 구현은 선형 탐색이므로 기능 검사에만 사용하며 복잡도 요구 충족의 근거로 삼지 않는다.

프로젝트 루트에서 실행한다. Python의 `-O` 옵션은 검증 assertion을 끄므로 사용하지 않는다.

```powershell
python problem/metadata/leetcode21/tools/validate_dataset.py
```

기본 컴파일러는 `.tools/gcc/bin/g++.exe`, 외부 소스 위치는 `.tools/leetcode-source`다. `--compiler`, `--upstream` 옵션으로 변경할 수 있다. 소스의 고정 커밋·파일 해시와 재수집 절차는 [출처 기록](../../leetcode-source/README.md)에 있다. 검증기는 현재 코드와 파일의 해시를 확인하고 보고서를 갱신한다.

생성기 [build_dataset.py](tools/build_dataset.py)는 활성 자료와 manifest를 덮어쓴다. 재생성 순서, 색인 해시 갱신 및 변경 전 스냅샷은 [품질 점검 안내](../quality/README.md)를 따른다. [추가 입력 생성기](tools/supplemental.py)와 [정답 검증기](tools/oracles.py)를 함께 공개한다.

## 적용 범위

크기·수치 경계를 추가했지만 모든 최대 크기와 시간 복잡도를 포괄하는 성능 시험은 아니다. 공개 문제의 학습 오염 부재나 유한 테스트의 의미 동치 보장을 주장하지 않는다. 평가 입력·정답과 진단 자료는 번역 프롬프트에 전달하지 않는다. 현재 연결 설정은 [lmstudio_v2.yaml](../../../lmstudio_v2.yaml)이며 LLM 실험 결과는 데이터 검증과 구분한다.
