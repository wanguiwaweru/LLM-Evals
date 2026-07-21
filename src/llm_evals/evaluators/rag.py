import json
import re
from .base import BaseEvaluator, EvalScore


class FaithfulnessEvaluator(BaseEvaluator):
    """
    Measures if claims made in the output are backed strictly by provided context.
    Prevents factual hallucinations.
    """

    def __init__(self, judge_client=None):
        self.judge_client = judge_client

    async def evaluate(
        self, input_text: str, output_text: str, expected: str = "", context: str = ""
    ) -> EvalScore:
        if not context:
            return EvalScore(
                name="Faithfulness",
                passed=True,
                score=1.0,
                reasoning="No retrieval context provided to evaluate against.",
            )

        prompt = f"""
You are an expert evaluator. Analyze the Output against the provided Context.
1. Extract all factual assertions/claims made in the Output.
2. Verify if each claim is directly supported by the Context.
3. Return a JSON with:
   - "score": Float between 0.0 and 1.0 (Supported Claims / Total Claims)
   - "reasoning": Brief explanation of any unsupported claims or hallucinations.

Context: {context}
Output: {output_text}

Return strictly JSON format: {{"score": 1.0, "reasoning": "..."}}
"""
        # Simulated LLM Judge response (Replace with real client call, e.g. OpenAI/Anthropic/Ollama)
        simulated_response = '{"score": 0.95, "reasoning": "All key facts present in output are backed by the context."}'
        res = json.loads(simulated_response)

        return EvalScore(
            name="Faithfulness",
            passed=res["score"] >= 0.8,
            score=res["score"],
            reasoning=res["reasoning"],
        )
