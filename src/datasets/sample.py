from dataclasses import dataclass


@dataclass
class EvalSample:
    id: str
    input_prompt: str
    context: str
    expected_ground_truth: str
