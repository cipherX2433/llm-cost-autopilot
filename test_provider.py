from app import providers
from app.models import config
import os

# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

from app.registry import ModelRegistry
from pathlib import Path

load_dotenv()


def main():

    BASE_DIR = Path(__file__).resolve().parent
    config_path = BASE_DIR / "app" / "config" / "models.yaml"

    registry = ModelRegistry(
        config_path=config_path,
        openai_key=os.getenv("OPENAI_API_KEY"),
        anthropic_key=os.getenv("ANTHROPIC_API_KEY")
    )

    print("\nAvailable models:")

    for model in registry.list_models():
        print("-", model)

    result = registry.get_enabled_models()
    print(result)

    results = registry.get_models_by_quality("medium")
    print(results)

    prompt = "Explain what an API is in simple terms."


    # print("\n========== OPENAI ==========")

    # openai = registry.get("gpt-4o-mini")

    # response = openai.generate(prompt)

    # print("Model:", response.model)
    # print("Output:", response.output)
    # print("Input tokens:", response.input_tokens)
    # print("Output tokens:", response.output_tokens)
    # print("Total tokens:", response.total_tokens)
    # print("Latency:", response.latency)
    # print("Cost:", response.cost)


    # print("\n========== ANTHROPIC ==========")

    # anthropic = registry.get("claude-haiku")

    # response = anthropic.generate(prompt)

    # print("Model:", response.model)
    # print("Output:", response.output)
    # print("Input tokens:", response.input_tokens)
    # print("Output tokens:", response.output_tokens)
    # print("Total tokens:", response.total_tokens)
    # print("Latency:", response.latency)
    # print("Cost:", response.cost)


    # print("\n========== OLLAMA ==========")

    # ollama = registry.get("llama3.2")

    # response = ollama.generate(prompt)

    # print("Model:", response.model)
    # print("Output:", response.output)
    # print("Input tokens:", response.input_tokens)
    # print("Output tokens:", response.output_tokens)
    # print("Total tokens:", response.total_tokens)
    # print("Latency:", response.latency)
    # print("Cost:", response.cost)


if __name__ == "__main__":
    main()