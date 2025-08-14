import pytest
from pydantic import ValidationError
from immich_mcp.config import ImmichConfig


def test_immich_config_api_key_required():
    with pytest.raises(ValidationError):
        ImmichConfig(immich_base_url="http://immich.test/api", immich_api_key=None)


def test_immich_config_api_endpoint_required():
    with pytest.raises(ValidationError):
        ImmichConfig(immich_api_key="test_key")


def test_immich_config_valid_from_args():
    config = ImmichConfig(
        immich_api_key="test_key_args", immich_base_url="http://immich.test/api/args"
    )
    assert config.immich_api_key == "test_key_args"
    assert str(config.immich_base_url) == "http://immich.test/api/args"
