# Development Tools

This module provides development-focused tools for the Nexus Agent framework, enabling code interpretation and shell command execution capabilities.

## Tools

### Code Interpreter (`code_interpreter.py`)

A tool for interpreting and executing code snippets safely using Docker containers.

#### Key Features

- Secure code execution in isolated Docker containers
- Support for multiple languages (Python, JavaScript, Shell)
- Support for visualization libraries (matplotlib, etc.)
- Package dependency management
- Resource limitations and security controls
- Input/output handling
- Error reporting and debugging information

#### Requirements

- Docker must be installed and running on the system

#### Example Usage

```python
from nexus_agent.tools.dev.code_interpreter import CodeInterpreter

interpreter = CodeInterpreter()

# Execute Python code
result = await interpreter.execute_python(
    code="print('Hello, World!')",
    packages=["numpy", "pandas"]  # Optional additional packages
)

# Execute JavaScript code
result = await interpreter.execute_javascript(
    code="console.log('Hello from Node.js!')"
)

# Execute shell commands
result = await interpreter.execute_shell(
    code="ls -la"
)
```

### Shell Command Executor (`shell.py`)

A tool for executing shell commands with safety measures and output handling.

#### Features

- Secure command execution
- Output streaming
- Error handling
- Command timeout management
- Platform-specific command adaptation

#### Usage Example

```python
from nexus_agent.tools.dev.shell import execute_shell_command

result = await execute_shell_command(
    command="ls -la",
    timeout=60
)
```

## Security

Development tools implement several security measures:

1. Docker Container Isolation
   - Process isolation
   - Resource limitations
   - Network isolation
   - Filesystem isolation
   - Memory limits
   - CPU restrictions

2. Command Validation
   - Allowlist/blocklist for shell commands
   - Syntax checking for code
   - Resource usage limits

3. Error Handling
   - Graceful failure handling
   - Detailed error reporting
   - Resource cleanup
   - Container cleanup

## Configuration

Development tools can be configured through environment variables and the framework's configuration system:

- `MAX_EXECUTION_TIME`: Maximum execution time for commands
- `ALLOWED_MODULES`: List of allowed Python modules
- `SHELL_COMMAND_TIMEOUT`: Default timeout for shell commands
- Docker-specific settings are configured in the CodeInterpreter class

## Integration

Development tools are integrated into the chat interface and can be accessed through specific commands or prompts. The framework handles parameter validation and provides appropriate feedback for all operations.

## Development

When adding new development tools:

1. Create a new Python file in the `dev` directory
2. Implement the tool functionality with security in mind
3. Add corresponding tests in `tests/nexus_agent/tools/dev/`
4. Update this README with documentation for the new tool

### Best Practices

- Always implement security measures
- Include comprehensive error handling
- Provide clear documentation
- Add type hints for all functions
- Write thorough tests
- Clean up resources (especially Docker containers)

## Testing

Development tool tests are located in `tests/nexus_agent/tools/dev/`. Run the tests specifically for development tools:

```bash
pytest tests/nexus_agent/tools/dev/
```

## Error Handling

Development tools implement robust error handling for various scenarios:

- Invalid commands or code
- Execution timeouts
- Resource exhaustion
- Security violations
- System-level errors
- Docker-related errors (container creation, execution, cleanup)
