# Leetcode 저장소 수집 기록

수집일: 2026-09-16. 출처는 [DhanushNehru/Leetcode](https://github.com/DhanushNehru/Leetcode)이며 기준 커밋은 `b9d7d2c234c39b3b3c67eded0c125e2841685b29`다.

| 파일 | 내용 | 평가 용도 |
|---|---|---|
| [inventory.json](inventory.json) | 624개 파일의 경로·크기·SHA-256 | 출처 버전 확인 |
| [public_examples.json](public_examples.json) | 문제 README 12개의 공개 입력·출력 28쌍 | 수집 기록만 제공; 평가 입력에서 제외 |
| [collect_source.py](collect_source.py) | 파일 목록 및 공개 예제 추출기 | 같은 커밋의 자료 재수집 |

공개 예제는 README의 Input/Output 항목에서 추출했다. 문제 설명 전체와 해설은 복제하지 않았다. 입력과 출력은 원래 함수 호출 또는 표 형식을 유지하며 별도 독립 검증을 하지 않았으므로 바로 stdin/stdout 평가에 연결하는 자료가 아니다. 디렉터리 앞 숫자가 공식 LeetCode 문제 번호와 다른 경우가 있어 출처 디렉터리명을 그대로 기록했다.

## 기존 IPOP 문제와 연결한 풀이

이 저장소는 풀이 코드 중심이며 기존 IPOP 19문제 각각에 필요한 미제시 입력 10개를 제공하지 않는다. 다음 3개 알고리즘을 추가 정답 검사에 채택했다. 동일 문제로 간주하지 않고 입력 영역 제한과 결과 변환을 기록했다.

| 기존 문제 | 저장소 경로 | 적용 조건 |
|---|---|---|
| IPOP_10988 | [valid_palindrome/solution.js](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/valid_palindrome/solution.js) | 영문 소문자만 입력; boolean → 0/1 |
| IPOP_9012 | [valid_parentheses/solution.js](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/valid_parentheses/solution.js) | 소괄호만 입력; 문자열별 boolean → YES/NO |
| IPOP_1992 | [construct_quad_tree/solution.js](https://github.com/DhanushNehru/Leetcode/blob/b9d7d2c234c39b3b3c67eded0c125e2841685b29/problems/construct_quad_tree/solution.js) | Node 제공; TL/TR/BL/BR 순서로 BOJ 출력 직렬화 |

각 풀이를 새 입력 10개에 적용한 결과 30/30이 독립 정답과 일치했다. 대응 방법·소스 해시는 [평가 manifest](../evaluation-v2-a/manifest.json), 실행 결과는 [검증 보고서](../evaluation-v2-a/validation_report.json)에 있다. 나머지 16문제에는 이 묶음에서 채택한 대응 풀이가 없다.

입력 생성과 기본 정답 검증은 저장소 풀이와 분리되어 있다. [190개 평가 입력](../evaluation-v2-a/README.md)은 로컬 BOJ 명세에 따라 자체 생성했으며 저장소에서 내려받은 공식 테스트로 표시하지 않는다.

## 재수집

소스 체크아웃은 프로젝트의 `.tools/leetcode-source`에 있다. 수집 커밋에서 LICENSE/COPYING 파일을 찾지 못했으며, 이 디렉터리에는 외부 풀이 코드 전체를 복사하지 않고 출처와 해시를 기록했다.

체크아웃이 없는 환경에서는 프로젝트 루트에서 다음 명령을 실행한다. 이미 경로가 존재한다면 clone을 반복하지 않는다.

```powershell
git clone -c core.autocrlf=true https://github.com/DhanushNehru/Leetcode.git .tools/leetcode-source
git -C .tools/leetcode-source checkout b9d7d2c234c39b3b3c67eded0c125e2841685b29
python problem/leetcode-source/collect_source.py .tools/leetcode-source
python problem/evaluation-v2-a/tools/validate_dataset.py
```

이번 수집은 Windows의 CRLF 체크아웃 기준이다. 위 clone 명령의 설정은 같은 파일 바이트를 재현하기 위한 것이며, 다른 줄바꿈 정책의 체크아웃은 동일 커밋이어도 SHA-256이 달라질 수 있다. 체크아웃의 파일 바이트가 기록한 SHA-256과 일치해야 한다. 외부 풀이 검증기는 검토한 3개 파일에만 적용하며 해시가 다른 코드를 실행하지 않는다.
