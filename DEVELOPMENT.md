# 🧪 Development

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-org/immich-mcp.git
cd immich-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Project Structure

```
immich-mcp/
├── immich_mcp/
│   ├── __init__.py
│   ├── client.py          # Immich API client
│   ├── config.py          # Configuration management
│   ├── tools.py           # MCP tools implementation
│   ├── cache.py           # Caching utilities
│   ├── rate_limiter.py    # Rate limiting
│   └── server.py          # FastAPI server
├── tests/
│   ├── __init__.py
│   └── immich_mcp/
│       ├── test_client.py
│       ├── test_config.py
│       └── test_tools.py
├── immich_mcp/
│   ├── cli.py             # Command-line interface
├── pyproject.toml        # Project configuration
├── README.md            # This file
└── .env.example         # Environment template
```

### Code Style

This project uses:
- **ruff** for code formatting and linting
- **mypy** for type checking

```bash
# Format and lint code
ruff check . --fix && ruff format .

# Type check
mypy immich_mcp/
```
