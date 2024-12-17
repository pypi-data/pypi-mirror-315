# Init LLM

A toolkit for initializing LLMs(Langchain) and embeddings with multiple providers.
All models are openai compatible.

## Installation

```bash
pip install init-llm
```

## Quick Start

```python
from init_llm import ChatLLM, EmbeddingLLM

# Initialize chat model
llm = ChatLLM('openai')  # or 'azure', 'anthropic', etc.
response = llm.invoke('Hello!')

# Initialize embeddings
embeddings = EmbeddingLLM('text-embedding-3-small')
vector = embeddings.embed_query('Hello world')
```

## Configuration

The package uses two configuration files:
- `model_providers.toml`: Model configurations and provider settings
- `.env`: API keys and other sensitive information

### Auto Configuration
On first use, the package will:
1. Check for configuration files in the working directory
2. If not found, create them automatically with default settings
3. Load environment variables from `.env`

### Custom Configuration
You can specify custom configuration location and env file name:

```python
llm = ChatLLM(
    'openai',
    config_dir='/path/to/config',
    env_file='custom.env'
)
```

## See Supported Providers in model_providers.toml


## License

[MIT](LICENSE)

