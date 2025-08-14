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
            "Accept": "application/json",
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
                f"{self.config.immich_base_url}/api/assets", headers=self.headers
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
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def search_metadata(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search assets by metadata criteria.

        Args:
            query: Search criteria including:
                - albumIds: Filter by album IDs
                - checksum: Filter by checksum
                - city: Filter by city
                - country: Filter by country
                - createdAfter: Filter by creation date (after)
                - createdBefore: Filter by creation date (before)
                - description: Filter by description
                - deviceAssetId: Filter by device asset ID
                - deviceId: Filter by device ID
                - encodedVideoPath: Filter by encoded video path
                - id: Filter by asset ID
                - isEncoded: Filter by encoded status
                - isFavorite: Filter by favorite status
                - isMotion: Filter by motion status
                - isNotInAlbum: Filter by not in album
                - isOffline: Filter by offline status
                - lensModel: Filter by lens model
                - libraryId: Filter by library ID
                - make: Filter by camera make
                - model: Filter by camera model
                - order: Sort order (asc/desc)
                - originalFileName: Filter by original file name
                - originalPath: Filter by original path
                - page: Page number for pagination
                - personIds: Filter by person IDs
                - previewPath: Filter by preview path
                - q: Search query string
                - rating: Filter by rating (-1 to 5)
                - size: Number of items per page (1-1000)
                - state: Filter by state
                - tagIds: Filter by tag IDs
                - takenAfter: Filter by taken date (after)
                - takenBefore: Filter by taken date (before)
                - thumbnailPath: Filter by thumbnail path
                - trashedAfter: Filter by trashed date (after)
                - trashedBefore: Filter by trashed date (before)
                - type: Asset type (IMAGE, VIDEO, AUDIO, OTHER)
                - updatedAfter: Filter by updated date (after)
                - updatedBefore: Filter by updated date (before)
                - visibility: Filter by visibility (archive, timeline, hidden, locked)
                - withDeleted: Include deleted assets
                - withExif: Include EXIF data
                - withPeople: Include people data
                - withStacked: Include stacked assets

        Returns:
            Dict[str, Any]: Search results containing assets and total count

        Example:
            >>> client = ImmichClient(config)
            >>> results = await client.search_metadata({
            ...     "q": "beach",
            ...     "type": "IMAGE",
            ...     "isFavorite": True
            ... })
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.config.immich_base_url}/api/search/metadata",
                headers=self.headers,
                json=query,
            )
            response.raise_for_status()
            return response.json()

    async def search_smart(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Smart search using AI to find assets based on natural language queries.

        Args:
            query: Smart search query including:
                - query: Natural language search query (required)
                - albumIds: Filter by album IDs
                - city: Filter by city
                - country: Filter by country
                - createdAfter: Filter by creation date (after)
                - createdBefore: Filter by creation date (before)
                - deviceId: Filter by device ID
                - isEncoded: Filter by encoded status
                - isFavorite: Filter by favorite status
                - isMotion: Filter by motion status
                - isNotInAlbum: Filter by not in album
                - isOffline: Filter by offline status
                - language: Language for the query
                - lensModel: Filter by lens model
                - libraryId: Filter by library ID
                - make: Filter by camera make
                - model: Filter by camera model
                - page: Page number for pagination
                - personIds: Filter by person IDs
                - rating: Filter by rating (-1 to 5)
                - size: Number of items per page (1-1000)
                - state: Filter by state
                - tagIds: Filter by tag IDs
                - takenAfter: Filter by taken date (after)
                - takenBefore: Filter by taken date (before)
                - trashedAfter: Filter by trashed date (after)
                - trashedBefore: Filter by trashed date (before)
                - type: Asset type filter (IMAGE, VIDEO, AUDIO, OTHER)
                - updatedAfter: Filter by updated date (after)
                - updatedBefore: Filter by updated date (before)
                - visibility: Filter by visibility (archive, timeline, hidden, locked)
                - withDeleted: Include deleted assets
                - withExif: Include EXIF data

        Returns:
            Dict[str, Any]: AI-powered search results

        Example:
            >>> client = ImmichClient(config)
            >>> results = await client.search_smart({
            ...     "query": "photos of my dog at the beach",
            ...     "limit": 10
            ... })
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.config.immich_base_url}/api/search/smart",
                headers=self.headers,
                json=query,
            )
            response.raise_for_status()
            return response.json()

    async def search_people(
        self, query: str = "", limit: int = 100, with_hidden: bool = None
    ) -> List[Dict[str, Any]]:
        """
        Search for people in the photo library.

        Args:
            query: Search query for person names
            limit: Maximum number of results to return
            with_hidden: Include hidden people in the results

        Returns:
            List[Dict[str, Any]]: List of people matching the search criteria

        Example:
            >>> client = ImmichClient(config)
            >>> people = await client.search_people("John", limit=10)
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"name": query, "limit": limit}
            if with_hidden is not None:
                params["withHidden"] = with_hidden
            response = await client.get(
                f"{self.config.immich_base_url}/api/search/person",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def search_places(
        self, query: str = "", limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search for places and locations in the photo library.

        Args:
            query: Search query for place names
            limit: Maximum number of results to return

        Returns:
            List[Dict[str, Any]]: List of places matching the search criteria

        Example:
            >>> client = ImmichClient(config)
            >>> places = await client.search_places("beach", limit=10)
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"q": query, "limit": limit}
            response = await client.get(
                f"{self.config.immich_base_url}/api/search/places",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def get_search_suggestions(self, query: str = "") -> List[str]:
        """
        Get search suggestions based on partial queries.

        Args:
            query: Partial search query for suggestions

        Returns:
            List[str]: List of search suggestions

        Example:
            >>> client = ImmichClient(config)
            >>> suggestions = await client.get_search_suggestions("be")
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"q": query}
            response = await client.get(
                f"{self.config.immich_base_url}/api/search/suggestions",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def search_random(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get random assets from the photo library.

        Args:
            limit: Maximum number of random assets to return

        Returns:
            List[Dict[str, Any]]: List of random assets

        Example:
            >>> client = ImmichClient(config)
            >>> random_assets = await client.search_random(limit=5)
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.config.immich_base_url}/api/search/random",
                headers=self.headers,
                json={"limit": limit},
            )
            response.raise_for_status()
            return response.json()

    async def get_all_people(
        self, query: str = "", limit: int = 100, offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get all people from the photo library with optional filtering.

        Args:
            query: Search query for filtering people by name
            limit: Maximum number of people to return
            offset: Number of people to skip for pagination

        Returns:
            Dict[str, Any]: Response containing people list and total count

        Example:
            >>> client = ImmichClient(config)
            >>> people = await client.get_all_people("John", 50, 0)
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"q": query, "limit": limit, "offset": offset}
            response = await client.get(
                f"{self.config.immich_base_url}/api/people",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def get_person(self, person_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific person.

        Args:
            person_id: The unique identifier of the person to retrieve

        Returns:
            Dict[str, Any]: Person object containing comprehensive information including:
                - id: Unique person identifier
                - name: Person's name
                - thumbnailPath: Thumbnail image path
                - faces: List of face instances
                - assets: Associated assets
                - birthDate: Birth date if available
                - etc.

        Raises:
            httpx.HTTPStatusError: If the API request fails (e.g., person not found)
            httpx.RequestError: If there's a network connectivity issue

        Example:
            >>> client = ImmichClient(config)
            >>> person = await client.get_person("550e8400-e29b-41d4-a716-446655440000")
            >>> print(person["name"])
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.config.immich_base_url}/api/people/{person_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_person_statistics(self, person_id: str) -> Dict[str, Any]:
        """
        Get statistics for a specific person.

        Args:
            person_id: The unique identifier of the person

        Returns:
            Dict[str, Any]: Statistics including:
                - totalAssets: Total number of assets
                - totalSize: Total size of assets
                - oldestDate: Date of oldest asset
                - newestDate: Date of newest asset
                - etc.

        Example:
            >>> client = ImmichClient(config)
            >>> stats = await client.get_person_statistics("550e8400-e29b-41d4-a716-446655440000")
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.config.immich_base_url}/api/people/{person_id}/statistics",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_person_thumbnail(self, person_id: str) -> bytes:
        """
        Get thumbnail image for a specific person.

        Args:
            person_id: The unique identifier of the person

        Returns:
            bytes: Thumbnail image data

        Example:
            >>> client = ImmichClient(config)
            >>> thumbnail = await client.get_person_thumbnail("550e8400-e29b-41d4-a716-446655440000")
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.config.immich_base_url}/api/people/{person_id}/thumbnail",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.content

    async def get_all_albums(self) -> List[Dict[str, Any]]:
        """
        Retrieve all albums from the Immich API.

        Returns:
            List[Dict[str, Any]]: List of album objects containing metadata like:
                - id: Unique album identifier
                - albumName: Album name
                - description: Album description
                - albumThumbnailAssetId: Thumbnail asset ID
                - shared: Whether album is shared
                - assetCount: Number of assets in album
                - createdAt: Creation timestamp
                - updatedAt: Last update timestamp

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue

        Example:
            >>> client = ImmichClient(config)
            >>> albums = await client.get_all_albums()
            >>> print(f"Found {len(albums)} albums")
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.config.immich_base_url}/api/albums", headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def create_album(
        self,
        album_name: str,
        description: str = "",
        asset_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new album in Immich.

        Args:
            album_name: Name of the album to create
            description: Optional description for the album
            asset_ids: Optional list of asset IDs to add to the album

        Returns:
            Dict[str, Any]: Created album object

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue

        Example:
            >>> client = ImmichClient(config)
            >>> album = await client.create_album("Vacation 2024", "Summer vacation photos")
        """
        payload = {"albumName": album_name, "description": description}
        if asset_ids:
            payload["assetIds"] = asset_ids

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.config.immich_base_url}/api/albums",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def get_album(self, album_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific album.

        Args:
            album_id: The unique identifier of the album

        Returns:
            Dict[str, Any]: Album object containing comprehensive information including:
                - id: Unique album identifier
                - albumName: Album name
                - description: Album description
                - assets: List of assets in the album
                - albumThumbnailAssetId: Thumbnail asset ID
                - shared: Whether album is shared
                - sharedUsers: List of users album is shared with
                - assetCount: Number of assets
                - createdAt: Creation timestamp
                - updatedAt: Last update timestamp

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue

        Example:
            >>> client = ImmichClient(config)
            >>> album = await client.get_album("550e8400-e29b-41d4-a716-446655440000")
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.config.immich_base_url}/api/albums/{album_id}",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def delete_album(self, album_id: str) -> None:
        """
        Delete an album from Immich.

        Args:
            album_id: The unique identifier of the album to delete

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue

        Example:
            >>> client = ImmichClient(config)
            >>> await client.delete_album("550e8400-e29b-41d4-a716-446655440000")
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.delete(
                f"{self.config.immich_base_url}/api/albums/{album_id}",
                headers=self.headers,
            )
            response.raise_for_status()

    async def add_assets_to_album(
        self, album_id: str, asset_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Add assets to an existing album.

        Args:
            album_id: The unique identifier of the album
            asset_ids: List of asset IDs to add to the album

        Returns:
            Dict[str, Any]: Response containing success/failure information for each asset

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue

        Example:
            >>> client = ImmichClient(config)
            >>> results = await client.add_assets_to_album("album-id", ["asset1", "asset2"])
        """
        payload = {"ids": asset_ids}

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.put(
                f"{self.config.immich_base_url}/api/albums/{album_id}/assets",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def remove_assets_from_album(
        self, album_id: str, asset_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Remove assets from an album.

        Args:
            album_id: The unique identifier of the album
            asset_ids: List of asset IDs to remove from the album

        Returns:
            Dict[str, Any]: Response containing success/failure information

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue

        Example:
            >>> client = ImmichClient(config)
            >>> results = await client.remove_assets_from_album("album-id", ["asset1", "asset2"])
        """
        payload = {"ids": asset_ids}

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.request(
                "DELETE",
                f"{self.config.immich_base_url}/api/albums/{album_id}/assets",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
