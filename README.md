# 프로그래밍 언어 간 의미 거리의 정량적 측정 방법

다음 예제로 C++ → Python → C++ 왕복 번역을 실행하고 결과를 확인할 수 있습니다.

1. 프로젝트 폴더에서 의존성을 설치합니다. 예제 실행에는 `uv`, `g++`, Python이 필요합니다.

   ```powershell
   uv sync --extra analysis
   ```

2. LM Studio에서 모델을 로드하고 로컬 서버를 시작합니다. [local.yaml](examples/research/local.yaml)의 `models.local.model`을 실제 모델 ID로 변경합니다. 기본 서버 주소는 `http://localhost:1234/v1`입니다.

3. 설정을 검증한 뒤 실험을 실행합니다.

   ```powershell
   uv run rttdist research validate --config examples/research/local.yaml
   uv run rttdist research run --config examples/research/local.yaml
   ```

4. 결과를 집계합니다.

   ```powershell
   uv run rttdist research analyze --experiment artifacts/research/local-demo --analysis-id baseline
   ```

   `artifacts/research/local-demo/analyses/baseline/summary.csv`에서 성공률과 평균 홉 수 등을 확인합니다. 이 예제는 토큰 유사도를 사용합니다.

중단된 실험은 다음 명령으로 이어서 실행합니다.

```powershell
uv run rttdist research resume --config examples/research/local.yaml
```

새 조건으로 실행할 때는 설정의 `id`도 변경합니다.

[자세한 사용법](docs/RESEARCH_LIBRARY.md) · [여러 모델 비교 설정](examples/research/multi-model.yaml) · [추가 분석 프로파일](examples/research/analysis.yaml)
