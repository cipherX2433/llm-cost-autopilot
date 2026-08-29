# LLM Cost Autopilot 🚀

**LLM Cost Autopilot** is an intelligent LLM management and routing framework designed to optimize cost, latency, and model selection across multiple AI providers (OpenAI, Anthropic, Ollama). 

It dynamically loads model configurations, tracks token usage costs, evaluates prompt complexity, and enables smart routing to the most cost-effective model for any given task.

---

## 🌟 Features

- 🔌 **Multi-Provider Integration**: Unified interface for **OpenAI**, **Anthropic**, and local **Ollama** models.
- ⚙️ **YAML-Driven Configuration**: Easily configure pricing (per 1M tokens), latency benchmarks, quality tiers, and model enablement via `app/config/models.yaml`.
- 🧠 **Prompt Complexity Analyzer**: Dynamically scores and categorizes incoming prompts into complexity tiers (`tier_1`, `tier_2`, `tier_3`) based on keyword analysis and length heuristics.
- 📦 **Centralized Model Registry**: Dynamically instantiates provider clients, handles credentials, and queries models by quality tier or active status.
- 📊 **Normalized Response & Cost Metrics**: Unified `LLMResponse` model capturing generated output, latency, exact token usage, and calculated API cost.

---

## 📁 Project Structure

```
llm-cost-autopilot/
├── app/
│   ├── config/
│   │   ├── models.yaml          # Model definitions, pricing & quality tier specs
│   │   └── routing.yaml         # Routing rules configuration
│   ├── models/
│   │   ├── config.py            # Pydantic schema for ModelConfig
│   │   └── response.py          # Unified LLMResponse data structure
│   ├── providers/
│   │   ├── base.py              # Abstract base class for LLM providers
│   │   ├── openai_provider.py   # OpenAI client integration
│   │   ├── anthropic_provider.py# Anthropic Claude client integration
│   │   └── ollama_provider.py   # Local Ollama client integration
│   ├── router/
│   │   ├── complexity.py        # Rule-based prompt complexity scorer
│   │   └── model_router.py      # Core routing engine logic
│   └── registry.py              # Model Registry & provider loader
├── test_provider.py             # Script to verify registry and model execution
├── requirements.txt             # Python dependencies
├── .env                         # API keys and environment variables
└── README.md
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.9+
- (Optional) Local [Ollama](https://ollama.com/) instance for open-source model execution.

### 2. Clone & Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

---

## ⚙️ Configuration (`models.yaml`)

Models are configured declaratively in `app/config/models.yaml`:

```yaml
models:
  gpt-4o-mini:
    provider: openai
    model_id: gpt-4o-mini
    input_cost_per_1m: 0.15
    output_cost_per_1m: 0.60
    average_latency: 1.0
    quality_tier: medium
    enabled: true

  claude-haiku:
    provider: anthropic
    model_id: claude-haiku
    input_cost_per_1m: 0.25
    output_cost_per_1m: 1.25
    average_latency: 1.0
    quality_tier: medium
    enabled: true

  llama3.2:
    provider: ollama
    model_id: llama3.2
    input_cost_per_1m: 0.0
    output_cost_per_1m: 0.0
    average_latency: 2.0
    quality_tier: low
    enabled: false
```

---

## 💡 Usage

### Using the Model Registry

```python
from pathlib import Path
import os
from dotenv import load_dotenv
from app.registry import ModelRegistry

load_dotenv()

config_path = Path("app/config/models.yaml")
registry = ModelRegistry(
    config_path=config_path,
    openai_key=os.getenv("OPENAI_API_KEY"),
    anthropic_key=os.getenv("ANTHROPIC_API_KEY")
)

# List available models
print("Available Models:", registry.list_models())

# Get enabled models
print("Enabled Models:", registry.get_enabled_models())

# Execute request with OpenAI provider
provider = registry.get("gpt-4o-mini")
response = provider.generate("Explain what an API is in simple terms.")

print(f"Model: {response.model}")
print(f"Output: {response.output}")
print(f"Cost: ${response.cost:.6f}")
print(f"Latency: {response.latency:.2f}s")
```

### Analyzing Prompt Complexity

```python
from app.router.complexity import ComplexityAnalyzer

analyzer = ComplexityAnalyzer()

prompt_1 = "Hi, how are you?"
tier = analyzer.analyze(prompt_1)
# Returns: 'tier_1'

prompt_2 = "Design a distributed system architecture for real-time video streaming with micro-services, trade-offs, and data storage strategies."
tier = analyzer.analyze(prompt_2)
# Returns: 'tier_3'
```

---

## 🧪 Testing

Run the test script to verify registry loading and model provider queries:

```bash
python test_provider.py
```

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
