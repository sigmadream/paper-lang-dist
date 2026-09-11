## 코퍼스 감사와 해석 범위

원본 20문제 중 IPOP_1260은 10개 fixture 모두에서 출력이 비어 검증을 통과하지 못했다. 해당 입력 파일 첫 줄의 `:` 때문에 reference.cpp의 정수 입력이 실패하고 조기 종료한다. 따라서 세 경로 모두에서 제외하며 모델의 기능 오류로 세지 않는다. 원본과 fixture를 수정하지 않았고, 나머지 19문제가 사전 검증을 통과했다.

검증을 통과한 19문제에는 fixture 입력 파일 190개가 있지만, 문제별로 바이트 내용 중복을 제거한 서로 다른 입력은 총 70개다. 특히 8문제(IPOP_1158, IPOP_11729, IPOP_1620, IPOP_1929, IPOP_1992, IPOP_2609, IPOP_9251, IPOP_9663)는 입력이 한 종류뿐이다. 프롬프트가 첫 fixture 입력과 정답을 제공하므로 이 8문제의 평가는 프롬프트에 제시하지 않은 입력에 대한 검증을 포함하지 않는다. fixture 10쌍을 서로 다른 10개 테스트로 해석하면 안 된다. 상세 중복 수는 `artifacts-lmstudio/preflight-v1/fixture_diversity.json`에 저장했다.

## 예비 실행에서 확인한 빠른 실패 사례

예비 실행 IPOP_1436의 C 경로는 첫 번역 직후 기능 오류로 종료됐다. 생성 코드의 `strstr((char*)&value, "666")`는 정수를 십진 문자열로 변환하는 대신 정수의 메모리를 문자열처럼 읽는다. 첫 fixture부터 오답이 발생했고 10번 fixture는 30초 제한을 넘겼다. 이 실행은 짧은 종료 횟수로 가까운 언어 거리를 뜻하는 것이 아니다. SF 정의에서는 후보 안정화가 없으므로 c=0부터 실패이며 조건부 tau와 Delta_0 계산에서 빠진다. 이 사례는 예비 자료로만 설명하며 본 실험 분모에 합산하지 않는다.

## 구버전 자료의 재평가

기존 `lmstudio-rtt-demo`의 3경로는 저장된 해시와 모든 단계 검사 기록에 따르면 tau_c=2에서 c=0 후보·기능 조건을 만족했다. 그러나 과거 원본 사전 실행 검증 이력과 추가 확인 왕복 기록이 없으므로 새 본 실험에 포함하지 않는다. c>=1은 `confirmed: unavailable`이며 0 또는 성공으로 대체하지 않았다. 재평가 결과는 `artifacts-lmstudio/lmstudio-rtt-demo/legacy_sf_reassessment.json`에 저장했다. 모델·프롬프트·문제 집합이 다른 과거 발표와 이번 실험의 순위를 직접 비교하지 않는다.

## 방법과 도구의 근거

토큰 시퀀스 지표는 입력 방향을 원본/이전 코드에서 후보/이후 코드로 고정하고 SequenceMatcher의 autojunk를 끈다. LCS나 대칭 거리로 해석하지 않는다. [Python difflib 문서](https://docs.python.org/3.14/library/difflib.html).

모델 양자화와 컨텍스트는 파일명에서 추정하지 않고 실행 시작 시 native API의 실제 로드 설정을 저장했다. [LM Studio 모델 목록 API](https://lmstudio.ai/docs/developer/rest/list).

AST 표현과 단위 비용 TSED는 이 실험의 고정 정의이며, 원 논문의 비용 조정값을 재현한 것으로 주장하지 않는다. [Song 등의 AST 편집 유사도 연구](https://aclanthology.org/2024.acl-short.3/).
