# I/O Tools

This module provides input/output tools for the Nexus Agent framework, handling file operations and web browsing capabilities.

## Tools

### File Operations (`file_operation.py`)

A tool for handling file system operations safely and efficiently.

#### Features

- File reading and writing
- Directory operations
- File type detection
- Stream handling
- Path validation

#### Usage Example

```python
from nexus_agent/tools/io/file_operation import read_file, write_file

# Read file content
content = await read_file("path/to/file.txt")

# Write to file
await write_file(
    path="path/to/output.txt",
    content="Hello, World!",
    mode="w"
)
```

### Web Browser (`web_browser.py`)

A tool for web interaction and scraping capabilities.

#### Features

- Web page navigation
- Content extraction
- Screenshot capture
- Form interaction
- JavaScript execution
- Cookie handling

#### Usage Example

```python
from nexus_agent.tools.io.web_browser import browse_page

# Navigate and extract content
result = await browse_page(
    url="https://example.com",
    extract_selector=".main-content"
)
```

## Security

I/O tools implement several security measures:

1. File Operations
   - Path validation and sanitization
   - Permission checking
   - File size limits
   - Type verification

2. Web Operations
   - URL validation
   - Request rate limiting
   - Content type verification
   - SSL/TLS enforcement

## Configuration

I/O tools can be configured through environment variables and the framework's configuration system:

- `MAX_FILE_SIZE`: Maximum file size for operations
- `ALLOWED_DOMAINS`: List of allowed web domains
- `REQUEST_TIMEOUT`: Default timeout for web requests
- `DOWNLOAD_PATH`: Default path for downloaded files

## Integration

I/O tools are integrated into the chat interface and can be accessed through specific commands or prompts. The framework handles parameter validation and provides appropriate feedback for all operations.

## Development

When adding new I/O tools:

1. Create a new Python file in the `io` directory
2. Implement the tool functionality with security in mind
3. Add corresponding tests in `tests/nexus_agent/tools/io/`
4. Update this README with documentation for the new tool

### Best Practices

- Implement proper error handling
- Include security measures
- Add type hints
- Write comprehensive tests
- Document all functions
- Handle resources properly (close files, connections)

## Testing

I/O tool tests are located in `tests/nexus_agent/tools/io/`. Run the tests specifically for I/O tools:

```bash
pytest tests/nexus_agent/tools/io/
```

## Error Handling

I/O tools implement robust error handling for various scenarios:

- File not found
- Permission denied
- Network errors
- Invalid URLs
- Timeout errors
- Resource exhaustion
