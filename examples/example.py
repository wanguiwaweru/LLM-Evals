import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "src"))

from datasets.sample import EvalSample
from runner.runner import EvalRunner


# Mock application wrapper for demonstration
async def mock_llm_app(prompt: str, context: str) -> str:
    await asyncio.sleep(0.1)  # Simulate network latency
    return "Final Answer: The system handles real-time updates seamlessly."


# Usage
async def main():
    cases = [
        EvalSample(
            id="test_001",
            input_prompt="Summarize real-time capabilities",
            context="System supports live websockets and instant sync.",
            expected_ground_truth="real-time updates",
        )
    ]

    runner = EvalRunner(target_llm_fn=mock_llm_app)
    results = await runner.run_suite(cases)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
