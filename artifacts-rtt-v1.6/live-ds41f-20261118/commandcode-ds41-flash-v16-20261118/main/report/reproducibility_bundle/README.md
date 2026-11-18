# v1.6 재현 묶음

인증값을 제외한 원관측·계약·문제 목록·환경·집계 코드를 보관합니다. 원응답과 생성 코드는 raw_sources.json의 포함 여부와 해시를 확인하십시오. 이 묶음만으로는 미포함 평가 출력의 정확성을 감사했다고 볼 수 없습니다.

저장소의 uv 환경에서 실행하십시오.

```powershell
uv sync --extra analysis
uv run python scripts/report_v16.py --bundle <이_묶음_경로> --destination <출력_경로>
uv run python scripts/verify_v16_reproducibility.py --bundle <이_묶음_경로>
```
