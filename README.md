# Immich MCP Server

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)](https://fastapi.tiangolo.com/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-orange.svg)](https://modelcontextprotocol.io/)

A production-ready Model Context Protocol (MCP) server for the Immich photo management API. This server provides a standardized interface for AI assistants to interact with your Immich photo library, enabling intelligent photo management, search, and organization capabilities.

## 🚀 Features

- **Complete Immich API Integration**: Full access to albums, assets, search, and upload functionality
- **Production-Ready**: Built with caching, rate limiting, and error handling
- **FastAPI Integration**: Modern async web framework with automatic API documentation
- **Comprehensive Testing**: Full test coverage with mocked API responses
- **Environment Configuration**: Flexible configuration via environment variables or .env files
- **Performance Optimized**: Caching and rate limiting for optimal performance
- **Type Safety**: Full type hints and Pydantic validation

## 🚀 Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-org/immich-mcp.git
cd immich-mcp

# Install dependencies
pip install -e .
```
For more details, see the [full installation guide](INSTALL.md).

### 2. Configuration

Create a `.env` file in the project root with your Immich server details:

```bash
# .env
IMMICH_BASE_URL=https://your-immich-server.com
IMMICH_API_KEY=your-immich-api-key-here
AUTH_TOKEN=your-secret-auth-token-here
```
For more details, see the [full configuration guide](CONFIGURATION.md).

### 3. Usage

Start the server with the following command:

```bash
immich-mcp
```

The server will start on `http://0.0.0.0:8626`. For more details, see the [full usage guide](USAGE.md).

## 📚 Documentation

For more detailed information, please see the full documentation:

- [Installation](INSTALL.md)
- [Configuration](CONFIGURATION.md)
- [Usage](USAGE.md)
- [Usage Examples](USAGE_EXAMPLES.md)
- [API Reference](API_REFERENCE.md)
- [Development](DEVELOPMENT.md)
- [Testing](TESTING.md)
- [Deployment](DEPLOYMENT.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [License](LICENSE)

## 🙏 Acknowledgments

- [Immich](https://immich.app/) for the amazing photo management platform
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [MCP](https://modelcontextprotocol.io/) for the protocol specification

---

**Made with ❤️ by the Immich MCP Team**
