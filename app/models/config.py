from dataclasses import dataclass

@dataclass
class ModelConfig:
    provider: str
    model_id: str
    input_cost_per_1m: float
    output_cost_per_1m: float
    average_latency: float
    quality_tier: str
    enabled: bool = True