# 실험 결과 분석 (IPOP_1436 / Python 번역)

- 상태: 번역 및 기능 보존 성공 (`success`)
- 성과 지표:
  - 반복 횟수 (Iterations) / 수렴 상태: `2회` 수행 후 고정점(`fixed_point`) 수렴
  - 새로운 측정 지표 (Change-count distance): `2` (2회 왕복이 수행된 후 종료되었으므로 README의 정의대로 2로 도출됨)
  - 의미론적 검증 (Semantic): `pass` (기능 보존됨)
  - 유사도 및 AST 측도: 
    - 잔류 유사성(Residual similarity): 약 85.22% (0.852273)
    - 구문 트리(AST) 거리: 23 (씨드 C++ 대응), 23 (왕복 생성본 대응)
  