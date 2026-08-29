from dataclasses import dataclass


@dataclass
class ComplexityResult:

    tier: str
    score: int
    reasons: list[str]