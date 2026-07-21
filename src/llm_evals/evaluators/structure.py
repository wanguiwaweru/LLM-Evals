import json
from .base import BaseEvaluator, EvalScore


class JSONSchemaEvaluator(BaseEvaluator):
    """Validates if the LLM output is valid JSON and contains required keys."""

    def __init__(self, required_keys: list[str] = None):
        self.required_keys = required_keys or []

    async def evaluate(
        self, input_text: str, output_text: str, expected: str = "", context: str = ""
    ) -> EvalScore:
        try:
            parsed = json.loads(output_text)
            missing_keys = [k for k in self.required_keys if k not in parsed]

            if missing_keys:
                return EvalScore(
                    name="JSONSchemaCheck",
                    passed=False,
                    score=0.5,
                    reasoning=f"Valid JSON, but missing required keys: {missing_keys}",
                )

            return EvalScore(
                name="JSONSchemaCheck",
                passed=True,
                score=1.0,
                reasoning="Output is valid JSON and satisfies all required schema keys.",
            )
        except json.JSONDecodeError as e:
            return EvalScore(
                name="JSONSchemaCheck",
                passed=False,
                score=0.0,
                reasoning=f"Invalid JSON output: {str(e)}",
            )
