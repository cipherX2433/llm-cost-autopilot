import time

import httpx

from app.models.config import ModelConfig
from app.models.response import LLMResponse
from app.providers.base import LLMProvider


class OllamaProvider(LLMProvider):

    def __init__(
        self,
        config: ModelConfig,
        base_url: str = "http://localhost:11434"
    ):
        super().__init__(config)

        self.base_url = base_url

    def generate(self, prompt: str) -> LLMResponse:

        start_time = time.perf_counter()

        response = httpx.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.config.model_id,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        end_time = time.perf_counter()

        latency = end_time - start_time

        input_tokens = data.get("prompt_eval_count", 0)
        output_tokens = data.get("eval_count", 0)
        total_tokens = input_tokens + output_tokens

        cost = (
            (input_tokens / 1_000_000)
            * self.config.input_cost_per_1m
        ) + (
            (output_tokens / 1_000_000)
            * self.config.output_cost_per_1m
        )

        return LLMResponse(
            output=data["message"]["content"],
            model=self.config.model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency=latency,
            cost=cost
        )