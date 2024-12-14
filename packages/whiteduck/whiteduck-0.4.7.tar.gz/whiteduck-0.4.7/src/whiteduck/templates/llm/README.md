# Chat Template Project

A flexible chat interface built with Chainlit that supports multiple LLM providers through LiteLLM.

## Features

- 🤖 Multi-model support through LiteLLM
- 💬 Persistent chat history
- 🔌 Easy model switching via environment variables
- 🎨 Clean Chainlit UI
- 🐛 Rich debugging output
- 📝 JSON fallback for development

## Prerequisites

### UV Package Manager

This project uses [UV](https://github.com/astral-sh/uv), a modern Python package manager.

#### Installation

Visit the official documentation for detailed installation instructions:
- [UV Installation Guide](https://docs.astral.sh/uv/)
- [UV GitHub Repository](https://github.com/astral-sh/uv)

## 🛠 Setup & Development

### Initial Setup

Synchronize all project dependencies:
```bash
uv sync --all-groups
```

## Configuration

Copy `.env.example` to `.env` and configure your environment variables:

```env
CHAT_MODEL="gpt-4"        # Your chosen model
OPENAI_API_KEY="..."      # OpenAI API key if using OpenAI models
AZURE_OPENAI_API_KEY="..." # Azure API key if using Azure models
```

Use LiteLLM's syntax to define models... for example `CHAT_MODEL="ollama_chat/mymodel"` will use your local ollama instance.

### API Keys

Different models require different API keys. Refer to the [LiteLLM documentation](https://docs.litellm.ai/docs/providers/azure) to determine which API keys are needed for your chosen model.

For example:
- OpenAI models require `OPENAI_API_KEY`
- Azure models require `AZURE_OPENAI_API_KEY`

### Supported Models

The `CHAT_MODEL` variable can be set to any model supported by LiteLLM. If not set, the application will run in development mode, returning JSON representations of messages.

## Usage

Run the chat interface:

```bash
uv run poe chat # or just poe chat if in .venv
```

This will start a Chainlit server, typically accessible at `http://localhost:8000`.

### Development Mode

If `CHAT_MODEL` is not set, the application will run in development mode, where it:
- Displays Rich debug information for messages
- Returns JSON representations of inputs
- Allows testing the chat interface without an LLM

### Production Mode

When `CHAT_MODEL` is set:
- Messages are sent to the specified LLM
- Chat history is maintained
- Responses are streamed back to the UI


## Dependencies

Key dependencies (see `pyproject.toml` for complete list):

- chainlit (>=1.3.2) - Chat interface
- litellm (>=1.55.0) - LLM provider abstraction
- python-decouple (>=3.8) - Environment configuration
- rich (>=13.9.4) - Debug output
- pydantic (==2.10.1) - Data validation
- loguru (>=0.7.3) - Logging

## Development Tools

Development dependencies include:

- poethepoet - Task runner
- pytest - Testing
- ruff - Linting and formatting

## License

This project is licensed under the MIT License - see the LICENSE file for details.
