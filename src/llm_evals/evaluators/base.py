from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EvalScore:
    name: str
    passed: bool
    score: float
    reasoning: str


class BaseEvaluator(ABC):
    @abstractmethod
    async def evaluate(
        self, input_text: str, output_text: str, expected: str = "", context: str = ""
    ) -> EvalScore:
        pass
