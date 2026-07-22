# LLM-Evals

A lightweight, async evaluation harness for LLM applications — load a labeled dataset,
run it through your target LLM function, score the outputs with pluggable evaluators
(heuristic + LLM-as-judge), and generate a summary report.

## Why this exists

Most eval frameworks either lock you into a specific provider's judge model or make it
hard to mix cheap heuristic checks (formatting, regex, schema validation) with expensive
LLM-judge scoring in the same run. This harness keeps evaluators as a simple pluggable
interface so both can run side by side, in parallel, against the same dataset.

## Architecture
Dataset (JSON) → EvalPipeline.run_suite() → [Evaluator, Evaluator, ...] → Reporter
│ │
target_fn(prompt, context) runs in parallel per case
(your LLM app under test) (FormatEvaluator, LLMJudgeEvaluator, ...)

- **`datasets/loader.py`** — loads labeled test cases from JSON
- **`evaluators/`** — pluggable scoring logic; ships with `FormatEvaluator` (heuristic)
  and `LLMJudgeEvaluator` (LLM-as-judge grading)
- **`runner/pipeline.py`** — `EvalPipeline` runs the target function against every case
  and scores it with all active evaluators concurrently
- **`reporters/summary.py`** — aggregates results into a `report.json`

## Quickstart

```bash
git clone https://github.com/wanguiwaweru/LLM-Evals.git
cd LLM-Evals
pip install -e ".[dev]"
python main.py
```

This runs the bundled `regression_v1.json` dataset against a dummy target function and
writes `report.json` with per-case and aggregate scores.