import time

from openai import OpenAI

from app.models.config import ModelConfig
from app.models.response import LLMResponse
from app.providers.base import LLMProvider

class OpenAIProvider(LLMProvider):
    
    def __init__(self, config: ModelConfig, api_key: str):
        super().__init__(config)

        self.client = OpenAI(
            api_key=api_key
        )
    
    def generate(self, prompt: str) -> LLMResponse:

        start_time = time.perf_counter()

       # pyrefly: ignore [parse-error]
       response = self.client.chat.completions.create(
            model = self.config.model_id,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        # pyrefly: ignore [parse-error]
        end_time = time.perf_counter()

        latency = end_time - start_time

        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens

        cost = (
            (input_tokens / 1_000_000)
            * self.config.input_cost_per_1m
        ) + (
            (output_tokens / 1_000_000)
            * self.config.output_cost_per_1m
        )

        return LLMResponse(
            output=str(response.choices[0].message.content),
            model=self.config.model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            latency=latency,
            cost=cost
        )
