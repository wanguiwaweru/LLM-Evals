from datasets.sample import EvalSample
from datasets.results import EvalResult
from runner.evaluate_format import evaluate_format
from runner.evaluate_judge import evaluate_with_judge
from typing import Callable, Any
import time
import asyncio


class EvalRunner:
    def __init__(self, target_llm_fn: Callable[[str, str], Any]):
        self.target_llm = target_llm_fn

    async def run_case(self, case: EvalSample) -> EvalResult:
        start_time = time.perf_counter()

        # 1. Execute Target LLM Call
        output = await self.target_llm(case.input_prompt, case.context)
        latency = time.perf_counter() - start_time

        # 2. Run Evaluators in Parallel
        format_passed = evaluate_format(output)
        judge_score, reasoning = await evaluate_with_judge(
            case.input_prompt, output, case.expected_ground_truth
        )

        return EvalResult(
            case_id=case.id,
            output=output,
            latency_sec=round(latency, 4),
            passed_format=format_passed,
            judge_score=judge_score,
            reasoning=reasoning,
        )

    async def run_suite(self, test_cases: list[EvalSample]) -> list[EvalResult]:
        tasks = [self.run_case(case) for case in test_cases]
        return await asyncio.gather(*tasks)
