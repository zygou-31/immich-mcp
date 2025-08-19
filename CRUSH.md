# Immich MCP Development Guide

## Project Overview
- FastAPI-based MCP server for Immich photo management
- Asynchronous client for Immich API interactions
- Caching and rate limiting for performance

## Build/Run Commands
```bash
# Install dependencies
pip install -e ".[dev]"

# Start development server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Run all tests
pytest

# Run specific test file
pytest tests/immich_mcp/test_client.py

# Run single test
pytest tests/immich_mcp/test_client.py::test_specific_function

# Format and lint code
ruff check . --fix && ruff format .

# Type checking
mypy immich_mcp/

# Pyright type checking
pyright immich_mcp/
```

## Code Style Guidelines
1. Use ruff for formatting and linting with default settings
3. Type hints required for all functions
4. Use Pydantic for configuration and data validation
5. Error handling with HTTPException for API endpoints
6. Async/await for all I/O operations
7. Docstrings for all public functions (Google style)
8. Naming: snake_case for variables/functions, PascalCase for classes

## Testing
- Use pytest with respx for HTTP mocking
- Place tests in tests/ directory matching source structure
- Use async tests for async functions
- Test both success and error cases

## Configuration
- Use pydantic-settings for environment configuration
- .env file for local development settings
- Validate all configuration at startup

## Git Hooks
- Pre-commit hooks for formatting and linting
- Run `pre-commit install` after cloning