import asyncio


# Example Evaluator: LLM-as-a-Judge
async def evaluate_with_judge(
    input_prompt: str, output: str, expected: str
) -> tuple[float, str]:
    """
    Simulates calling an impartial model (e.g., GPT-4 / Claude) to judge correctness.
    In production, this executes a prompt returning structured JSON: {"score": float, "reason": str}.
    """
    # Mocking evaluation response for demonstration
    await asyncio.sleep(0.05)

    if expected.lower() in output.lower():
        return 1.0, "Output accurately covers ground truth facts."
    return 0.2, "Output missed key information required by ground truth."
