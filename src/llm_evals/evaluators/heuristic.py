import re
from .base import BaseEvaluator, EvalScore


class FormatEvaluator(BaseEvaluator):
    def __init__(self, pattern: str = r"^Final Answer:"):
        self.pattern = pattern

    async def evaluate(
        self, input_text: str, output_text: str, expected: str = "", context: str = ""
    ) -> EvalScore:
        passed = bool(re.search(self.pattern, output_text, re.MULTILINE))
        return EvalScore(
            name="FormatCheck",
            passed=passed,
            score=1.0 if passed else 0.0,
            reasoning=f"Regex pattern '{self.pattern}' {'matched' if passed else 'failed'}.",
        )
