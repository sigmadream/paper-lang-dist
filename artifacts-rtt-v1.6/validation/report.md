# T02 고정 코퍼스·기준 구현 완료 보고

15문제·75개 기준 구현의 975개 평가가 모두 통과하였습니다. 독립 이중 계산 195개도 모두 통과하였고, 미검증 사례와 부족한 실행 도구는 각각 0개입니다. 외부 모델 API 호출·기존 problem 자료 수정·git add/commit·하위 작업자 생성은 없었습니다.

## 구현 파일

- papers/v1.6/data/selection.json: 설계의 정확한 15문제, 3개 교체 대응, 재귀군 3개, 반복형 최대공약수 및 C++ 기준 특성
- papers/v1.6/data/references/<문제 ID>/reference.{py,java,hs,pl}: 60개 추가 기준 구현
- papers/v1.6/data/PROVENANCE.md: 원본·재사용·독립 계산 방법과 판본 구분
- scripts/prepare_v16_corpus.py: prepare_corpus(selection_path, source_root, destination), 원본 보존·입출력 중복 및 누락 검사·멱등 준비·해시 매니페스트
- scripts/validate_v16_corpus.py: validate_corpus(cfg), 75개 구현의 모든 사례·도구 버전·독립 계산·검증 구현 해시 기록
- tests/unit/test_v16_corpus.py: 11개 계약 테스트
- data/rtt-v1.6: 692개 생성 파일, 원본 바이트 그대로 복사한 C++ 15개 포함
- artifacts-rtt-v1.6/validation: validation.json, 75개 evaluation.json과 실행 코드·컴파일 근거, 실패 이력, 이 보고서
- .test-tmp/v16-orchestration/corpus-contract.md: 먼저 공유한 정확한 키와 core-contract.md 연결

정확한 파일 목록은 같은 디렉터리의 files.json에 기록하였습니다. 기존 12개를 포함한 C++ 15개 모두 현재 problem 원본과 바이트 일치를 확인하였습니다. core·providers·reporting 소유 파일과 TODO 원문은 직접 수정하지 않았습니다.

## 실제 검증 명령과 결과

- `uv run pytest tests/unit/test_v16_corpus.py -q`: 최종 11개 통과
- `uv run python scripts/prepare_v16_corpus.py`: 15문제·75개 구현 준비, 같은 경로 재실행의 멱등성 확인
- `uv run python scripts/validate_v16_corpus.py --config configs/v1.6/experiment.yaml`: 최종 75/75개 구현·975/975개 평가, 독립 계산 195/195개 통과
- `uv run --with black black --check scripts/prepare_v16_corpus.py scripts/validate_v16_corpus.py tests/unit/test_v16_corpus.py papers/v1.6/data/references`: Python 18개 파일 통과
- `load_hops_config`와 `_validated_inputs`에 실제 설정·검증 JSON 연결: 15문제·975개 성공 자료의 실행기 관문 통과
- `git diff --name-only -- problem`: 변경 파일 없음

최초 전체 실행에서 962개 평가가 성공하였고 Haskell N-Queen은 컴파일 오류로 13개를 실행하지 못하였습니다. 구문 수정 후 해당 13개를 실제 실행하여 고정 평가 975개를 완성하였으며, 이후 공유 설정 명령은 동일한 소스·입력·runtime 계약의 평가 캐시를 재사용하였습니다. 반복 검증 명령의 캐시 결과를 새로운 975개 실행으로 중복 계산하지 않았습니다. Python·Prolog N-Queen n=14의 수동 성능 예비 실행 2회는 고정 평가 수와 별개입니다.

## 도구와 시간 제한

Get-Command와 fps_v1.yaml의 명시 경로를 확인한 뒤 실제 실행되는 도구만 사용하였습니다. PATH에 g++가 없으므로 기존 설정의 MinGW g++.exe 명시 경로를 사용하였고, Python은 현재 uv 프로젝트 가상환경 실행 파일을 사용하였습니다. 검증 의존성 black은 uv 범위에서 실행하였으며 다른 런타임 설치는 하지 않았습니다.

모든 언어에 사례당 5초·컴파일 180초를 그대로 적용하였습니다. 아래 시간은 고정 13개 평가에서 관측한 언어별 최장 사례 시간이며, Haskell N-Queen의 최장 사례는 첫 프로세스 시작 비용을 포함한 n=1입니다.

| 언어 | 실제 도구 버전 | 평가 통과 | 하노이탑 최장 시간 | N-Queen 최장 시간 |
|---|---|---|---|---|
| C++ | g++ 13.2.0 | 195/195 | 0.203553초 | 1.166519초 |
| Python | 3.15.1 | 195/195 | 0.077268초 | 2.314847초 |
| Java | OpenJDK·javac 27.0.1.0.3 | 195/195 | 0.119226초 | 0.158781초 |
| Haskell | GHC 9.10.3 | 195/195 | 0.380013초 | 0.395806초 |
| Prolog | SWI-Prolog 10.0.2 | 195/195 | 0.247113초 | 3.825266초 |

하노이탑 최대 평가 입력 n=16에서 65535개 이동과 개수 행을 출력하였고, 5개 언어 모두 출력은 262146바이트였습니다. 모든 이동의 합법성·최종 탑·2^n-1 최소 이동 수와 출력 순서를 확인하였습니다. N-Queen은 무해 n=2·3을 포함한 기존 13개 입력을 모두 검증하였고 n=14의 365596개 해가 일치하였습니다. 쿼드트리는 재귀 하향 분할과 상향 병합 결과를 대조하여 사분면 순서도 확인하였습니다.

## 실패에서 통과로 전환한 근거

1. 실제 최초 계약 테스트는 selection.json과 두 구현 스크립트 부재로 5개가 실패하였습니다. 구현 뒤 해당 조건을 포함한 11개 테스트가 통과하였습니다.
2. 최초 전체 검증은 Haskell N-Queen의 let 들여쓰기 구문 오류로 74/75개 구현·962/975개 평가였습니다. where 바인딩으로 수정한 뒤 마지막 13개 평가도 통과하였습니다.
3. 최초 validation.json·컴파일 오류 stderr·실패 당시 Haskell 소스는 history/initial-validation 아래 보존하였습니다. 최종 성공 근거는 references/IPOP_9663/haskell/evaluation.json입니다.
4. 누락 언어 15개 결과가 생략되지 않음, 사례가 12개면 실패함, 자료 해시 변경·공개 예시 중복·시간 제한 완화가 차단됨을 테스트하였습니다.

## 연결 상태와 남은 수

core 담당자가 실제 도구 경로와 코퍼스 밖 validation 경로를 공유 설정에 반영한 후 정식 명령과 실행기 해시 관문을 함께 통과하였습니다. validation.file_hashes는 매니페스트 내용 파일과 manifest.json 자체의 해시를 모두 담으며, 매니페스트 내부 목록은 자기 자신을 제외하여 순환 해시를 피합니다. data/rtt-v1.6/validation.json은 생성된 적이 없으며 삭제할 내부 검증 파일도 없습니다.

T02의 미검증 기준 구현은 0/75개, 미검증 고정 평가는 0/975개입니다. 실제 모델 번역·유료 실험·파일럿·본 실험 실행은 이 작업 범위에 포함하지 않았습니다.
