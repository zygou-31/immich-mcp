# 🛠 Installation

### Prerequisites

- Python 3.10 or higher
- Immich server instance (v1.90.0+)
- Immich API key (obtain from your Immich server settings)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/your-org/immich-mcp.git
cd immich-mcp

# Install dependencies
pip install -e .

# Or install from PyPI (when available)
pip install immich-mcp
```

### Development Install

```bash
# Clone and install in development mode
git clone https://github.com/your-org/immich-mcp.git
cd immich-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```
