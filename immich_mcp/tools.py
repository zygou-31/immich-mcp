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
        album_ids: Optional[List[str]] = None,
        checksum: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        description: Optional[str] = None,
        device_asset_id: Optional[str] = None,
        device_id: Optional[str] = None,
        encoded_video_path: Optional[str] = None,
        asset_id: Optional[str] = None,
        is_encoded: Optional[bool] = None,
        is_favorite: Optional[bool] = None,
        is_motion: Optional[bool] = None,
        is_not_in_album: Optional[bool] = None,
        is_offline: Optional[bool] = None,
        lens_model: Optional[str] = None,
        library_id: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        order: Optional[str] = None,
        original_file_name: Optional[str] = None,
        original_path: Optional[str] = None,
        page: Optional[int] = None,
        person_ids: Optional[List[str]] = None,
        preview_path: Optional[str] = None,
        rating: Optional[int] = None,
        size: Optional[int] = None,
        state: Optional[str] = None,
        tag_ids: Optional[List[str]] = None,
        taken_after: Optional[str] = None,
        taken_before: Optional[str] = None,
        thumbnail_path: Optional[str] = None,
        trashed_after: Optional[str] = None,
        trashed_before: Optional[str] = None,
        asset_type: Optional[str] = None,
        updated_after: Optional[str] = None,
        updated_before: Optional[str] = None,
        visibility: Optional[str] = None,
        with_deleted: Optional[bool] = None,
        with_exif: Optional[bool] = None,
        with_people: Optional[bool] = None,
        with_stacked: Optional[bool] = None,
    ) -> str:
        """
        Search assets by metadata criteria with caching and rate limiting.
        Fully compliant with Immich OpenAPI specs for /search/metadata.
        """
        try:
            search_query = {
                k: v
                for k, v in {
                    "albumIds": album_ids,
                    "checksum": checksum,
                    "city": city,
                    "country": country,
                    "createdAfter": created_after,
                    "createdBefore": created_before,
                    "description": description,
                    "deviceAssetId": device_asset_id,
                    "deviceId": device_id,
                    "encodedVideoPath": encoded_video_path,
                    "id": asset_id,
                    "isEncoded": is_encoded,
                    "isFavorite": is_favorite,
                    "isMotion": is_motion,
                    "isNotInAlbum": is_not_in_album,
                    "isOffline": is_offline,
                    "lensModel": lens_model,
                    "libraryId": library_id,
                    "make": make,
                    "model": model,
                    "order": order,
                    "originalFileName": original_file_name,
                    "originalPath": original_path,
                    "page": page,
                    "personIds": person_ids,
                    "previewPath": preview_path,
                    "rating": rating,
                    "size": size,
                    "state": state,
                    "tagIds": tag_ids,
                    "takenAfter": taken_after,
                    "takenBefore": taken_before,
                    "thumbnailPath": thumbnail_path,
                    "trashedAfter": trashed_after,
                    "trashedBefore": trashed_before,
                    "type": asset_type,
                    "updatedAfter": updated_after,
                    "updatedBefore": updated_before,
                    "visibility": visibility,
                    "withDeleted": with_deleted,
                    "withExif": with_exif,
                    "withPeople": with_people,
                    "withStacked": with_stacked,
                }.items()
                if v is not None
            }

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
        album_ids: Optional[List[str]] = None,
        city: Optional[str] = None,
        country: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        device_id: Optional[str] = None,
        is_encoded: Optional[bool] = None,
        is_favorite: Optional[bool] = None,
        is_motion: Optional[bool] = None,
        is_not_in_album: Optional[bool] = None,
        is_offline: Optional[bool] = None,
        language: Optional[str] = None,
        lens_model: Optional[str] = None,
        library_id: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        page: Optional[int] = None,
        person_ids: Optional[List[str]] = None,
        rating: Optional[int] = None,
        state: Optional[str] = None,
        tag_ids: Optional[List[str]] = None,
        taken_after: Optional[str] = None,
        taken_before: Optional[str] = None,
        trashed_after: Optional[str] = None,
        trashed_before: Optional[str] = None,
        asset_type: Optional[str] = None,
        updated_after: Optional[str] = None,
        updated_before: Optional[str] = None,
        visibility: Optional[str] = None,
        with_deleted: Optional[bool] = None,
        with_exif: Optional[bool] = None,
    ) -> str:
        """
        Smart search using AI to find assets based on natural language queries.
        """
        try:
            search_query = {"query": query, "size": limit}
            if page:
                search_query["page"] = page
            if library_id:
                search_query["libraryId"] = library_id
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
    async def search_people(self, name: str, with_hidden: Optional[bool] = None) -> str:
        """
        Search for people in the photo library with caching.
        """
        try:
            results = await self.client.search_people(name, with_hidden)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching people: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def search_places(self, name: str) -> str:
        """
        Search for places and locations in the photo library with caching.
        """
        try:
            results = await self.client.search_places(name)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching places: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=256)
    async def get_search_suggestions(
        self,
        type: str,
        country: Optional[str] = None,
        include_null: Optional[bool] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        state: Optional[str] = None,
    ) -> str:
        """
        Get search suggestions based on partial queries with caching.
        """
        try:
            results = await self.client.get_search_suggestions(
                type, country, include_null, make, model, state
            )
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
        self,
        closest_asset_id: Optional[str] = None,
        closest_person_id: Optional[str] = None,
        page: Optional[int] = None,
        size: Optional[int] = None,
        with_hidden: Optional[bool] = None,
    ) -> str:
        """
        Get all people from the photo library with caching and rate limiting.
        """
        try:
            results = await self.client.get_all_people(
                closest_asset_id, closest_person_id, page, size, with_hidden
            )
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
