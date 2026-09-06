# 1. 핵심 아이디어

1. 프로그램 코드의 언어 A를 LLM으로 언어 B로 변환한 뒤 다시 A로 왕복 번역하는 과정에서 발생하는 정보 손실과 구조적 변화 정도를 두 언어 사이의 "거리"로 본다.
2. 왕복을 반복했을 때 더 이상 코드가 변하지 않는 지점(고정점)에 도달하는지, 도달한다면 반복 횟수가 얼마인지, 그리고 원본과 고정점 코드의 구조적 차이를 측정한다.
3. 구조적 차이의 정량화에는 MOSS 같은 코드 유사도 측정 시스템을 활용하며, 의미 보존은 실제 BOJ 문제를 통과하는지 실행 기반으로 평가한다.

이 패턴은 Allamanis 등이 제안한 Round-Trip Correctness(RTC)처럼 "모델 예측을 다시 역변환했을 때 의미 동치가 유지되는지"를 보는 비지도 평가 기법과 같은 계열에 속합니다.

# 2. 주요 분야와 논문

## 2.1 왕복 번역과 Round-trip Correctness 계열

- Allamanis, Panthaplackel, Yin, "Unsupervised Evaluation of Code LLMs with Round-Trip Correctness" (ICML 2024):
  - 코드 설명 생성 후 다시 코드를 합성해 원본과 의미 동치인지 테스트하는 RTC를 제안합니다. 코드 LLM 성능이 HumanEval 등 기존 벤치마크에서의 성능과 높은 상관을 보인다고 보고해, 왕복 기반 평가의 타당성을 뒷받침합니다.
  - SAP 블로그 등에서 RTC를 일반적인 "모델↔텍스트↔모델" 왕복 평가 메트릭으로 확장해 설명하고 있어, 왕복 아이디어를 코드 외 다른 도메인에 적용할 때 참고가 됩니다.
  - [community.sap](https://community.sap.com/t5/technology-blog-posts-by-sap/round-trip-correctness-a-new-metric-for-generative-ai-based-process/ba-p/14091979)

현재 논문은 RTC를 "언어 간 거리"로 재해석해, 왕복 번역 반복과 고정점을 지표로 사용하는 특수한 케이스라고 볼 수 있습니다. [arxiv](https://arxiv.org/abs/2402.08699)

## 2.2 언어 거리와 유사도 측정 이론 (자연어 중심)

- DistaLs: "DistaLs: A Comprehensive Collection of Language Distance Measures"는 ISO 639-3 언어들에 대해 메타데이터, 형태론, 단어 리스트, 텍스트 기반 특성 등 다양한 거리 메트릭을 모아 자연 언어 거리를 체계적으로 측정합니다. [aclanthology](https://aclanthology.org/2025.emnlp-demos.23.pdf)
  - POS 분포 기반 언어 거리: 한 논문은 품사 3그램 분포의 Jensen–Shannon 거리로 언어 간 통계적 거리를 정의해, 언어를 확률적 특성 공간에서 비교하는 방법을 제시합니다. [web3.arxiv](https://web3.arxiv.org/pdf/2403.18430v1)
  - conceptual language similarity 연구들은 레벤슈타인 거리, 어휘 유사도, 개념 임베딩 기반 코사인 유사도 등 여러 유사도 지표를 비교하면서 "거리 행렬"을 만들고 이를 계통 관계나 교육적 응용으로 해석합니다. [ar5iv.labs.arxiv](https://ar5iv.labs.arxiv.org/html/2305.13401)

프로그래밍 언어에 대해서도 예약어 집합, 타입·메모리 모델 특성 벡터, AST 분포 등으로 특성 공간을 만들고 거리 행렬을 구성하려는 시도들이 있어, 부록 D에서 요약한 키워드 집합, AST 편집 거리, 벡터 임베딩, 특성 벡터 접근들과 자연스럽게 연결됩니다. [shape-of-code](https://shape-of-code.com/2022/04/24/programming-language-similarity-based-on-their-traits/)

## 2.3 코드 유사도와 정보 거리

- Aiken의 MOSS 시스템은 토큰 k-그램과 Winnowing 알고리즘으로 코드 fingerprint 집합을 만들고, 공통 fingerprint 비율로 구조적 유사도를 측정합니다. 이는 변수명 변경 등 표면 변형에 강건한 코드 유사도 측정의 대표 사례입니다. [kc.umn.ac](https://kc.umn.ac.id/id/eprint/20064/3/BAB_II.pdf)
  - 여러 코드 유사도 메트릭 비교 논문들은 레벤슈타인 거리, 코사인 유사도, n-gram 기반 유사도, Greedy String Tiling 등 문자열 기반·벡터 기반 메트릭의 정밀도·재현율을 비교해 각각의 장단을 분석합니다. [archive.ceciis.foi](https://archive.ceciis.foi.hr/public/conferences/1/archive2011/EIS_8.pdf)
  - Kolmogorov 복잡도 기반 normalized information distance(NID)는 두 객체를 서로 변환하는 최단 프로그램 길이에 기반한 "보편적 거리"로, 모든 상계 반계산 가능한 유사도들을 상한하는 보편 메트릭을 정의합니다. [homepages.cwi](https://homepages.cwi.nl/~paulv/papers/similarity.pdf)

현재 논문이 사용하는 "왕복 고정점까지의 반복 횟수"와 "MOSS 유사도"는 이러한 다양한 코드 거리 메트릭 중 실행 의미 보존과 구조적 변형을 동시에 고려한 특수 구성으로 볼 수 있고, 향후 더 일반적인 정보 거리 프레임워크로 연결할 수 있는 포인트입니다. [homepages.cwi](https://homepages.cwi.nl/~paulv/papers/similarity.pdf)

# 3. 이 논문을 기반으로 직접 확장할 수 있는 분야와 관련 논문

여기서는 지금 실험의 틀을 유지하면서 범위와 이론을 넓히는 "정통 후속 연구" 방향을 정리합니다.

## 3.1 언어 거리 행렬과 군집 분석

- 아이디어: 지금처럼 C++ 기준으로 C, Java, Python만 보는 것이 아니라, 여러 언어 쌍에 대해 왕복 고정점 반복 횟수, 의미 보존률, 구조적 유사도(MOSS, AST 편집 거리, CSSG 등)를 측정해 "프로그래밍 언어 거리 행렬"을 구축할 수 있습니다. [arxiv](https://arxiv.org/html/2404.08817v1)
- 참고: 자연어 DistaLs에서 하는 것처럼 언어 특성(타입 시스템, 메모리 관리, 패러다임 등)을 수치화하고 거리 행렬을 기반으로 클러스터링·차원축소를 수행해 "언어 지형도"를 그리는 접근을 프로그래밍 언어로 가져올 수 있습니다. [aclanthology](https://aclanthology.org/2025.emnlp-demos.23.pdf)

후속 논문 방향:
- "Round-trip fixed-point 기반 프로그래밍 언어 거리 행렬과 군집 분석"
- "LLM 기반 언어 거리와 정적 특성 벡터의 상관 관계 분석"

관련 참고:
- Programming language similarity based on their traits (키워드·특성 벡터를 이용한 거리 측정). [shape-of-code](https://shape-of-code.com/2022/04/24/programming-language-similarity-based-on-their-traits/)
- DistaLs 언어 거리 컬렉션. [aclanthology](https://aclanthology.org/2025.emnlp-demos.23.pdf)

## 3.2 거리 지표의 정교화: AST·PDG 기반 메트릭 결합

- 현재 논문은 MOSS 유사도를 사용하지만, AST 편집 거리(TSED)나 PDG 기반 CSSG 같은 구조·의미 지향 메트릭을 결합해 "언어 간 구조적 거리"를 더 세밀하게 정의할 수 있습니다. [arxiv](https://arxiv.org/html/2601.04085v2)
- AST edit distance를 기반으로 TSED(Trees Similarity Edit Distance)를 최적화한 최근 연구는 언어별 코드 구조 유사도 측정에서 기존 BLEU, Jaccard, GPT-기반 유사도보다 높은 상관을 보였습니다. [arxiv](https://arxiv.org/html/2404.08817v1)
- CSSG는 프로그램 의존 그래프 기반 그래프 편집 거리를 사용해 제어·데이터 의존 관계를 포함한 의미 지향 코드 유사도를 정의하며, 단일 언어뿐 아니라 cross-lingual 설정에서도 기존 메트릭보다 나은 구분력을 보고합니다. [arxiv](https://arxiv.org/html/2601.04085v2)

후속 논문 방향:
- "왕복 고정점과 AST/PDG 기반 코드 유사도 메트릭을 이용한 언어 거리 정의"
- "MOSS, TSED, CSSG 간 상관 구조와 LLM 왕복 패턴의 결합 분석"

## 3.3 LLM·프롬프트 요인 분석과 모델 선택 프레임워크

현재 논문은 qwen2.5 coder와 gpt-5.4 사이의 왕복 패턴과 의미 보존률을 비교해 "모델별 언어 특성 의존성"을 관찰합니다. 이 부분을 더 체계화할 수 있습니다. 특히 일반 LLM과 코딩 특화 LLM 사이의 성능 편차가 결과에 미치는 영향을 분석하고, 언어 모델이 고도화될수록 이러한 지표들이 어떻게 수렴하는지 추적하는 것은 신뢰도 확보를 위한 매우 중요한 과제입니다.

- RTCE(RoundTripCodeEval) 같은 최근 벤치마크는 압축 알고리즘에 대한 코드 생성·역생성을 이용해 "실행 기반 왕복 self-consistency"를 측정하며, RTC와 다른 관점의 round-trip 평가를 제시합니다.
- 다양한 프롬프트 전략(예: 타입 설명 강조, 제약 조건 명시, AST 형태 유지 요청 등)을 설계해 왕복 고정점 도달 속도와 의미 보존률에 미치는 영향을 측정하면 "프롬프트-언어-모델" 3차원 상호작용을 정량화할 수 있습니다.

후속 논문 방향:
- "프로그래밍 언어 쌍 및 요구사항에 따른 LLM 모델·프롬프트 자동 선택 프레임워크"
- "왕복 고정점 기반 코드 LLM self-consistency 평가와 RTCE·RTC의 비교"
- "코드 특화 LLM의 성능 고도화(Scaling)에 따른 왕복 고정점 및 언어 거리 지표의 수렴성(Convergence) 분석"

## 3.4 더 큰·다양한 코퍼스와 실제 시스템 코드

- 지금은 BOJ 알고리즘 문제 5개를 대상으로 했는데, OSS 프로젝트, 산업용 코드, 다양한 도메인(네트워크, GUI, 데이터 처리 등)을 포함해 왕복 패턴을 측정하면 "도메인별 언어 거리"와 "실무 코드에서의 변환 난이도"까지 분석할 수 있습니다. [arxiv](https://arxiv.org/abs/2402.08699)
- Code refactoring with LLM에 대한 포괄적 평가 논문은 리팩토링 전후 코드의 레벤슈타인 거리, 유사도, 언어별 구조적 변화 정도를 측정해, 언어·샷 수에 따라 refactoring 난이도와 결과 품질의 차이를 보고합니다. 이를 왕복 번역과 결합하면 "언어 간 리팩토링 난이도"를 거리 개념으로 재구성할 수 있습니다. [arxiv](https://arxiv.org/html/2511.21788v1)

후속 논문 방향:
- "대규모 OSS 코퍼스를 이용한 LLM 기반 언어 거리 측정과 도메인 특성 분석"
- "언어 거리와 코드 리팩토링 난이도 상관 분석"

# 4. 응용 방향과 관련 논문

여기서는 지금 정의한 언어 거리·왕복 고정점 개념을 다른 문제로 투영하는 "변형 응용"을 제안합니다. 각 방향은 후속 논문에서 독립 주제로 다루기 좋습니다.

## 4.1 교육 커리큘럼 설계와 학습 경로 최적화

- 아이디어: 언어 거리 행렬을 바탕으로 "학생이 이미 익힌 언어와 가장 가까운 언어"를 추천해 학습 전이를 쉽게 만들거나, 반대로 "거리가 먼 언어를 의도적으로 배치해 패러다임 폭을 넓히는" 커리큘럼을 설계할 수 있습니다. [shape-of-code](https://shape-of-code.com/2022/04/24/programming-language-similarity-based-on-their-traits/)
- 참고: 언어 거리와 교육 난이도 연구들은 어휘·문법 유사도를 기반으로 "어떤 언어를 먼저 가르칠 때 다른 언어 학습이 쉬워지는가"를 분석합니다. [ar5iv.labs.arxiv](https://ar5iv.labs.arxiv.org/html/2305.13401)

후속 논문 방향:
- "LLM 기반 프로그래밍 언어 거리 행렬을 이용한 학습 경로 추천"
- "언어 거리와 학생 코드 오류 패턴의 상관 분석"

## 4.2 자동 언어 변환·이식 전략 설계

- 아이디어: 언어 거리와 왕복 고정점 패턴을 이용해 "어떤 언어 쌍에서는 자동 변환이 안정적이고, 어떤 쌍에서는 인간의 개입·리팩토링 설계가 필수적인지"를 전략적으로 정할 수 있습니다. [arxiv](https://arxiv.org/html/2511.21788v1)
- 참고:
  - 코드 리팩토링 LLM 평가 논문은 언어별 구조적 변화량과 의미 보존률을 정량화해, Java와 C#은 구조 변화가 크지만 의미 유사도가 높은 패턴, Python은 구조 변화가 작지만 유사도가 중간인 패턴 등을 보고합니다. [arxiv](https://arxiv.org/html/2511.21788v1)
  - CSSG·TSED 같은 구조·의미 기반 유사도 메트릭은 "변환 전후 코드가 얼마나 비슷한가"를 정밀하게 측정할 수 있어, LLM 기반 언어 변환 파이프라인의 품질 보증에 활용하기 좋습니다. [arxiv](https://arxiv.org/html/2404.08817v1)

후속 논문 방향:
- "언어 거리와 코드 변환 파이프라인 설계: LLM 기반 자동 이식의 위험 분석"
- "왕복 고정점 기반 언어 변환에서의 안전성·보수성 트레이드오프"

## 4.3 코드 표절·유사도 탐지기의 차세대 설계

- 아이디어: 지금 논문은 MOSS를 사용해 구조적 유사도를 측정하는데, MOSS는 전통적으로 표절 탐지에 쓰이는 시스템입니다. LLM 기반 왕복 거리 개념을 결합하면 "LLM이 일부 재작성해도 의미적으로 거의 동일한 코드"를 탐지하는 더 강력한 표절 탐지 기법을 설계할 수 있습니다. [kc.umn.ac](https://kc.umn.ac.id/id/eprint/20064/3/BAB_II.pdf)
- 참고:
  - MOSS의 Winnowing fingerprinting과 다양한 문자열 기반 유사도 메트릭(레벤슈타인, 코사인, n-gram, Greedy String Tiling) 비교 연구는 표절 탐지에서 각 메트릭의 민감도·강건성을 분석합니다. [archive.ceciis.foi](https://archive.ceciis.foi.hr/public/conferences/1/archive2011/EIS_8.pdf)
  - CSSG 같은 의미 지향 코드 유사도 메트릭은 PDG 기반 그래프 편집 거리로 "컨트롤·데이터 의존 관계까지 유사한지"를 판단해 표면적 변형을 넘어선 유사성 탐지에 적합합니다. [arxiv](https://arxiv.org/html/2601.04085v2)

후속 논문 방향:
- "LLM 왕복 고정점 기반 의미 표절 탐지: MOSS·CSSG 결합 접근"
- "언어 거리와 표절 탐지 난이도의 상관 구조"

## 4.4 멀티언어 코드 검색·추천·RAG 시스템

- 아이디어: 언어 거리를 이용해 "검색 질의 언어와 대상 코드 언어의 거리"를 고려하는 코드 검색·추천 시스템을 설계할 수 있습니다. 예를 들어, Python 개발자가 C++ 코드 예제를 검색할 때, 언어 거리가 가까운 C, Rust, Java 등을 함께 추천하는 식입니다. [shape-of-code](https://shape-of-code.com/2022/04/24/programming-language-similarity-based-on-their-traits/)
- 참고: 코드 유사도 메트릭들(BLEU, CodeBLEU, TSED, CSSG 등)은 cross-lingual 코드 클론 탐지와 멀티언어 코드 검색에서 "다른 언어로 쓰인 동일 알고리즘"을 찾는 데 쓰입니다. [arxiv](https://arxiv.org/html/2404.08817v1)

후속 논문 방향:
- "언어 거리 기반 멀티언어 코드 검색·추천 시스템 설계"
- "코드 RAG에서 소스 언어 선택을 위한 언어 거리 활용"

## 4.5 정보 거리·압축 관점에서의 일반화

- 아이디어: Kolmogorov 기반 normalized information distance(NID)와 RTCE의 "압축·역압축 왕복 평가"를 참고해, 프로그래밍 언어 간 거리도 근본적으로 "압축·변환·역변환" 연산의 비용으로 볼 수 있습니다. [homepages.cwi](https://homepages.cwi.nl/~paulv/papers/similarity.pdf)
- 참고:
  - NID는 두 문자열을 서로 변환하는 최단 프로그램 길이에 기반해 보편적 유사도·거리 메트릭을 정의합니다. [homepages.cwi](https://homepages.cwi.nl/~paulv/papers/similarity.pdf)
  - RTCE는 압축 알고리즘에 대해 코드 LLM이 압축·복원을 수행할 때의 bijection fidelity를 평가해, 실행 없는 closed-loop self-consistency를 측정합니다. [aclanthology](https://aclanthology.org/2026.findings-acl.1279.pdf)

후속 논문 방향:
- "LLM 기반 언어 거리와 normalized information distance의 관계 탐색"
- "압축·역압축 관점에서 본 프로그래밍 언어 간 왕복 변환 난이도"

# 5. 제안서 종합 학술 평가 및 권장 연구 방향 (Appendix 요약)

## 5.1 전체 총평 및 핵심 쟁점

현재 연구를 "LLM 왕복 번역과 고정점 개념을 결합하여 프로그래밍 언어 간 차이를 정량화하려는 파일럿 연구"로 평가할 수 있습니다. 후속 연구의 가장 중요한 과제는 관측된 지표(반복 횟수, 의미 보존률)에서 모델의 특성, 프롬프트, 과제 난이도를 분리해내어 온전한 '언어의 차이'를 통계적으로 검증하는 것입니다. 현재의 측정값을 단순한 '거리(Distance)'보다는 "모델 조건부 확률적 변환 발산도(Divergence)"로 재정의하는 것이 학술적으로 더 타당합니다.

## 5.2 권장되는 이론적 재정의와 다중뷰 지표

- 의미 생존 보정 고정점 거리: 단순 반복 횟수 비교의 한계(빠른 의미 실패가 짧은 거리로 오인되는 문제)를 해결하기 위해, 의미 보존 실패를 별도의 페널티로 분리하고, 의미 등가류에 대한 확률적 고정점 도달 기댓값을 산출해야 합니다.
- 다중 관점(Multi-view) 측정: MOSS 0% 사례에서 보듯 구조적 변화와 의미적 보존은 다르게 움직입니다. MOSS(어휘/표면) 외에도 AST(구문), 데이터 흐름(의존성), 임베딩(의미 표현), 실행 테스트 통과 여부 등을 종합적으로 측정해야 합니다.

## 5.3 최적의 실험 설계 및 논문 구성

- 실험 데이터 3계층 구성: (1) 단일 특성만 바꾼 마이크로벤치마크, (2) 다언어 벤치마크(MultiPL-E 등), (3) 실제 OSS 시스템 코드로 점진적 확대.
- 논문 프레이밍:
  - 연구 질문: LLM 매개 언어 간 왕복 변환에서 관측되는 의미 손실과 수렴 과정 중, 언어쌍에 기인하는 성분을 모델/과제 효과로부터 분리하여 재현 가능한 방향성 발산도로 정의할 수 있는가? 또한, 코딩 특화 모델이 발전함에 따라 이 발산도는 모델 독립적인 고유의 '언어 거리'로 수렴하는가?
  - 권장 전개 순서:
    1. 의미 생존 보정 확률적 고정점 거리 제안 (이론/검증)
    2. 다중뷰 프로그래밍 언어 거리 구축 (지표 고도화)
    3. 모델 불변 다언어 거리 지도(Phylogeny) 및 언어 특성 분석 (확장)
    4. 코드 특화 LLM 발전에 따른 언어 거리 지표의 수렴성 입증 (신뢰도 검증)
