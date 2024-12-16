# Nexus Agent

> **Note**: This is an ongoing project under active development.

A powerful chatbot framework with extensive tool integration capabilities, powered by OpenRouter API. This framework provides a web interface for interacting with various language models while enabling custom function execution through a modular tool system.

## Features

- Web-based chat interface using Streamlit
- Support for multiple language models via OpenRouter
- Modular tool system with categories:
  - [AI Tools](src/nexus_agent/tools/ai/): Image generation and AI-specific capabilities
  - [Core Tools](src/nexus_agent/tools/core/): Core functionality like model selection
  - [Development Tools](src/nexus_agent/tools/dev/): Secure code execution in Docker containers for multiple languages
  - [I/O Tools](src/nexus_agent/tools/io/): File operations and web browsing
  - [Utility Tools](src/nexus_agent/tools/utils/): Math, search, time, and weather utilities
- Streaming responses
- Configurable model parameters
- Comprehensive test coverage
- Strong type checking and code quality tools

## Requirements

- Python 3.11 or higher
- OpenRouter API key
- Docker (for secure code execution)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Nexus-Agent.git
cd Nexus-Agent
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenRouter API key:

```bash
OPENROUTER_API_KEY=your_api_key_here
```

You can get an API key from [OpenRouter](https://openrouter.ai/).

4. Ensure Docker is installed and running:
   - [Install Docker](https://docs.docker.com/get-docker/) if not already installed
   - Start the Docker daemon
   - Verify Docker is running: `docker --version`

## Usage

1. Start the Streamlit interface:

```bash
./run_stlit.sh
```

or

```bash
streamlit run src/main.py
```

2. Your default web browser will automatically open to the Streamlit interface. If it doesn't, navigate to the URL shown in the terminal (typically `http://localhost:8501`).

3. Select a model from the dropdown menu and start chatting!

## Project Structure

```
Nexus-Agent/
├── src/
│   └── nexus_agent/
│       ├── tools/                 # Modular tool system
│       │   ├── ai/               # AI-specific tools
│       │   ├── core/             # Core functionality
│       │   ├── dev/              # Development tools
│       │   ├── io/               # I/O operations
│       │   └── utils/            # Utility functions
│       ├── agent.py              # Core agent implementation
│       └── interface.py          # Streamlit web interface
├── tests/                        # Comprehensive test suite
├── requirements.txt              # Project dependencies
└── pyproject.toml               # Project configuration
```

## Available Tools

### AI Tools

- Image generation capabilities
- See [AI Tools Documentation](src/nexus_agent/tools/ai/README.md)

### Core Tools

- Model selection and configuration
- See [Core Tools Documentation](src/nexus_agent/tools/core/README.md)

### Development Tools

- Secure code execution in Docker containers
  - Python with visualization support
  - JavaScript (Node.js)
  - Shell commands
- Resource and security controls
- See [Development Tools Documentation](src/nexus_agent/tools/dev/README.md)

### I/O Tools

- File operations
- Web browsing capabilities
- See [I/O Tools Documentation](src/nexus_agent/tools/io/README.md)

### Utility Tools

- Mathematical calculations
- Web search functionality
- Time zone utilities
- Weather information
- See [Utility Tools Documentation](src/nexus_agent/tools/utils/README.md)

## Development

### Dependencies

The project uses several key dependencies:

- Core: aiohttp, pydantic, openai, streamlit
- Docker: docker-py for container management
- Testing: pytest, pytest-asyncio, pytest-cov
- Development: black, isort, mypy, pylint, pre-commit

### Code Quality

The project maintains high code quality standards through:

- Type checking with mypy
- Code formatting with black and isort
- Linting with pylint
- Pre-commit hooks for automated checks
- Comprehensive test coverage

### Testing

Run the test suite:

```bash
pytest
```

For test coverage report:

```bash
pytest --cov=nexus_agent
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality checks pass
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details
