import asyncio
from pathlib import Path

from src.llm_evals.datasets.loader import load_dataset
from src.llm_evals.evaluators.heuristic import FormatEvaluator
from src.llm_evals.evaluators.judge import LLMJudgeEvaluator
from src.llm_evals.runner.pipeline import EvalPipeline
from src.llm_evals.reporters.summary import generate_summary_report


# Dummy LLM application target (replace with your real LLM call)
async def sample_llm_app(prompt: str, context: str) -> str:
    await asyncio.sleep(0.05)
    return f"Final Answer: Based on context, the details are {context}"


async def main():
    # Dynamic path lookup relative to repo root
    base_dir = Path(__file__).parent
    dataset_path = base_dir / "datasets" / "regression_v1.json"
    report_path = base_dir / "report.json"

    # 1. Load ground truth dataset
    cases = load_dataset(str(dataset_path))

    # 2. Instantiate active evaluators
    evaluators = [FormatEvaluator(), LLMJudgeEvaluator()]

    # 3. Run parallel evaluation suite
    pipeline = EvalPipeline(target_fn=sample_llm_app, evaluators=evaluators)
    results = await pipeline.run_suite(cases)

    # 4. Generate report summary
    summary = generate_summary_report(results, output_file=str(report_path))

    print("\n✅ Evaluation Run Finished Successfully!")
    print(f"Summary: {summary}")


if __name__ == "__main__":
    asyncio.run(main())
