import asyncio
import time
from dataclasses import dataclass
from src.llm_evals.evaluators.base import BaseEvaluator, EvalScore
from src.llm_evals.datasets.loader import EvalSample


@dataclass
class EvalSampleResult:
    case_id: str
    output: str
    latency_sec: float
    scores: list[EvalScore]


class EvalPipeline:
    def __init__(self, target_fn, evaluators: list[BaseEvaluator]):
        self.target_fn = target_fn
        self.evaluators = evaluators

    async def run_case(self, case: EvalSample) -> EvalSampleResult:
        start_time = time.perf_counter()

        # Call LLM Application Target
        output = await self.target_fn(case.input_prompt, case.context)
        latency = time.perf_counter() - start_time

        # Inside EvalPipeline.run_case:
        score_tasks = [
            evaluator.evaluate(
                input_text=case.input_prompt,
                output_text=output,
                expected=case.expected_ground_truth,
                context=case.context,
            )
            for evaluator in self.evaluators
        ]
        scores = await asyncio.gather(*score_tasks)
        return EvalSampleResult(
            case_id=case.id, output=output, latency_sec=round(latency, 4), scores=scores
        )

    async def run_suite(self, test_cases: list[EvalSample]) -> list[EvalSampleResult]:
        tasks = [self.run_case(case) for case in test_cases]
        return await asyncio.gather(*tasks)
