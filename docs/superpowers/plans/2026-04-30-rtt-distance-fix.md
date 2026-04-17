# RTT 고정점 기반 언어 거리 지표 수정 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존의 AST 거리 지표를 제거하고, 고정점(Fixed Point)에 도달한 RTT 횟수를 새로운 "언어 거리" 지표로 사용하여 보고서를 생성하도록 수정합니다.

**Architecture:** `reporting.py`의 요약 및 집계 로직을 수정하여 `fixed_point`에 도달한 경우에만 RTT 횟수를 거리로 기록하고, 집계 시에도 성공한 케이스만 포함하도록 변경합니다.

**Tech Stack:** Python, `rttdist` CLI

---

### Task 1: RTT 거리 지표 산출 로직 추가 및 AST 지표 제거

**Files:**
- Modify: `src/rttdist/reporting.py`

- [ ] **Step 1: `RTT Distance` 산출용 유틸리티 함수 정의**

파일 하단에 `fixed_point` 여부에 따라 거리를 반환하는 함수를 추가합니다.

```python
def _build_rtt_distance_measurement(
    *, convergence_outcome: str, iteration_count: int
) -> dict[str, Any]:
    if convergence_outcome == "fixed_point":
        return {
            "availability": "measured",
            "value": iteration_count,
        }
    return {
        "availability": "unavailable",
        "reason": f"not_fixed_point ({convergence_outcome})",
    }
```

- [ ] **Step 2: `_build_summary_entry` 수정**

`ast_distance` 항목을 제거하고, `rtt_distance`를 추가합니다.

```python
    # _build_summary_entry 함수 내
    entry = {
        # ... 기존 필드들
        "rtt_distance": _build_rtt_distance_measurement(
            convergence_outcome=_convergence_outcome(final_record),
            iteration_count=len(iterations)
        ),
        # "ast_distance": ... 제거
    }
```

- [ ] **Step 3: `_build_ordered_pair_aggregates` 수정**

새로운 `rtt_distance`에 대한 집계 항목을 추가합니다.

```python
    # _build_ordered_pair_aggregates 함수 내
    aggregates[ordered_pair_key] = {
        # ... 기존 필드들
        "rtt_distance": _build_numeric_aggregate(
            grouped,
            measurement_getter=lambda item: item.get("rtt_distance"),
            value_getter=lambda value: float(value) if isinstance(value, (int, float)) else None,
        ),
    }
```

---

### Task 2: Markdown 보고서 렌더링 수정

**Files:**
- Modify: `src/rttdist/reporting.py`

- [ ] **Step 1: `render_run_summary_markdown` 테이블 헤더 수정**

`AST distance to seed`를 `RTT Distance (A<->A')`로 변경합니다.

```python
    # render_run_summary_markdown 함수 내
    if include_moss:
        lines.extend(
            [
                "| Problem | Ordered pair | Final status | Iterations | RTT Distance (A<->A') | Convergence | Residual similarity | MOSS similarity | Semantic |",
                "| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |",
            ]
        )
    else:
        # ... 생략
```

- [ ] **Step 2: 행(row) 데이터 매핑 수정**

`ast` 대신 `rtt_distance`를 사용하도록 수정합니다.

---

### Task 3: Mock 실험을 통한 검증

- [ ] **Step 1: Mock 환경 설정**
- [ ] **Step 2: 실험 실행**
- [ ] **Step 3: 결과 파일 확인**

---

### Task 4: 실제 모델(OpenAI/Ollama) 실험 재수행

- [ ] **Step 1: OpenAI 실험 재실행**
- [ ] **Step 2: 최종 보고서 생성**
- [ ] **Step 3: 결과 보고**
