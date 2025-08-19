"""
Immich API client for interacting with the Immich photo management server.

This module provides an asynchronous client for the Immich API, handling
authentication, request formatting, and response parsing for various
photo management operations.
"""

import httpx
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin
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

    async def get_asset(self, asset_id: str, key: Optional[str] = None, slug: Optional[str] = None) -> Dict[str, Any]:
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
            params = {}
            if key:
                params["key"] = key
            if slug:
                params["slug"] = slug
            url = urljoin(str(self.config.immich_base_url), f"api/assets/{asset_id}")
            response = await client.get(
                url,
                headers=self.headers,
                params=params if params else None,
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
            url = urljoin(str(self.config.immich_base_url), "api/search/metadata")
            response = await client.post(
                url,
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
            url = urljoin(str(self.config.immich_base_url), "api/search/smart")
            response = await client.post(
                url,
                headers=self.headers,
                json=query,
            )
            response.raise_for_status()
            return response.json()

    async def search_people(
        self, name: str, with_hidden: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for people in the photo library.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"name": name}
            if with_hidden is not None:
                params["withHidden"] = with_hidden
            url = urljoin(str(self.config.immich_base_url), "api/search/person")
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def search_places(
        self, name: str
    ) -> List[Dict[str, Any]]:
        """
        Search for places and locations in the photo library.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"name": name}
            url = urljoin(str(self.config.immich_base_url), "api/search/places")
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def get_search_suggestions(
        self,
        type: str,
        country: Optional[str] = None,
        include_null: Optional[bool] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        state: Optional[str] = None,
    ) -> List[str]:
        """
        Get search suggestions based on partial queries.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"type": type}
            if country is not None:
                params["country"] = country
            if include_null is not None:
                params["includeNull"] = include_null
            if make is not None:
                params["make"] = make
            if model is not None:
                params["model"] = model
            if state is not None:
                params["state"] = state
            url = urljoin(str(self.config.immich_base_url), "api/search/suggestions")
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def search_random(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get random assets from the photo library.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = urljoin(str(self.config.immich_base_url), "api/search/random")
            response = await client.post(
                url,
                headers=self.headers,
                json=query,
            )
            response.raise_for_status()
            return response.json()

    async def get_all_people(
        self,
        closest_asset_id: Optional[str] = None,
        closest_person_id: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        with_hidden: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Get all people from the photo library with optional filtering.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {}
            if closest_asset_id is not None:
                params["closestAssetId"] = closest_asset_id
            if closest_person_id is not None:
                params["closestPersonId"] = closest_person_id
            if page is not None:
                params["page"] = page
            if size is not None:
                params["size"] = size
            if with_hidden is not None:
                params["withHidden"] = with_hidden
            url = urljoin(str(self.config.immich_base_url), "api/people")
            response = await client.get(
                url,
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
            url = urljoin(str(self.config.immich_base_url), f"api/people/{person_id}")
            response = await client.get(
                url,
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
            url = urljoin(
                str(self.config.immich_base_url), f"api/people/{person_id}/statistics"
            )
            response = await client.get(
                url,
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
            url = urljoin(
                str(self.config.immich_base_url), f"api/people/{person_id}/thumbnail"
            )
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.content

    async def get_all_albums(self, asset_id: Optional[str] = None, shared: Optional[bool] = None) -> List[Dict[str, Any]]:
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
            params = {}
            if asset_id:
                params["assetId"] = asset_id
            if shared is not None:
                params["shared"] = shared
            url = urljoin(str(self.config.immich_base_url), "api/albums")
            response = await client.get(
                url, headers=self.headers, params=params if params else None
            )
            response.raise_for_status()
            return response.json()

    async def create_album(
        self,
        album_name: str,
        description: str = "",
        asset_ids: Optional[List[str]] = None,
        album_users: Optional[List[Dict[str, str]]] = None,
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
        if album_users:
            payload["albumUsers"] = album_users

        async with httpx.AsyncClient(timeout=10) as client:
            url = urljoin(str(self.config.immich_base_url), "api/albums")
            response = await client.post(
                url,
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def get_album(self, album_id: str, key: Optional[str] = None, slug: Optional[str] = None, without_assets: Optional[bool] = None) -> Dict[str, Any]:
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
            params = {}
            if key:
                params["key"] = key
            if slug:
                params["slug"] = slug
            if without_assets is not None:
                params["withoutAssets"] = without_assets
            url = urljoin(str(self.config.immich_base_url), f"api/albums/{album_id}")
            response = await client.get(
                url,
                headers=self.headers,
                params=params if params else None,
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
            url = urljoin(str(self.config.immich_base_url), f"api/albums/{album_id}")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def add_assets_to_album(
        self, album_id: str, asset_ids: List[str], key: Optional[str] = None, slug: Optional[str] = None
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
        params = {}
        if key:
            params["key"] = key
        if slug:
            params["slug"] = slug

        async with httpx.AsyncClient(timeout=10) as client:
            url = urljoin(str(self.config.immich_base_url), f"api/albums/{album_id}/assets")
            response = await client.put(
                url,
                headers=self.headers,
                json=payload,
                params=params if params else None,
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
            url = urljoin(str(self.config.immich_base_url), f"api/albums/{album_id}/assets")
            response = await client.request(
                "DELETE",
                url,
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
