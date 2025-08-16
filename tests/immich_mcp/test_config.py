import pytest
import os
from unittest.mock import patch
from pydantic import ValidationError

# Set TESTING environment variable before importing config module
os.environ["TESTING"] = "true"

from immich_mcp.config import ImmichConfig


class TestConfig:
    """Test cases for the ImmichConfig class."""

    def teardown_method(self):
        """Clean up test environment."""
        # Remove TESTING environment variable
        if "TESTING" in os.environ:
            del os.environ["TESTING"]

    def test_missing_auth_token(self):
        """Test that an error is raised if the auth token is missing."""
        with patch.object(ImmichConfig, "model_config", {"env_file": None}):
            if "IMMICH_API_KEY" in os.environ:
                del os.environ["IMMICH_API_KEY"]
            with pytest.raises(ValidationError) as exc_info:
                ImmichConfig(
                    immich_base_url="http://test.com/api",
                    immich_api_key="test_api_key",
                )
            assert "An auth token must be configured" in str(exc_info.value)

    def test_missing_api_key(self):
        """Test that an error is raised if the Immich API key is missing."""
        with patch.object(ImmichConfig, "model_config", {"env_file": None}):
            if "IMMICH_API_KEY" in os.environ:
                del os.environ["IMMICH_API_KEY"]
            with pytest.raises(ValidationError) as exc_info:
                ImmichConfig(
                    immich_base_url="http://test.com/api",
                    auth_token="test_auth_token",
                )
            assert "An Immich API key must be configured" in str(exc_info.value)

    def test_load_auth_token_from_file(self, tmp_path):
        """Test that the auth token can be loaded from a file."""
        token_file = tmp_path / "auth_token.txt"
        token_file.write_text("token_from_file")
        config = ImmichConfig(
            immich_base_url="http://test.com/api",
            immich_api_key="test_api_key",
            auth_token_file=str(token_file),
        )
        assert config.auth_token == "token_from_file"

    def test_load_api_key_from_file(self, tmp_path):
        """Test that the Immich API key can be loaded from a file."""
        api_key_file = tmp_path / "api_key.txt"
        api_key_file.write_text("api_key_from_file")
        config = ImmichConfig(
            immich_base_url="http://test.com/api",
            auth_token="test_auth_token",
            immich_api_key_file=str(api_key_file),
        )
        assert config.immich_api_key == "api_key_from_file"

    def test_auth_token_file_not_found(self):
        """Test that an error is raised if the auth token file is not found."""
        with patch.object(ImmichConfig, "model_config", {"env_file": None}):
            if "IMMICH_API_KEY" in os.environ:
                del os.environ["IMMICH_API_KEY"]
            with pytest.raises(ValidationError) as exc_info:
                ImmichConfig(
                    immich_base_url="http://test.com/api",
                    immich_api_key="test_api_key",
                    auth_token_file="non_existent_file.txt",
                )
            assert "Auth token file not found" in str(exc_info.value)

    def test_api_key_file_not_found(self):
        """Test that an error is raised if the API key file is not found."""
        with patch.object(ImmichConfig, "model_config", {"env_file": None}):
            if "IMMICH_API_KEY" in os.environ:
                del os.environ["IMMICH_API_KEY"]
            with pytest.raises(ValidationError) as exc_info:
                ImmichConfig(
                    immich_base_url="http://test.com/api",
                    auth_token="test_auth_token",
                    immich_api_key_file="non_existent_file.txt",
                )
            assert "Immich API key file not found" in str(exc_info.value)

    def test_valid_config(self):
        """Test that a valid config can be created."""
        with patch.object(ImmichConfig, "model_config", {"env_file": None}):
            config = ImmichConfig(
                immich_base_url="http://test.com/api",
                immich_api_key="test_api_key",
                auth_token="test_auth_token",
            )
            assert str(config.immich_base_url) == "http://test.com/api"
            assert config.immich_api_key == "test_api_key"
            assert config.auth_token == "test_auth_token"
