# 실제 코드 사례와 실행 비용

사례는 본 실험 전 동결한 대로 종료 유형별 문제 ID·경로의 사전순 첫 관측을 선택했다. 성공률을 높이기 위한 재생성·출력 수정은 없다.

## 성공

IPOP_10988, cpp-via-haskell: success. 완료 왕복 3, FPS 종료 크기 5, 성공 조건부 거리 5, Sym_adj=1.0, Sym_final=0.0.

| 편도 | 언어 | FPS 크기 | 중복 | 기능 평가 | 인접 유사도 | 원본 유사도 |
| ---: | --- | ---: | --- | --- | --- | --- |
| 1 | haskell | 2 | False | success | None | None |
| 2 | cpp | 3 | False | success | 0.0 | 0.0 |
| 3 | haskell | 4 | False | success | None | None |
| 4 | cpp | 5 | False | success | 0.7435897435897436 | 0.0 |
| 5 | haskell | 5 | True | success | None | None |
| 6 | cpp | 5 | True | success | 1.0 | 0.0 |

종료 단계의 실제 소스:

```cpp
#include <iostream>
#include <string>
#include <algorithm>

int main() {
    std::string input;
    std::cin >> input;
    std::string reversedInput = input;
    std::reverse(reversedInput.begin(), reversedInput.end());
    if (input == reversedInput) {
        std::cout << "1" << std::endl;
    } else {
        std::cout << "0" << std::endl;
    }
    return 0;
}
```

## 생성 코드 실패

IPOP_10988, cpp-via-prolog: runtime_error. 완료 왕복 0, FPS 종료 크기 2, 성공 조건부 거리 None, Sym_adj=None, Sym_final=None.

| 편도 | 언어 | FPS 크기 | 중복 | 기능 평가 | 인접 유사도 | 원본 유사도 |
| ---: | --- | ---: | --- | --- | --- | --- |
| 1 | prolog | 2 | False | runtime_error | None | None |

첫 실패 입력: case01, runtime_error.

```text
INPUT: a

EXPECTED: 1

STDOUT: 
STDERR: ERROR: [Thread main] -g main: main/0: Unknown procedure: read_line_to_string/1

```


종료 단계의 실제 소스:

```pl
main :-
    read_line_to_string(Input),
    reverse_string(Input, Reversed),
    (Input == Reversed -> write(1); write(0)),
    nl.

reverse_string(String, Reversed) :-
    reverse_chars(String, [], Reversed).

reverse_chars([], Acc, Acc).
reverse_chars([H|T], Acc, Reversed) :-
    reverse_chars(T, [H|Acc], Reversed).
```

## 거리 상한 도달

해당 관측이 없다. 사례를 만들어 넣지 않는다.

## 전체 실패 위치

| 생성 언어 | 중간/복원 | 종료 사유 | 건수 |
| --- | --- | --- | ---: |
| cpp | intermediate | wrong_answer | 4 |
| haskell | intermediate | compile_error | 13 |
| haskell | intermediate | runtime_error | 2 |
| haskell | intermediate | timeout | 1 |
| haskell | intermediate | wrong_answer | 5 |
| haskell | restored | compile_error | 6 |
| haskell | restored | runtime_error | 1 |
| prolog | intermediate | compile_error | 6 |
| prolog | intermediate | runtime_error | 22 |
| prolog | intermediate | timeout | 1 |
| prolog | intermediate | wrong_answer | 1 |
| prolog | restored | compile_error | 3 |
| prolog | restored | runtime_error | 16 |

## 비용

| 단계 | 응답 수 | 입력 토큰 | 출력 토큰 | API 지연 합계(초) | 오류 시도 | 잘림 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| pilot | 32 | 16684 | 5776 | 188.02818389996537 | 0 | 0 |
| main | 153 | 78817 | 25566 | 847.7982368998928 | 0 | 0 |

로컬 API 사용료는 0이며 전력 비용은 측정하지 않았다. API 지연 합계에는 컴파일·프로그램 실행·JPlag 분석 시간이 포함되지 않는다.
