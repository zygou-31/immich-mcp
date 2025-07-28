"""
Immich API client for interacting with the Immich photo management server.

This module provides an asynchronous client for the Immich API, handling
authentication, request formatting, and response parsing for various
photo management operations.
"""

import httpx
from typing import Optional, Dict, Any, List
from immich_mcp.config import ImmichConfig


class ImmichClient:
    """
    Asynchronous client for interacting with the Immich API.
    
    This client handles all HTTP communications with the Immich server,
    including authentication via API key and standard request/response formatting.
    
    Attributes:
        config: Configuration object containing server URL and API credentials
        headers: HTTP headers including authentication token
    """
    
    def __init__(self, config: ImmichConfig):
        """
        Initialize the Immich API client.
        
        Args:
            config: Configuration object containing server URL and API key
        """
        self.config = config
        self.headers = {
            "x-api-key": self.config.immich_api_key,
            "Accept": "application/json"
        }

    async def get_all_assets(self) -> List[Dict[str, Any]]:
        """
        Retrieve all assets from the Immich API.
        
        This method fetches all photos and videos from your Immich library,
        returning comprehensive metadata for each asset.
        
        Returns:
            List[Dict[str, Any]]: List of asset objects containing metadata like:
                - id: Unique asset identifier
                - originalFileName: Original filename
                - fileCreatedAt: Creation timestamp
                - type: Asset type (IMAGE/VIDEO)
                - thumbhash: Thumbnail hash
                - etc.
                
        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
            
        Example:
            >>> client = ImmichClient(config)
            >>> assets = await client.get_all_assets()
            >>> print(f"Found {len(assets)} assets")
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.config.immich_base_url}/api/assets",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def get_asset(self, asset_id: str) -> Dict[str, Any]:
        """
        Retrieve detailed information about a specific asset.
        
        Args:
            asset_id: The unique identifier of the asset to retrieve
            
        Returns:
            Dict[str, Any]: Asset object containing comprehensive metadata including:
                - id: Unique asset identifier
                - originalFileName: Original filename
                - fileCreatedAt: Creation timestamp
                - type: Asset type (IMAGE/VIDEO)
                - exifInfo: EXIF metadata
                - smartInfo: AI-generated tags
                - people: Recognized faces
                - etc.
                
        Raises:
            httpx.HTTPStatusError: If the API request fails (e.g., asset not found)
            httpx.RequestError: If there's a network connectivity issue
            
        Example:
            >>> client = ImmichClient(config)
            >>> asset = await client.get_asset("550e8400-e29b-41d4-a716-446655440000")
            >>> print(asset["originalFileName"])
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.config.immich_base_url}/api/assets/{asset_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

