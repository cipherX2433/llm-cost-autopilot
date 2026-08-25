from dataclasses import dataclass

@dataclass
class LLMResponse:
    output: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency: float
    cost: float