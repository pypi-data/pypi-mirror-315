# Utility Tools

This module provides various utility tools for the Nexus Agent framework, including mathematical operations, search functionality, time handling, and weather information.

## Tools

### Math Solver (`math_solver.py`)

A tool for performing mathematical calculations and solving equations.

#### Math Solver Features

- Basic arithmetic operations
- Complex mathematical expressions
- Unit conversions
- Scientific calculations

#### Math Usage

```python
from nexus_agent.tools.utils.math_solver import solve_expression

result = await solve_expression("2 * (3 + 4) / 2")
```

### Search (`search.py`)

A tool for performing web searches and information retrieval.

#### Search Features

- Web search functionality
- Result filtering
- Content summarization
- Safe search options

#### Search Usage

```python
from nexus_agent.tools.utils.search import web_search

results = await web_search(
    query="python programming",
    max_results=5
)
```

### Time Tools (`time_tools.py`)

A tool for handling time-related operations and conversions.

#### Time Tools Features

- Timezone conversions
- Date formatting
- Time calculations
- Schedule handling

#### Time Example

```python
from nexus_agent.tools.utils.time_tools import get_time

time = await get_time(
    timezone="America/New_York",
    format="full"
)
```

### Weather (`weather.py`)

A tool for retrieving weather information and forecasts.

#### Weather Features

- Current weather conditions
- Weather forecasts
- Location-based weather
- Multiple unit support (metric/imperial)

#### Weather Example

```python
from nexus_agent.tools.utils.weather import get_weather

forecast = await get_weather(
    location="New York",
    units="metric"
)
```

## Configuration

Utility tools can be configured through environment variables and the framework's configuration system:

- `WEATHER_API_KEY`: API key for weather service
- `SEARCH_API_KEY`: API key for search service
- `DEFAULT_TIMEZONE`: Default timezone for time operations
- `TEMPERATURE_UNIT`: Default temperature unit (C/F)

## Integration

Utility tools are integrated into the chat interface and can be accessed through natural language commands. The framework handles parameter validation and provides appropriate feedback for all operations.

## Development

When adding new utility tools:

1. Create a new Python file in the `utils` directory
2. Implement the tool functionality
3. Add corresponding tests in `tests/nexus_agent/tools/utils/`
4. Update this README with documentation for the new tool

### Best Practices

- Include error handling
- Add type hints
- Write comprehensive tests
- Document all functions
- Handle API rate limits
- Implement caching where appropriate

## Testing

Utility tool tests are located in `tests/nexus_agent/tools/utils/`. Run the tests specifically for utility tools:

```bash
pytest tests/nexus_agent/tools/utils/
```

## Error Handling

Utility tools implement robust error handling for various scenarios:

- API errors
- Invalid input
- Network issues
- Rate limiting
- Service unavailability
