from abc import ABC, abstractmethod

from app.models.config import ModelConfig
from app.models.response import LLMResponse


class LLMProvider(ABC):

    def __init__(self, config: ModelConfig):
        self.config = config

    @abstractmethod
    def generate(self, prompt: str) -> LLMResponse:
        pass