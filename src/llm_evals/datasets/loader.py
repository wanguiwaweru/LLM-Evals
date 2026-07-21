import json
from dataclasses import dataclass


@dataclass
class EvalSample:
    id: str
    input_prompt: str
    context: str
    expected_ground_truth: str


def load_dataset(path: str) -> list[EvalSample]:
    # Use "utf-8-sig" to safely strip any Windows UTF-8 BOM headers
    with open(path, "r", encoding="utf-8-sig") as f:
        raw_data = json.load(f)
    return [EvalSample(**item) for item in raw_data]
