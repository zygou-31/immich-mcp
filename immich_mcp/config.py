import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, HttpUrl, ValidationError
import logging
import httpx

# Load environment variables from .env file if not in test environment
if os.getenv("TESTING") != "true":
    load_dotenv()

logger = logging.getLogger(__name__)


class ImmichConfig(BaseSettings):
    """
    Configuration class for Immich MCP server with Pydantic validation.

    This class manages all configuration settings for the Immich MCP server,
    including server connection details, authentication credentials, and
    operational parameters. It provides automatic validation and type checking
    for all configuration values.

    Attributes:
        immich_base_url: Base URL of the Immich API server
        immich_api_key: API key for authenticating with Immich
        immich_timeout: HTTP request timeout in seconds
        immich_max_retries: Maximum number of retry attempts for failed requests

    Example:
        >>> config = ImmichConfig(
        ...     immich_base_url="https://immich.example.com/api",
        ...     immich_api_key="your-api-key-here"
        ... )
        >>> print(config.immich_base_url)
        https://immich.example.com/api
    """

    immich_base_url: HttpUrl = Field(
        ...,
        env="IMMICH_BASE_URL",
        description="Base URL of the Immich API server (must end with /api)",
    )
    immich_api_key: str = Field(
        ...,
        env="IMMICH_API_KEY",
        description="API key for authenticating with Immich",
        min_length=10,
        max_length=100,
    )
    immich_timeout: int = Field(
        default=30,
        env="IMMICH_TIMEOUT",
        description="HTTP request timeout in seconds",
        ge=5,
        le=300,
    )
    immich_max_retries: int = Field(
        default=3,
        env="IMMICH_MAX_RETRIES",
        description="Maximum number of retry attempts for failed requests",
        ge=0,
        le=10,
    )

    async def test_connection(self) -> bool:
        """
        Test connectivity to the Immich API server.

        This method performs a lightweight health check to verify that the
        configured Immich server is accessible and responding correctly.

        Returns:
            bool: True if connection is successful, False otherwise

        Example:
            >>> config = ImmichConfig(...)
            >>> if await config.test_connection():
            ...     print("Connection successful")
            ... else:
            ...     print("Connection failed")
        """
        try:
            async with httpx.AsyncClient(
                base_url=str(self.immich_base_url),
                headers={"x-api-key": self.immich_api_key},
                timeout=self.immich_timeout,
            ) as client:

                # Test a simple endpoint that should be available if the server is up
                response = await client.get("/server-info/ping")
                return response.status_code == 200

        except httpx.RequestError as e:
            logger.error(f"Connection test failed: {e}")
            return False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="IMMICH_",
        extra="ignore",
        json_schema_extra={
            "env": {
                "immich_base_url": "IMMICH_BASE_URL",
                "immich_api_key": "IMMICH_API_KEY",
                "immich_timeout": "IMMICH_TIMEOUT",
                "immich_max_retries": "IMMICH_MAX_RETRIES",
            }
        },
    )


def load_config() -> ImmichConfig:
    """
    Load and validate the configuration from environment variables.

    This function loads configuration from environment variables and .env files,
    performs validation using Pydantic, and returns a validated configuration
    instance. It provides helpful error messages if validation fails.

    Returns:
        ImmichConfig: Validated configuration instance ready for use

    Raises:
        ValidationError: If configuration validation fails, with detailed
                        error messages about what went wrong

    Example:
        >>> try:
        ...     config = load_config()
        ...     print("Configuration loaded successfully")
        ... except ValidationError as e:
        ...     print(f"Configuration error: {e}")
    """
    try:
        config = ImmichConfig()
        logger.info("Configuration loaded successfully")
        return config

    except ValidationError as e:
        error_msg = "Invalid configuration:\n" + "\n".join(
            [f"- {error['loc'][0]}: {error['msg']}" for error in e.errors()]
        )
        logger.error(error_msg)
        raise
