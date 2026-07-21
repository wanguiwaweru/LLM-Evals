import asyncio
from .base import BaseEvaluator, EvalScore


class LLMJudgeEvaluator(BaseEvaluator):
    def __init__(self, judge_model: str = "gpt-4o"):
        self.judge_model = judge_model

    async def evaluate(
        self, input_text: str, output_text: str, expected: str = "", context: str = ""
    ) -> EvalScore:
        await asyncio.sleep(0.05)

        is_relevant = expected.lower() in output_text.lower()
        score = 1.0 if is_relevant else 0.2
        return EvalScore(
            name="LLMJudge_Relevance",
            passed=score >= 0.7,
            score=score,
            reasoning=(
                "Output covers ground truth key phrases."
                if is_relevant
                else "Missed expected ground truth facts."
            ),
        )
