import time

# pyrefly: ignore [missing-import]
from anthropic import Anthropic

from app.models.config import ModelConfig
from app.models.response import LLMResponse
from app.providers.base import LLMProvider


class AnthropicProvider(LLMProvider):

    def __init__(self, config: ModelConfig, api_key: str):
        super().__init__(config)

        self.client = Anthropic(
            api_key=api_key
        )

    def generate(self, prompt: str) -> LLMResponse:

        start_time = time.perf_counter()

        response = self.client.messages.create(
            model=self.config.model_id,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        end_time = time.perf_counter()

        latency = end_time - start_time

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = input_tokens + output_tokens

        cost = (
            (input_tokens / 1_000_000)
            * self.config.input_cost_per_1m
        ) + (
            (output_tokens / 1_000_000)
            * self.config.output_cost_per_1m
        )

        output = response.content[0].text

        return LLMResponse(
            output=output,
            model=self.config.model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency=latency,
            cost=cost
        )