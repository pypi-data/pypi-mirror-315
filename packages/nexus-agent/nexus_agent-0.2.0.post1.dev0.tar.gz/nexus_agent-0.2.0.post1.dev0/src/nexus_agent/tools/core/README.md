# Core Tools

This module provides core functionality tools for the Nexus Agent framework.

## Tools

### Model Selector (`model_selector.py`)

The model selector tool manages language model selection and configuration.

#### Features

- Dynamic model selection from available OpenRouter models
- Model parameter configuration (temperature, max tokens, etc.)
- Model capability validation

#### Usage Example

```python
from nexus_agent.tools.core.model_selector import select_model

# Select a model with specific parameters
model_config = await select_model(
    model_name="anthropic/claude-2",
    temperature=0.7,
    max_tokens=1000
)
```

## Configuration

Core tools can be configured through environment variables and the framework's configuration system. Key configuration options include:

- `OPENROUTER_API_KEY`: Required for model access
- Model-specific parameters in the chat interface
- System-level configurations in `agent.py`

## Integration

Core tools are fundamental to the Nexus Agent framework and are automatically integrated into the system. They provide essential functionality that other tools and components rely on.

## Development

When adding new core tools:

1. Create a new Python file in the `core` directory
2. Implement the core functionality
3. Add corresponding tests in `tests/nexus_agent/tools/core/`
4. Update this README with documentation for the new tool

### Best Practices

- Maintain backward compatibility
- Include comprehensive error handling
- Provide clear documentation
- Add type hints for all functions
- Write thorough tests

## Testing

Core tool tests are located in `tests/nexus_agent/tools/core/`. Run the tests specifically for core tools:

```bash
pytest tests/nexus_agent/tools/core/
```

## Error Handling

Core tools implement robust error handling to ensure system stability:

- Invalid model selections
- Configuration errors
- API communication issues
- Parameter validation failures
