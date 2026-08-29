from typing import Optional
from app.models.config import ModelConfig
from app.providers.openai_provider import OpenAIProvider
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.ollama_provider import OllamaProvider
import os
import yaml

REGISTRY = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "ollama": OllamaProvider
}

class ModelRegistry:

    def __init__(self, config_path: str, openai_key: Optional[str], anthropic_key: Optional[str]):
        
        self.models = {}

        self.openai_key = openai_key,
        self.anthropic_key = anthropic_key

        self._load_config(config_path)

    def _load_config(self, config_path: str):

            with open(config_path, "r") as file:
                config = yaml.safe_load(file)
            
            models = config.get("models", {})

            for model_name, model_data in models.items():
                model_config = ModelConfig(
                        provider=model_data["provider"],
                        model_id=model_data["model_id"],
                        input_cost_per_1m=model_data["input_cost_per_1m"],
                        output_cost_per_1m=model_data["output_cost_per_1m"],
                        average_latency=model_data["average_latency"],
                        quality_tier=model_data["quality_tier"],
                        enabled=model_data.get("enabled", True)
                )

                provider = self._create_provider(
                    model_config
                )

                self.models[model_name] = provider

    def _create_provider(self, config: ModelConfig):

            if config.provider == "openai":
                return OpenAIProvider(
                    config=config,
                    api_key=self.openai_key
                )

            elif config.provider == "anthropic":
                return AnthropicProvider(
                    config=config,
                    api_key=self.anthropic_key
                )

            elif config.provider == "ollama":
                return OllamaProvider(
                    config=config
                )
            else:
                raise ValueError(
                f"Unsupported provider: {config.provider}"
            )

    def get(self, model_name: str):

            if model_name not in self.models:
                raise ValueError(
                    f"Model {model_name} not found"
                )
            
            model = self.models[model_name]

            if not model.config.enabled:
                raise ValueError(
                    f"Model {model_name} not enabled"
                )

            return model

    def list_models(self):
            return list(self.models.keys())

    def get_config(self, model_name: str):

            if model_name not in self.models:
                raise ValueError(
                    f"Model {model_name} not found"
                )

            return self.models[model_name].config
    def get_enabled_models(self):
        enabled_models = []
        for name, provider in self.models.items():
            if provider.config.enabled:
                enabled_models.append(name)
        return enabled_models
    
    def get_models_by_quality(self, quality_tier: str):
        models = []
        for name, provider in self.models.items():
            if provider.config.quality_tier == quality_tier:
                models.append(name)
        return models

        