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
        self.base_url = str(config.immich_base_url)
        if not self.base_url.endswith("/"):
            self.base_url += "/"

        self.headers = {
            "x-api-key": self.config.immich_api_key,
            "Accept": "application/json",
        }

    def _get_url(self, path: str) -> str:
        return urljoin(self.base_url, path)

    async def get_all_jobs_status(self) -> Dict[str, Any]:
        """
        Get the status of all jobs.

        Returns:
            Dict[str, Any]: A dictionary containing the status of all jobs.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"{self.config.immich_base_url}/api/jobs", headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def send_job_command(
        self, job_id: str, command: str, force: bool = False
    ) -> Dict[str, Any]:
        """
        Send a command to a job.

        Args:
            job_id: The ID of the job to send the command to.
            command: The command to send (e.g., 'start', 'stop').
            force: Whether to force the command.

        Returns:
            Dict[str, Any]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.put(
                f"{self.config.immich_base_url}/api/jobs/{job_id}",
                headers=self.headers,
                json={"command": command, "force": force},
            )
            response.raise_for_status()
            return response.json()

    async def run_asset_jobs(self, name: str, asset_ids: List[str]) -> None:
        """
        Run a job for a set of assets.

        Args:
            name: The name of the job to run.
            asset_ids: A list of asset IDs to run the job on.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                f"{self.config.immich_base_url}/api/assets/jobs",
                headers=self.headers,
                json={"name": name, "assetIds": asset_ids},
            )
            response.raise_for_status()

    async def get_asset(
        self, asset_id: str, key: Optional[str] = None, slug: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieve detailed information about a specific asset.

        Args:
            asset_id: The unique identifier of the asset to retrieve
            key: The key for the asset, used for shared links.
            slug: The slug for the asset, used for shared links.

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
            url = self._get_url(f"asset/{asset_id}")
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
            query: Search criteria dictionary. See Immich API for all possible options.

        Returns:
            Dict[str, Any]: Search results containing assets and total count

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("search/metadata")
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
            query: Smart search query dictionary. See Immich API for all possible options.

        Returns:
            Dict[str, Any]: AI-powered search results

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("search/smart")
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

        Args:
            name: The name of the person to search for.
            with_hidden: Whether to include hidden people in the results.

        Returns:
            List[Dict[str, Any]]: A list of people matching the search criteria.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"name": name}
            if with_hidden is not None:
                params["withHidden"] = with_hidden
            url = self._get_url("search/person")
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def search_places(self, name: str) -> List[Dict[str, Any]]:
        """
        Search for places and locations in the photo library.

        Args:
            name: The name of the place to search for.

        Returns:
            List[Dict[str, Any]]: A list of places matching the search criteria.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {"name": name}
            url = self._get_url("search/places")
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

        Args:
            type: The type of suggestion to get.
            country: The country to get suggestions for.
            include_null: Whether to include null values.
            make: The make of the camera to get suggestions for.
            model: The model of the camera to get suggestions for.
            state: The state to get suggestions for.

        Returns:
            List[str]: A list of search suggestions.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
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
            url = self._get_url("search/suggestions")
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

        Args:
            query: Search criteria dictionary. See Immich API for all possible options.

        Returns:
            List[Dict[str, Any]]: A list of random assets.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("search/random")
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

        Args:
            closest_asset_id: The asset ID to search for closest people from.
            closest_person_id: The person ID to search for closest people from.
            page: The page number for pagination.
            size: The number of people to return per page.
            with_hidden: Whether to include hidden people in the results.

        Returns:
            Dict[str, Any]: A dictionary containing a list of people and the total count.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
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
            url = self._get_url("people")
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
            Dict[str, Any]: Person object containing comprehensive information.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"people/{person_id}")
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
            person_id: The unique identifier of the person.

        Returns:
            Dict[str, Any]: Statistics for the person.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"people/{person_id}/statistics")
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
            person_id: The unique identifier of the person.

        Returns:
            bytes: The thumbnail image data.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"people/{person_id}/thumbnail")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.content

    async def get_all_albums(
        self, asset_id: Optional[str] = None, shared: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all albums from the Immich API.

        Args:
            asset_id: The asset ID to get the albums for.
            shared: Whether to get shared albums.

        Returns:
            List[Dict[str, Any]]: List of album objects.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {}
            if asset_id:
                params["assetId"] = asset_id
            if shared is not None:
                params["shared"] = shared
            url = self._get_url("albums")
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
            album_users: Optional list of users to share the album with.

        Returns:
            Dict[str, Any]: Created album object

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        payload = {"albumName": album_name, "description": description}
        if asset_ids:
            payload["assetIds"] = asset_ids
        if album_users:
            payload["albumUsers"] = album_users

        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("albums")
            response = await client.post(
                url,
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def get_album(
        self,
        album_id: str,
        key: Optional[str] = None,
        slug: Optional[str] = None,
        without_assets: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific album.

        Args:
            album_id: The unique identifier of the album.
            key: The key for the album, used for shared links.
            slug: The slug for the album, used for shared links.
            without_assets: Whether to exclude asset information from the response.

        Returns:
            Dict[str, Any]: Album object containing comprehensive information.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {}
            if key:
                params["key"] = key
            if slug:
                params["slug"] = slug
            if without_assets is not None:
                params["withoutAssets"] = without_assets
            url = self._get_url(f"albums/{album_id}")
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
            album_id: The unique identifier of the album to delete.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"albums/{album_id}")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def add_assets_to_album(
        self,
        album_id: str,
        asset_ids: List[str],
        key: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add assets to an existing album.

        Args:
            album_id: The unique identifier of the album.
            asset_ids: List of asset IDs to add to the album.
            key: The key for the album, used for shared links.
            slug: The slug for the album, used for shared links.

        Returns:
            Dict[str, Any]: Response containing success/failure information for each asset.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        payload = {"ids": asset_ids}
        params = {}
        if key:
            params["key"] = key
        if slug:
            params["slug"] = slug

        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"albums/{album_id}/assets")
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
            album_id: The unique identifier of the album.
            asset_ids: List of asset IDs to remove from the album.

        Returns:
            Dict[str, Any]: Response containing success/failure information.

        Raises:
            httpx.HTTPStatusError: If the API request fails
            httpx.RequestError: If there's a network connectivity issue
        """
        payload = {"ids": asset_ids}

        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"albums/{album_id}/assets")
            response = await client.request(
                "DELETE",
                url,
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()
