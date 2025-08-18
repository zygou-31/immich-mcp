import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, HttpUrl, ValidationError, model_validator
from typing import Optional
import logging
import httpx

# Load environment variables from .env file if not in test environment
if os.getenv("TESTING") != "true":
    load_dotenv()

logger = logging.getLogger(__name__)


class ImmichConfig(BaseSettings):
    """
    Configuration class for Immich MCP server with Pydantic validation.
    """

    immich_base_url: HttpUrl = Field(
        ...,
        description="Base URL of the Immich API server (must end with /api)",
    )
    immich_api_key: Optional[str] = Field(
        default=None,
        description="API key for authenticating with Immich",
        min_length=10,
        max_length=100,
    )
    immich_api_key_file: Optional[str] = Field(
        default=None,
        description="Path to a file containing the Immich API key",
    )
    immich_timeout: int = Field(
        default=30,
        description="HTTP request timeout in seconds",
        ge=5,
        le=300,
    )
    immich_max_retries: int = Field(
        default=3,
        description="Maximum number of retry attempts for failed requests",
        ge=0,
        le=10,
    )

    # Server settings
    mcp_port: int = Field(
        default=8626,
        description="Port to run the MCP server on",
        ge=1024,
        le=65535,
    )
    mcp_base_url: str = Field(
        default="",
        description="Base URL for the MCP server, for reverse proxy use",
    )

    # Auth settings
    auth_token: Optional[str] = Field(
        default=None,
        min_length=10,
        description="Bearer token for authenticating with the MCP server",
    )

    auth_token_file: Optional[str] = Field(
        default=None,
        description="Path to a file containing the auth token",
    )

    @model_validator(mode="after")
    def load_secrets_from_files(self):
        """
        Load secrets from files if specified.
        """
        if self.auth_token_file:
            try:
                with open(self.auth_token_file, "r") as f:
                    self.auth_token = f.read().strip()
            except FileNotFoundError:
                raise ValueError(f"Auth token file not found: {self.auth_token_file}")

        if self.immich_api_key_file:
            try:
                with open(self.immich_api_key_file, "r") as f:
                    self.immich_api_key = f.read().strip()
            except FileNotFoundError:
                raise ValueError(
                    f"Immich API key file not found: {self.immich_api_key_file}"
                )

        if not self.auth_token:
            raise ValueError("An auth token must be configured")

        if not self.immich_api_key:
            raise ValueError("An Immich API key must be configured")

        return self

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
                "mcp_port": "MCP_PORT",
                "mcp_base_url": "MCP_BASE_URL",
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
        # Build a robust error message even if error['loc'] shape varies
        parts = []
        for error in e.errors():
            loc = error.get("loc")
            if isinstance(loc, (list, tuple)) and len(loc) > 0:
                loc_str = ".".join(str(x) for x in loc)
            else:
                loc_str = str(loc)
            parts.append(f"- {loc_str}: {error.get('msg')}")

        error_msg = "Invalid configuration:\n" + "\n".join(parts)
        logger.error(error_msg)
        raise
