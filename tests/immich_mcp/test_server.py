from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock

from main import create_app


class TestAuth:
    """Test cases for API authentication."""

    def test_valid_token(self):
        """Test that a valid token is accepted."""
        with patch("main.load_config") as mock_load_config:
            mock_config = MagicMock()
            mock_config.auth_token = "test_token"
            mock_config.test_connection = AsyncMock(return_value=True)
            mock_load_config.return_value = mock_config
            app = create_app()
            with TestClient(app) as client:
                response = client.get(
                    "/", headers={"Authorization": "Bearer test_token"}
                )
                assert response.status_code == 200

    def test_invalid_token(self):
        """Test that an invalid token is rejected."""
        with patch("main.load_config") as mock_load_config:
            mock_config = MagicMock()
            mock_config.auth_token = "test_token"
            mock_config.test_connection = AsyncMock(return_value=True)
            mock_load_config.return_value = mock_config
            app = create_app()
            with TestClient(app) as client:
                response = client.get(
                    "/", headers={"Authorization": "Bearer invalid_token"}
                )
                assert response.status_code == 401
                assert response.json() == {"detail": "Invalid token"}

    def test_missing_token(self):
        """Test that a missing token is rejected."""
        with patch("main.load_config") as mock_load_config:
            mock_config = MagicMock()
            mock_config.auth_token = "test_token"
            mock_config.test_connection = AsyncMock(return_value=True)
            mock_load_config.return_value = mock_config
            app = create_app()
            with TestClient(app) as client:
                response = client.get("/")
                assert response.status_code == 403

    def test_invalid_scheme(self):
        """Test that an invalid authentication scheme is rejected."""
        with patch("main.load_config") as mock_load_config:
            mock_config = MagicMock()
            mock_config.auth_token = "test_token"
            mock_config.test_connection = AsyncMock(return_value=True)
            mock_load_config.return_value = mock_config
            app = create_app()
            with TestClient(app) as client:
                response = client.get(
                    "/", headers={"Authorization": "Basic test_token"}
                )
                assert response.status_code == 403
