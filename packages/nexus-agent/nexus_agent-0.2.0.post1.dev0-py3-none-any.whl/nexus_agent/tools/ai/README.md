# AI Tools

This module provides AI-specific tools for the Nexus Agent framework.

## Tools

### Image Generation (`image_gen.py`)

The image generation tool provides capabilities to generate images using AI models.

#### Features

- Image generation from text descriptions
- Support for different image sizes and styles
- Configurable generation parameters

#### Usage Example

```python
from nexus_agent.tools.ai.image_gen import generate_image

# Generate an image from a text description
image = await generate_image(
    prompt="A beautiful sunset over mountains",
    size="1024x1024"
)
```

## Integration

AI tools are automatically integrated into the Nexus Agent framework and can be accessed through the chat interface. The framework handles parameter validation and error handling for all AI tool operations.

## Development

When adding new AI tools to this module:

1. Create a new Python file in the `ai` directory
2. Implement the tool functionality
3. Add corresponding tests in `tests/nexus_agent/tools/ai/`
4. Update this README with documentation for the new tool

## Testing

AI tool tests are located in `tests/nexus_agent/tools/ai/`. Run the tests specifically for AI tools:

```bash
pytest tests/nexus_agent/tools/ai/
