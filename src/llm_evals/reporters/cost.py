from dataclasses import dataclass

# Rates per 1,000,000 tokens (USD)
MODEL_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
}


@dataclass
class CostMetrics:
    prompt_tokens: int
    completion_tokens: int
    total_cost_usd: float


def calculate_token_cost(
    model_name: str, prompt_tokens: int, completion_tokens: int
) -> CostMetrics:
    rates = MODEL_PRICING.get(model_name, {"input": 0.0, "output": 0.0})

    cost_input = (prompt_tokens / 1_000_000) * rates["input"]
    cost_output = (completion_tokens / 1_000_000) * rates["output"]
    total_cost = cost_input + cost_output

    return CostMetrics(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_cost_usd=round(total_cost, 6),
    )
