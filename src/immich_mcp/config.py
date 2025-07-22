
import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, HttpUrl, validator, ValidationError
import logging
import httpx

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class ImmichConfig(BaseSettings):
    """
    Configuration class for Immich MCP server with Pydantic validation.
    """

    immich_base_url: HttpUrl = Field(..., env="IMMICH_BASE_URL", description="Base URL of the Immich API")
    immich_api_key: str = Field(..., env="IMMICH_API_KEY", description="API key for authenticating with Immich")
    immich_timeout: int = Field(30, env="IMMICH_TIMEOUT", ge=5, le=120,
                               description="Timeout in seconds for HTTP requests to Immich API (default: 30)")
    immich_max_retries: int = Field(3, env="IMMICH_MAX_RETRIES", ge=0, le=5,
                                   description="Maximum number of retries for failed HTTP requests (default: 3)")

    @validator('immich_api_key')
    def validate_api_key(cls, value):
        """Validate that the API key is not empty and has reasonable length."""
        if not value or len(value) < 10:
            raise ValueError("API key must be at least 10 characters long")
        return value

    async def test_connection(self) -> bool:
        """
        Test connectivity to the Immich API.

        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            async with httpx.AsyncClient(
                base_url=self.immich_base_url,
                headers={"x-api-key": self.immich_api_key},
                timeout=self.immich_timeout
            ) as client:

                # Test a simple endpoint that should be available if the server is up
                response = await client.get("/server-info/ping")
                return response.status_code == 200

        except httpx.RequestError as e:
            logger.error(f"Connection test failed: {e}")
            return False

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_prefix = "IMMICH_"

def load_config() -> ImmichConfig:
    """
    Load and validate the configuration.

    Returns:
        ImmichConfig: Validated configuration instance

    Raises:
        ValidationError: If configuration validation fails
    """
    try:
        config = ImmichConfig()
        logger.info("Configuration loaded successfully")

        # Test connection during startup if possible (async context required)
        return config

    except ValidationError as e:
        error_msg = "Invalid configuration:\n" + "\n".join(
            [f"- {error['loc'][0]}: {error['msg']}" for error in e.errors()]
        )
        logger.error(error_msg)
        raise
