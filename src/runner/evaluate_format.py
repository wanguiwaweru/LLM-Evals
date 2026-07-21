import re


# Example Evaluator: Schema / Format Check
def evaluate_format(output: str) -> bool:
    """Verifies output contains structured tags or expected markers."""
    return bool(re.search(r"^Final Answer:", output, re.MULTILINE))
