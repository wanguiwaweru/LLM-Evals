from dataclasses import dataclass


@dataclass
class EvalResult:
    case_id: str
    output: str
    latency_sec: float
    passed_format: bool
    judge_score: float  # Scale 0.0 - 1.0
    reasoning: str
