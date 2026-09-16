# 문제와 평가 입력

기존 IPOP 19문제와 별도로 LeetCode 21문제를 추가했다. 선정 문제는 총 40개, 평가 입력·정답은 문제당 10쌍씩 총 400쌍이다. 일반 입력·경계값·오류를 드러내기 쉬운 유효 입력을 포함한다.

| 자료 | 내용 |
|---|---|
| [평가 입력 묶음](evaluation-v2-a/README.md) | 19문제, 190개 입력·정답, 문제별 설명과 검증 방법 |
| [추가 LeetCode 21문제](leetcode-21/README.md) | 새 21문제, 210개 평가 입력·정답, 공개 예제, C++17 기준 풀이 |
| [추가 문제 검증 기록](leetcode-21/validation_report.json) | 독립 검증·C++·저장소 JS 평가 입력 각 210건 통과 |
| [전체 문제 색인](dataset-index.json) | 기존 19 + 신규 21의 문제 ID, 데이터 위치, manifest 해시 |
| [데이터 명세](evaluation-v2-a/manifest.json) | 사례 목적, 출처 구분, 예시 중복 검사 근거, SHA-256 |
| [실행 검증 기록](evaluation-v2-a/validation_report.json) | 독립 검증 190건, C++ 기준 풀이 190건, 대응 JavaScript 풀이 30건 |
| [GitHub 수집 자료](leetcode-source/README.md) | 저장소 파일 목록, 공개 예제, 채택한 대응 풀이와 변환 조건 |

기존 190개 평가 입력은 BOJ 명세, 새 210개는 LeetCode 명세를 기준으로 자체 생성했다. 저장소에서 수집한 공개 예제와 평가 입력은 구분한다. `IPOP_1260`은 v1 제외 상태를 유지하고 40문제에 포함하지 않았다.

각 `IPOP_*.md`와 기존 `IPOP_*/*.inp`, `*.out`은 v1 자료다. 새 평가 입력·정답은 `dataset_index`를 지정한 RTT 설정에서 별도로 읽는다. [lmstudio_v2.yaml](../lmstudio_v2.yaml)은 40문제 전체를 연결하며, 프롬프트 예제와 평가 파일의 경로 및 실행 방법은 [실행 안내](../README.md)를 참고한다. 데이터 준비와 실행기 연결만으로 LLM 번역 실험이 완료되는 것은 아니다.
