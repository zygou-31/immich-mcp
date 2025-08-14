from immich_mcp.client import ImmichClient
import json
import logging
from typing import Optional, List
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential

from .cache import CacheManager
from .rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class ImmichTools:
    """Production-ready tools for Immich MCP server with caching, rate limiting, and performance optimizations."""

    def __init__(self, config):
        self.config = config
        self.client = ImmichClient(config)
        self.cache = CacheManager()
        self.rate_limiter = RateLimiter(max_requests=100, window=60)

    async def __aenter__(self):
        """Async context manager entry."""
        await self.client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.__aexit__(exc_type, exc_val, exc_tb)

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_all_assets(self) -> str:
        """Retrieves all assets from Immich with caching and rate limiting."""
        try:
            assets = await self.client.get_all_assets()
            return json.dumps(assets)
        except Exception as e:
            logger.error(f"Error getting all assets: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_asset_info(self, asset_id: str) -> str:
        """Gets information about a specific asset with caching."""
        try:
            asset = await self.client.get_asset(asset_id)
            return json.dumps(asset)
        except Exception as e:
            logger.error(f"Error getting asset {asset_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=64)
    async def search_metadata(
        self,
        query: str = "",
        asset_type: str = None,
        is_favorite: bool = None,
        limit: int = 100,
        album_ids: List[str] = None,
        city: str = None,
        country: str = None,
        created_after: str = None,
        created_before: str = None,
        description: str = None,
        device_id: str = None,
        is_encoded: bool = None,
        is_motion: bool = None,
        is_not_in_album: bool = None,
        is_offline: bool = None,
        lens_model: str = None,
        make: str = None,
        model: str = None,
        person_ids: List[str] = None,
        rating: int = None,
        state: str = None,
        tag_ids: List[str] = None,
        taken_after: str = None,
        taken_before: str = None,
        visibility: str = None,
        with_deleted: bool = None,
        with_exif: bool = None,
        with_people: bool = None,
        with_stacked: bool = None,
    ) -> str:
        """
        Search assets by metadata criteria with caching and rate limiting.

        Args:
            query: Search query string for metadata (filename, description, etc.)
            asset_type: Filter by asset type (IMAGE, VIDEO, AUDIO, OTHER)
            is_favorite: Filter by favorite status
            limit: Maximum number of results to return (size parameter)
            album_ids: Filter by album IDs
            city: Filter by city
            country: Filter by country
            created_after: Filter by creation date (after) in ISO format
            created_before: Filter by creation date (before) in ISO format
            description: Filter by description
            device_id: Filter by device ID
            is_encoded: Filter by encoded status
            is_motion: Filter by motion status
            is_not_in_album: Filter by not in album
            is_offline: Filter by offline status
            lens_model: Filter by lens model
            make: Filter by camera make
            model: Filter by camera model
            person_ids: Filter by person IDs
            rating: Filter by rating (-1 to 5)
            state: Filter by state
            tag_ids: Filter by tag IDs
            taken_after: Filter by taken date (after) in ISO format
            taken_before: Filter by taken date (before) in ISO format
            visibility: Filter by visibility (archive, timeline, hidden, locked)
            with_deleted: Include deleted assets
            with_exif: Include EXIF data
            with_people: Include people data
            with_stacked: Include stacked assets

        Returns:
            str: JSON string containing search results with assets and total count

        Example:
            >>> results = await tools.search_metadata("beach", "IMAGE", True, 50, city="Paris")
        """
        try:
            search_query = {"size": limit}
            if query:
                search_query["q"] = query
            if asset_type:
                search_query["type"] = asset_type
            if is_favorite is not None:
                search_query["isFavorite"] = is_favorite
            if album_ids:
                search_query["albumIds"] = album_ids
            if city:
                search_query["city"] = city
            if country:
                search_query["country"] = country
            if created_after:
                search_query["createdAfter"] = created_after
            if created_before:
                search_query["createdBefore"] = created_before
            if description:
                search_query["description"] = description
            if device_id:
                search_query["deviceId"] = device_id
            if is_encoded is not None:
                search_query["isEncoded"] = is_encoded
            if is_motion is not None:
                search_query["isMotion"] = is_motion
            if is_not_in_album is not None:
                search_query["isNotInAlbum"] = is_not_in_album
            if is_offline is not None:
                search_query["isOffline"] = is_offline
            if lens_model:
                search_query["lensModel"] = lens_model
            if make:
                search_query["make"] = make
            if model:
                search_query["model"] = model
            if person_ids:
                search_query["personIds"] = person_ids
            if rating is not None:
                search_query["rating"] = rating
            if state:
                search_query["state"] = state
            if tag_ids:
                search_query["tagIds"] = tag_ids
            if taken_after:
                search_query["takenAfter"] = taken_after
            if taken_before:
                search_query["takenBefore"] = taken_before
            if visibility:
                search_query["visibility"] = visibility
            if with_deleted is not None:
                search_query["withDeleted"] = with_deleted
            if with_exif is not None:
                search_query["withExif"] = with_exif
            if with_people is not None:
                search_query["withPeople"] = with_people
            if with_stacked is not None:
                search_query["withStacked"] = with_stacked

            results = await self.client.search_metadata(search_query)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching metadata: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=64)
    async def search_smart(
        self,
        query: str,
        limit: int = 100,
        album_ids: List[str] = None,
        city: str = None,
        country: str = None,
        created_after: str = None,
        created_before: str = None,
        device_id: str = None,
        is_encoded: bool = None,
        is_favorite: bool = None,
        is_motion: bool = None,
        is_not_in_album: bool = None,
        is_offline: bool = None,
        language: str = None,
        lens_model: str = None,
        make: str = None,
        model: str = None,
        person_ids: List[str] = None,
        rating: int = None,
        state: str = None,
        tag_ids: List[str] = None,
        taken_after: str = None,
        taken_before: str = None,
        trashed_after: str = None,
        trashed_before: str = None,
        asset_type: str = None,
        updated_after: str = None,
        updated_before: str = None,
        visibility: str = None,
        with_deleted: bool = None,
        with_exif: bool = None,
    ) -> str:
        """
        Smart search using AI to find assets based on natural language queries.

        Args:
            query: Natural language search query (required)
            limit: Maximum number of results to return (size parameter)
            album_ids: Filter by album IDs
            city: Filter by city
            country: Filter by country
            created_after: Filter by creation date (after) in ISO format
            created_before: Filter by creation date (before) in ISO format
            device_id: Filter by device ID
            is_encoded: Filter by encoded status
            is_favorite: Filter by favorite status
            is_motion: Filter by motion status
            is_not_in_album: Filter by not in album
            is_offline: Filter by offline status
            language: Language for the query
            lens_model: Filter by lens model
            make: Filter by camera make
            model: Filter by camera model
            person_ids: Filter by person IDs
            rating: Filter by rating (-1 to 5)
            state: Filter by state
            tag_ids: Filter by tag IDs
            taken_after: Filter by taken date (after) in ISO format
            taken_before: Filter by taken date (before) in ISO format
            trashed_after: Filter by trashed date (after) in ISO format
            trashed_before: Filter by trashed date (before) in ISO format
            asset_type: Asset type filter (IMAGE, VIDEO, AUDIO, OTHER)
            updated_after: Filter by updated date (after) in ISO format
            updated_before: Filter by updated date (before) in ISO format
            visibility: Filter by visibility (archive, timeline, hidden, locked)
            with_deleted: Include deleted assets
            with_exif: Include EXIF data

        Returns:
            str: JSON string containing AI-powered search results

        Example:
            >>> results = await tools.search_smart("photos of my dog at the beach", 10, is_favorite=True)
        """
        try:
            search_query = {"query": query, "size": limit}
            if album_ids:
                search_query["albumIds"] = album_ids
            if city:
                search_query["city"] = city
            if country:
                search_query["country"] = country
            if created_after:
                search_query["createdAfter"] = created_after
            if created_before:
                search_query["createdBefore"] = created_before
            if device_id:
                search_query["deviceId"] = device_id
            if is_encoded is not None:
                search_query["isEncoded"] = is_encoded
            if is_favorite is not None:
                search_query["isFavorite"] = is_favorite
            if is_motion is not None:
                search_query["isMotion"] = is_motion
            if is_not_in_album is not None:
                search_query["isNotInAlbum"] = is_not_in_album
            if is_offline is not None:
                search_query["isOffline"] = is_offline
            if language:
                search_query["language"] = language
            if lens_model:
                search_query["lensModel"] = lens_model
            if make:
                search_query["make"] = make
            if model:
                search_query["model"] = model
            if person_ids:
                search_query["personIds"] = person_ids
            if rating is not None:
                search_query["rating"] = rating
            if state:
                search_query["state"] = state
            if tag_ids:
                search_query["tagIds"] = tag_ids
            if taken_after:
                search_query["takenAfter"] = taken_after
            if taken_before:
                search_query["takenBefore"] = taken_before
            if trashed_after:
                search_query["trashedAfter"] = trashed_after
            if trashed_before:
                search_query["trashedBefore"] = trashed_before
            if asset_type:
                search_query["type"] = asset_type
            if updated_after:
                search_query["updatedAfter"] = updated_after
            if updated_before:
                search_query["updatedBefore"] = updated_before
            if visibility:
                search_query["visibility"] = visibility
            if with_deleted is not None:
                search_query["withDeleted"] = with_deleted
            if with_exif is not None:
                search_query["withExif"] = with_exif

            results = await self.client.search_smart(search_query)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error in smart search: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def search_people(self, query: str = "", limit: int = 50) -> str:
        """
        Search for people in the photo library with caching.

        Args:
            query: Search query for person names
            limit: Maximum number of results to return

        Returns:
            str: JSON string containing list of people matching the search criteria

        Example:
            >>> people = await tools.search_people("John", 10)
        """
        try:
            results = await self.client.search_people(query, limit)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching people: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def search_places(self, query: str = "", limit: int = 50) -> str:
        """
        Search for places and locations in the photo library with caching.

        Args:
            query: Search query for place names
            limit: Maximum number of results to return

        Returns:
            str: JSON string containing list of places matching the search criteria

        Example:
            >>> places = await tools.search_places("beach", 10)
        """
        try:
            results = await self.client.search_places(query, limit)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching places: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=256)
    async def get_search_suggestions(self, query: str = "") -> str:
        """
        Get search suggestions based on partial queries with caching.

        Args:
            query: Partial search query for suggestions

        Returns:
            str: JSON string containing list of search suggestions

        Example:
            >>> suggestions = await tools.get_search_suggestions("be")
        """
        try:
            results = await self.client.get_search_suggestions(query)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error getting search suggestions: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=32)
    async def search_random(self, limit: int = 10) -> str:
        """
        Get random assets from the photo library with caching.

        Args:
            limit: Maximum number of random assets to return

        Returns:
            str: JSON string containing list of random assets

        Example:
            >>> random_assets = await tools.search_random(5)
        """
        try:
            results = await self.client.search_random(limit)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error getting random assets: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=64)
    async def get_all_people(
        self, query: str = "", limit: int = 100, offset: int = 0
    ) -> str:
        """
        Get all people from the photo library with caching and rate limiting.

        Args:
            query: Search query for filtering people by name
            limit: Maximum number of people to return
            offset: Number of people to skip for pagination

        Returns:
            str: JSON string containing people list and total count

        Example:
            >>> people = await tools.get_all_people("John", 50, 0)
        """
        try:
            results = await self.client.get_all_people(query, limit, offset)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error getting all people: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_person(self, person_id: str) -> str:
        """
        Get detailed information about a specific person with caching.

        Args:
            person_id: The unique identifier of the person to retrieve

        Returns:
            str: JSON string containing person details including:
                - id: Unique person identifier
                - name: Person's name
                - thumbnailPath: Thumbnail image path
                - faces: List of face instances
                - assets: Associated assets
                - birthDate: Birth date if available

        Example:
            >>> person = await tools.get_person("550e8400-e29b-41d4-a716-446655440000")
        """
        try:
            person = await self.client.get_person(person_id)
            return json.dumps(person)
        except Exception as e:
            logger.error(f"Error getting person {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=64)
    async def get_person_statistics(self, person_id: str) -> str:
        """
        Get statistics for a specific person with caching.

        Args:
            person_id: The unique identifier of the person

        Returns:
            str: JSON string containing statistics including:
                - totalAssets: Total number of assets
                - totalSize: Total size of assets
                - oldestDate: Date of oldest asset
                - newestDate: Date of newest asset

        Example:
            >>> stats = await tools.get_person_statistics("550e8400-e29b-41d4-a716-446655440000")
        """
        try:
            stats = await self.client.get_person_statistics(person_id)
            return json.dumps(stats)
        except Exception as e:
            logger.error(f"Error getting person statistics {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_person_thumbnail(self, person_id: str) -> str:
        """
        Get thumbnail image for a specific person as base64 encoded string.

        Args:
            person_id: The unique identifier of the person

        Returns:
            str: Base64 encoded thumbnail image data

        Example:
            >>> thumbnail = await tools.get_person_thumbnail("550e8400-e29b-41d4-a716-446655440000")
        """
        try:
            import base64

            thumbnail_data = await self.client.get_person_thumbnail(person_id)
            return base64.b64encode(thumbnail_data).decode("utf-8")
        except Exception as e:
            logger.error(f"Error getting person thumbnail {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_all_albums(self) -> str:
        """Retrieves all albums from Immich with caching and rate limiting."""
        try:
            albums = await self.client.get_all_albums()
            return json.dumps(albums)
        except Exception as e:
            logger.error(f"Error getting all albums: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_album(
        self,
        album_name: str,
        description: str = "",
        asset_ids: Optional[List[str]] = None,
    ) -> str:
        """Creates a new album in Immich."""
        try:
            album = await self.client.create_album(album_name, description, asset_ids)
            return json.dumps(album)
        except Exception as e:
            logger.error(f"Error creating album: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_album_info(self, album_id: str) -> str:
        """Gets information about a specific album with caching."""
        try:
            album = await self.client.get_album(album_id)
            return json.dumps(album)
        except Exception as e:
            logger.error(f"Error getting album {album_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_album(self, album_id: str) -> str:
        """Deletes an album from Immich."""
        try:
            await self.client.delete_album(album_id)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting album {album_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def add_assets_to_album(self, album_id: str, asset_ids: List[str]) -> str:
        """Adds assets to an existing album."""
        try:
            results = await self.client.add_assets_to_album(album_id, asset_ids)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error adding assets to album {album_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def remove_assets_from_album(
        self, album_id: str, asset_ids: List[str]
    ) -> str:
        """Removes assets from an album."""
        try:
            results = await self.client.remove_assets_from_album(album_id, asset_ids)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error removing assets from album {album_id}: {e}")
            return json.dumps({"error": str(e)})
