# FPS 실험 결과

모델: qwen2.5-coder-7b-instruct; 단계: pilot; 계획 18, 기록 18; 감사 통과 True.

| 경로 | 성공/평가 | P_sf [Wilson 95%] | P_functional | d_n 중앙값 [Q1,Q3] | Sym_final 중앙값 |
| --- | --- | --- | --- | --- | --- |
| cpp-via-haskell | 1/3 | 0.333 [0.061,0.792] | 0.333 | 4.000 [4.000,4.000] | 0.278 |
| cpp-via-prolog | 0/3 | 0.000 [0.000,0.561] | 0.000 | NA [NA,NA] | NA |
| haskell-via-cpp | 1/3 | 0.333 [0.061,0.792] | 0.333 | 6.000 [6.000,6.000] | 0.000 |
| haskell-via-prolog | 0/3 | 0.000 [0.000,0.561] | 0.000 | NA [NA,NA] | NA |
| prolog-via-cpp | 0/3 | 0.000 [0.000,0.561] | 0.000 | NA [NA,NA] | NA |
| prolog-via-haskell | 0/3 | 0.000 [0.000,0.561] | 0.000 | NA [NA,NA] | NA |

성공 조건부 값에는 실패를 0 또는 상한값으로 대입하지 않는다. bootstrap은 문제 단위 재표집이며 R=1의 실행 변동성을 추정하지 않는다.
전체 분모·상태·미평가·미완료·대응 비교·퇴화 구간·예비 문제 제외 분석은 summary.json을 따른다.

| 경로 | 계획 | 성공 | 평가 실패 | 미평가 | 미완료 |
| --- | ---: | ---: | ---: | ---: | ---: |
| cpp-via-haskell | 3 | 1 | 2 | 0 | 0 |
| cpp-via-prolog | 3 | 0 | 3 | 0 | 0 |
| haskell-via-cpp | 3 | 1 | 2 | 0 | 0 |
| haskell-via-prolog | 3 | 0 | 3 | 0 | 0 |
| prolog-via-cpp | 3 | 0 | 3 | 0 | 0 |
| prolog-via-haskell | 3 | 0 | 3 | 0 | 0 |
