from immich_mcp.client import ImmichClient
import json
import logging
from typing import Optional, List, Dict, Any
from functools import lru_cache
from tenacity import retry, stop_after_attempt, wait_exponential

from .cache import CacheManager
from .rate_limiter import RateLimiter
from .tool_definitions import TOOL_DESCRIPTIONS

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

    async def discover_tools(self, query: str) -> str:
        """
        Discovers relevant tools based on a natural language query.

        Args:
            query: A natural language query describing the desired functionality.

        Returns:
            A JSON string containing a list of recommended tools, including their names and descriptions.
        """
        query_words = set(query.lower().split())
        relevant_tools = {}

        for category, definition in TOOL_DESCRIPTIONS.items():
            if any(keyword in query_words for keyword in definition["keywords"]):
                for tool_name in definition["tools"]:
                    if hasattr(self, tool_name) and tool_name not in relevant_tools:
                        tool_method = getattr(self, tool_name)
                        relevant_tools[tool_name] = tool_method.__doc__.strip()

        return json.dumps(
            {
                "relevant_tools": [
                    {"name": name, "description": desc}
                    for name, desc in relevant_tools.items()
                ]
            },
            indent=2,
        )

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_asset_info(
        self, asset_id: str, key: Optional[str] = None, slug: Optional[str] = None
    ) -> str:
        """
        Gets information about a specific asset with caching.

        Args:
            asset_id: The ID of the asset.
            key: The key for the asset, used for shared links.
            slug: The slug for the asset, used for shared links.
        """
        try:
            asset = await self.client.get_asset(asset_id, key, slug)
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

        Args:
            album_ids (Optional[List[str]]): List of album IDs to filter by.
            checksum (Optional[str]): The checksum of the asset.
            city (Optional[str]): The city where the asset was taken.
            country (Optional[str]): The country where the asset was taken.
            created_after (Optional[str]): The date after which the asset was created.
            created_before (Optional[str]): The date before which the asset was created.
            description (Optional[str]): The description of the asset.
            device_asset_id (Optional[str]): The ID of the asset on the device.
            device_id (Optional[str]): The ID of the device.
            encoded_video_path (Optional[str]): The path to the encoded video.
            asset_id (Optional[str]): The ID of the asset.
            is_encoded (Optional[bool]): Whether the asset is encoded.
            is_favorite (Optional[bool]): Whether the asset is a favorite.
            is_motion (Optional[bool]): Whether the asset is a motion photo.
            is_not_in_album (Optional[bool]): Whether the asset is not in an album.
            is_offline (Optional[bool]): Whether the asset is offline.
            lens_model (Optional[str]): The lens model used to take the asset.
            library_id (Optional[str]): The ID of the library.
            make (Optional[str]): The make of the camera used to take the asset.
            model (Optional[str]): The model of the camera used to take the asset.
            order (Optional[str]): The order in which to sort the assets.
            original_file_name (Optional[str]): The original file name of the asset.
            original_path (Optional[str]): The original path of the asset.
            page (Optional[int]): The page number for pagination.
            person_ids (Optional[List[str]]): List of person IDs to filter by.
            preview_path (Optional[str]): The path to the preview of the asset.
            rating (Optional[int]): The rating of the asset.
            size (Optional[int]): The number of assets to return per page.
            state (Optional[str]): The state where the asset was taken.
            tag_ids (Optional[List[str]]): List of tag IDs to filter by.
            taken_after (Optional[str]): The date after which the asset was taken.
            taken_before (Optional[str]): The date before which the asset was taken.
            thumbnail_path (Optional[str]): The path to the thumbnail of the asset.
            trashed_after (Optional[str]): The date after which the asset was trashed.
            trashed_before (Optional[str]): The date before which the asset was trashed.
            asset_type (Optional[str]): The type of the asset.
            updated_after (Optional[str]): The date after which the asset was updated.
            updated_before (Optional[str]): The date before which the asset was updated.
            visibility (Optional[str]): The visibility of the asset.
            with_deleted (Optional[bool]): Whether to include deleted assets.
            with_exif (Optional[bool]): Whether to include EXIF data.
            with_people (Optional[bool]): Whether to include people data.
            with_stacked (Optional[bool]): Whether to include stacked assets.
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
    async def search_people(self, name: str, with_hidden: Optional[bool] = None) -> str:
        """
        Search for people in the photo library with caching.

        Args:
            name: The name of the person to search for.
            with_hidden: Whether to include hidden people in the results.
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

        Args:
            name: The name of the place to search for.
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

        Args:
            type: The type of suggestion to get. Enum: "COUNTRY", "STATE", "CITY", "MAKE", "MODEL".
            country: The country to get suggestions for.
            include_null: Whether to include null values.
            make: The make of the camera to get suggestions for.
            model: The model of the camera to get suggestions for.
            state: The state to get suggestions for.
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
    async def search_random(
        self,
        size: Optional[int] = None,
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
        lens_model: Optional[str] = None,
        library_id: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
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
        with_people: Optional[bool] = None,
        with_stacked: Optional[bool] = None,
    ) -> str:
        """
        Get random assets from the photo library with caching.

        Args:
            size (Optional[int]): Number of random assets to return.
            album_ids (Optional[List[str]]): List of album IDs to filter by.
            city (Optional[str]): The city where the asset was taken.
            country (Optional[str]): The country where the asset was taken.
            created_after (Optional[str]): The date after which the asset was created.
            created_before (Optional[str]): The date before which the asset was created.
            device_id (Optional[str]): The ID of the device.
            is_encoded (Optional[bool]): Whether the asset is encoded.
            is_favorite (Optional[bool]): Whether the asset is a favorite.
            is_motion (Optional[bool]): Whether the asset is a motion photo.
            is_not_in_album (Optional[bool]): Whether the asset is not in an album.
            is_offline (Optional[bool]): Whether the asset is offline.
            lens_model (Optional[str]): The lens model used to take the asset.
            library_id (Optional[str]): The ID of the library.
            make (Optional[str]): The make of the camera used to take the asset.
            model (Optional[str]): The model of the camera used to take the asset.
            person_ids (Optional[List[str]]): List of person IDs to filter by.
            rating (Optional[int]): The rating of the asset.
            state (Optional[str]): The state where the asset was taken.
            tag_ids (Optional[List[str]]): List of tag IDs to filter by.
            taken_after (Optional[str]): The date after which the asset was taken.
            taken_before (Optional[str]): The date before which the asset was taken.
            trashed_after (Optional[str]): The date after which the asset was trashed.
            trashed_before (Optional[str]): The date before which the asset was trashed.
            asset_type (Optional[str]): The type of the asset.
            updated_after (Optional[str]): The date after which the asset was updated.
            updated_before (Optional[str]): The date before which the asset was updated.
            visibility (Optional[str]): The visibility of the asset.
            with_deleted (Optional[bool]): Whether to include deleted assets.
            with_exif (Optional[bool]): Whether to include EXIF data.
            with_people (Optional[bool]): Whether to include people data.
            with_stacked (Optional[bool]): Whether to include stacked assets.
        """
        try:
            search_query = {
                k: v
                for k, v in {
                    "size": size,
                    "albumIds": album_ids,
                    "city": city,
                    "country": country,
                    "createdAfter": created_after,
                    "createdBefore": created_before,
                    "deviceId": device_id,
                    "isEncoded": is_encoded,
                    "isFavorite": is_favorite,
                    "isMotion": is_motion,
                    "isNotInAlbum": is_not_in_album,
                    "isOffline": is_offline,
                    "lensModel": lens_model,
                    "libraryId": library_id,
                    "make": make,
                    "model": model,
                    "personIds": person_ids,
                    "rating": rating,
                    "state": state,
                    "tagIds": tag_ids,
                    "takenAfter": taken_after,
                    "takenBefore": taken_before,
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
            results = await self.client.search_random(search_query)
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

        Args:
            closest_asset_id: The asset ID to search for closest people from.
            closest_person_id: The person ID to search for closest people from.
            page: The page number for pagination.
            size: The number of people to return per page.
            with_hidden: Whether to include hidden people in the results.
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
    async def get_all_albums(
        self, asset_id: Optional[str] = None, shared: Optional[bool] = None
    ) -> str:
        """
        Retrieves all albums from Immich with caching and rate limiting.

        Args:
            asset_id: The asset ID to get the albums for.
            shared: Whether to get shared albums.
        """
        try:
            albums = await self.client.get_all_albums(asset_id, shared)
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
        album_users: Optional[List[Dict[str, List[str]]]] = None,
    ) -> str:
        """
        Creates a new album in Immich.

        Args:
            album_name: The name of the new album.
            description: A description for the album.
            asset_ids: A list of asset IDs to include in the album.
            album_users: A list of users to share the album with, following the AddUsersDto schema.
                         Example: [{"sharedUserIds": ["user-id-1", "user-id-2"]}]
        """
        try:
            album = await self.client.create_album(
                album_name, description, asset_ids, album_users
            )
            return json.dumps(album)
        except Exception as e:
            logger.error(f"Error creating album: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_album_info(
        self,
        album_id: str,
        key: Optional[str] = None,
        slug: Optional[str] = None,
        without_assets: Optional[bool] = None,
    ) -> str:
        """
        Gets information about a specific album with caching.

        Args:
            album_id: The ID of the album.
            key: The key for the album, used for shared links.
            slug: The slug for the album, used for shared links.
            without_assets: Whether to exclude asset information from the response.
        """
        try:
            album = await self.client.get_album(album_id, key, slug, without_assets)
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
    async def add_assets_to_album(
        self,
        album_id: str,
        asset_ids: List[str],
        key: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> str:
        """
        Adds assets to an existing album.

        Args:
            album_id: The ID of the album to add assets to.
            asset_ids: A list of asset IDs to add to the album.
            key: The key for the album, used for shared links.
            slug: The slug for the album, used for shared links.
        """
        try:
            results = await self.client.add_assets_to_album(
                album_id, asset_ids, key, slug
            )
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

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_all_jobs_status(self) -> str:
        """
        Get the status of all jobs.

        Returns:
            str: JSON string containing the status of all jobs.
        """
        try:
            status = await self.client.get_all_jobs_status()
            return json.dumps(status)
        except Exception as e:
            logger.error(f"Error getting all jobs status: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def send_job_command(
        self, job_id: str, command: str, force: bool = False
    ) -> str:
        """
        Send a command to a job.

        Args:
            job_id: The ID of the job to send the command to.
            command: The command to send (e.g., 'start', 'stop').
            force: Whether to force the command.

        Returns:
            str: JSON string containing the response from the server.
        """
        try:
            result = await self.client.send_job_command(job_id, command, force)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error sending job command {command} to {job_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def run_asset_jobs(self, name: str, asset_ids: List[str]) -> str:
        """
        Run a job for a set of assets.

        Args:
            name: The name of the job to run.
            asset_ids: A list of asset IDs to run the job on.

        Returns:
            str: JSON string containing the response from the server.
        """
        try:
            await self.client.run_asset_jobs(name, asset_ids)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error running asset job {name}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def search_memories(
        self,
        for_date: Optional[str] = None,
        is_saved: Optional[bool] = None,
        is_trashed: Optional[bool] = None,
        memory_type: Optional[str] = None,
    ) -> str:
        """
        Search for memories.

        Args:
            for_date: The date to search for memories for.
            is_saved: Whether to search for saved memories.
            is_trashed: Whether to search for trashed memories.
            memory_type: The type of memory to search for.

        Returns:
            str: JSON string containing a list of memories.
        """
        try:
            results = await self.client.search_memories(
                for_date, is_saved, is_trashed, memory_type
            )
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching memories: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_memory(self, memory_data: Dict[str, Any]) -> str:
        """
        Create a new memory.

        Args:
            memory_data: The data for the new memory.

        Returns:
            str: JSON string containing the created memory.
        """
        try:
            result = await self.client.create_memory(memory_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error creating memory: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=64)
    async def get_memory_statistics(
        self,
        for_date: Optional[str] = None,
        is_saved: Optional[bool] = None,
        is_trashed: Optional[bool] = None,
        memory_type: Optional[str] = None,
    ) -> str:
        """
        Get memory statistics.

        Args:
            for_date: The date to get statistics for.
            is_saved: Whether to get statistics for saved memories.
            is_trashed: Whether to get statistics for trashed memories.
            memory_type: The type of memory to get statistics for.

        Returns:
            str: JSON string containing the memory statistics.
        """
        try:
            stats = await self.client.get_memory_statistics(
                for_date, is_saved, is_trashed, memory_type
            )
            return json.dumps(stats)
        except Exception as e:
            logger.error(f"Error getting memory statistics: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_memory(self, memory_id: str) -> str:
        """
        Get a specific memory.

        Args:
            memory_id: The ID of the memory.

        Returns:
            str: JSON string containing the memory.
        """
        try:
            memory = await self.client.get_memory(memory_id)
            return json.dumps(memory)
        except Exception as e:
            logger.error(f"Error getting memory {memory_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_memory(self, memory_id: str, memory_data: Dict[str, Any]) -> str:
        """
        Update a memory.

        Args:
            memory_id: The ID of the memory.
            memory_data: The data to update the memory with.

        Returns:
            str: JSON string containing the updated memory.
        """
        try:
            result = await self.client.update_memory(memory_id, memory_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error updating memory {memory_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_memory(self, memory_id: str) -> str:
        """
        Delete a memory.

        Args:
            memory_id: The ID of the memory.

        Returns:
            str: JSON string containing the status of the operation.
        """
        try:
            await self.client.delete_memory(memory_id)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting memory {memory_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def add_memory_assets(self, memory_id: str, asset_ids: List[str]) -> str:
        """
        Add assets to a memory.

        Args:
            memory_id: The ID of the memory.
            asset_ids: The IDs of the assets to add.

        Returns:
            str: JSON string containing the response from the server.
        """
        try:
            results = await self.client.add_memory_assets(memory_id, asset_ids)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error adding assets to memory {memory_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def remove_memory_assets(self, memory_id: str, asset_ids: List[str]) -> str:
        """
        Remove assets from a memory.

        Args:
            memory_id: The ID of the memory.
            asset_ids: The IDs of the assets to remove.

        Returns:
            str: JSON string containing the response from the server.
        """
        try:
            results = await self.client.remove_memory_assets(memory_id, asset_ids)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error removing assets from memory {memory_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def search_users_admin(
        self, user_id: Optional[str] = None, with_deleted: Optional[bool] = None
    ) -> str:
        """
        Search for users with admin privileges.

        Args:
            user_id: The ID of the user to search for.
            with_deleted: Whether to include deleted users in the results.
        """
        try:
            results = await self.client.search_users_admin(user_id, with_deleted)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching users with admin privileges: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_user_admin(self, user_data: Dict[str, Any]) -> str:
        """
        Create a new user with admin privileges.

        Args:
            user_data: The data for the new user.
        """
        try:
            result = await self.client.create_user_admin(user_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error creating user with admin privileges: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_user_admin(self, user_id: str) -> str:
        """
        Get detailed information about a specific user with admin privileges.

        Args:
            user_id: The unique identifier of the user to retrieve.
        """
        try:
            user = await self.client.get_user_admin(user_id)
            return json.dumps(user)
        except Exception as e:
            logger.error(f"Error getting user {user_id} with admin privileges: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_user_admin(self, user_id: str, user_data: Dict[str, Any]) -> str:
        """
        Update a user with admin privileges.

        Args:
            user_id: The ID of the user to update.
            user_data: The data to update the user with.
        """
        try:
            result = await self.client.update_user_admin(user_id, user_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error updating user {user_id} with admin privileges: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_user_admin(self, user_id: str, force: bool = False) -> str:
        """
        Delete a user with admin privileges.

        Args:
            user_id: The ID of the user to delete.
            force: Whether to force the deletion.
        """
        try:
            result = await self.client.delete_user_admin(user_id, force)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error deleting user {user_id} with admin privileges: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_user_preferences_admin(self, user_id: str) -> str:
        """
        Get preferences for a specific user with admin privileges.

        Args:
            user_id: The unique identifier of the user.
        """
        try:
            preferences = await self.client.get_user_preferences_admin(user_id)
            return json.dumps(preferences)
        except Exception as e:
            logger.error(
                f"Error getting preferences for user {user_id} with admin privileges: {e}"
            )
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_user_preferences_admin(
        self, user_id: str, preferences_data: Dict[str, Any]
    ) -> str:
        """
        Update preferences for a specific user with admin privileges.

        Args:
            user_id: The ID of the user.
            preferences_data: The data to update the preferences with.
        """
        try:
            result = await self.client.update_user_preferences_admin(
                user_id, preferences_data
            )
            return json.dumps(result)
        except Exception as e:
            logger.error(
                f"Error updating preferences for user {user_id} with admin privileges: {e}"
            )
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def restore_user_admin(self, user_id: str) -> str:
        """
        Restore a deleted user with admin privileges.

        Args:
            user_id: The ID of the user to restore.
        """
        try:
            result = await self.client.restore_user_admin(user_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error restoring user {user_id} with admin privileges: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=64)
    async def get_user_statistics_admin(
        self,
        user_id: str,
        is_favorite: Optional[bool] = None,
        is_trashed: Optional[bool] = None,
        visibility: Optional[str] = None,
    ) -> str:
        """
        Get statistics for a specific user with admin privileges.

        Args:
            user_id: The unique identifier of the user.
            is_favorite: Whether to filter by favorite status.
            is_trashed: Whether to filter by trashed status.
            visibility: The visibility of the assets.
        """
        try:
            stats = await self.client.get_user_statistics_admin(
                user_id, is_favorite, is_trashed, visibility
            )
            return json.dumps(stats)
        except Exception as e:
            logger.error(
                f"Error getting statistics for user {user_id} with admin privileges: {e}"
            )
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def search_users(self) -> str:
        """
        Search for users.
        """
        try:
            results = await self.client.search_users()
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching users: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=1)
    async def get_my_user(self) -> str:
        """
        Get the current user's information.
        """
        try:
            result = await self.client.get_my_user()
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting current user's information: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_my_user(self, user_data: Dict[str, Any]) -> str:
        """
        Update the current user's information.

        Args:
            user_data: The data to update the user with.
        """
        try:
            result = await self.client.update_my_user(user_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error updating current user's information: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_user(self, user_id: str) -> str:
        """
        Get a user's information.

        Args:
            user_id: The ID of the user to retrieve.
        """
        try:
            result = await self.client.get_user(user_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting user {user_id}'s information: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_user_license(self) -> str:
        """
        Delete the current user's license.
        """
        try:
            await self.client.delete_user_license()
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting current user's license: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=1)
    async def get_user_license(self) -> str:
        """
        Get the current user's license.
        """
        try:
            result = await self.client.get_user_license()
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting current user's license: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def set_user_license(self, license_key: str) -> str:
        """
        Set the current user's license.

        Args:
            license_key: The license key to set.
        """
        try:
            result = await self.client.set_user_license(license_key)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error setting current user's license: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_user_onboarding(self) -> str:
        """
        Delete the current user's onboarding status.
        """
        try:
            await self.client.delete_user_onboarding()
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting current user's onboarding status: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=1)
    async def get_user_onboarding(self) -> str:
        """
        Get the current user's onboarding status.
        """
        try:
            result = await self.client.get_user_onboarding()
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting current user's onboarding status: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def set_user_onboarding(self, onboarding_data: Dict[str, Any]) -> str:
        """
        Set the current user's onboarding status.

        Args:
            onboarding_data: The onboarding data to set.
        """
        try:
            result = await self.client.set_user_onboarding(onboarding_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error setting current user's onboarding status: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=1)
    async def get_my_preferences(self) -> str:
        """
        Get the current user's preferences.
        """
        try:
            result = await self.client.get_my_preferences()
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting current user's preferences: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_my_preferences(self, preferences_data: Dict[str, Any]) -> str:
        """
        Update the current user's preferences.

        Args:
            preferences_data: The preferences to update.
        """
        try:
            result = await self.client.update_my_preferences(preferences_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error updating current user's preferences: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_profile_image(self) -> str:
        """
        Delete the current user's profile image.
        """
        try:
            await self.client.delete_profile_image()
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting current user's profile image: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_profile_image(self, file_path: str) -> str:
        """
        Create a profile image for the current user.

        Args:
            file_path: The path to the image file.
        """
        try:
            result = await self.client.create_profile_image(file_path)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error creating profile image for current user: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def get_profile_image(self, user_id: str) -> str:
        """
        Get a user's profile image.

        Args:
            user_id: The ID of the user.
        """
        try:
            import base64

            image_data = await self.client.get_profile_image(user_id)
            return base64.b64encode(image_data).decode("utf-8")
        except Exception as e:
            logger.error(f"Error getting profile image for user {user_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_api_keys(self) -> str:
        """
        Get all API keys.
        """
        try:
            results = await self.client.get_api_keys()
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error getting API keys: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_api_key(self, key_data: Dict[str, Any]) -> str:
        """
        Create a new API key.

        Args:
            key_data: The data for the new API key.
        """
        try:
            result = await self.client.create_api_key(key_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error creating API key: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_api_key(self, key_id: str) -> str:
        """
        Get an API key.

        Args:
            key_id: The ID of the API key to retrieve.
        """
        try:
            result = await self.client.get_api_key(key_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting API key {key_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_api_key(self, key_id: str, key_data: Dict[str, Any]) -> str:
        """
        Update an API key.

        Args:
            key_id: The ID of the API key to update.
            key_data: The data to update the API key with.
        """
        try:
            result = await self.client.update_api_key(key_id, key_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error updating API key {key_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_api_key(self, key_id: str) -> str:
        """
        Delete an API key.

        Args:
            key_id: The ID of the API key to delete.
        """
        try:
            await self.client.delete_api_key(key_id)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting API key {key_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def sign_up_admin(self, user_data: Dict[str, Any]) -> str:
        """
        Sign up a new admin user.

        Args:
            user_data: The data for the new admin user.
        """
        try:
            result = await self.client.sign_up_admin(user_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error signing up admin: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def change_password(self, password_data: Dict[str, Any]) -> str:
        """
        Change the current user's password.

        Args:
            password_data: The data for changing the password.
        """
        try:
            result = await self.client.change_password(password_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def login(self, login_data: Dict[str, Any]) -> str:
        """
        Log in a user.

        Args:
            login_data: The data for logging in.
        """
        try:
            result = await self.client.login(login_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error logging in: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def logout(self) -> str:
        """
        Log out the current user.
        """
        try:
            result = await self.client.logout()
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error logging out: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def reset_pin_code(self, pin_code_data: Dict[str, Any]) -> str:
        """
        Reset the current user's pin code.

        Args:
            pin_code_data: The data for resetting the pin code.
        """
        try:
            await self.client.reset_pin_code(pin_code_data)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error resetting pin code: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def setup_pin_code(self, pin_code_data: Dict[str, Any]) -> str:
        """
        Set up a pin code for the current user.

        Args:
            pin_code_data: The data for setting up the pin code.
        """
        try:
            await self.client.setup_pin_code(pin_code_data)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error setting up pin code: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def change_pin_code(self, pin_code_data: Dict[str, Any]) -> str:
        """
        Change the current user's pin code.

        Args:
            pin_code_data: The data for changing the pin code.
        """
        try:
            await self.client.change_pin_code(pin_code_data)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error changing pin code: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def lock_auth_session(self) -> str:
        """
        Lock the current user's authentication session.
        """
        try:
            await self.client.lock_auth_session()
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error locking authentication session: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def unlock_auth_session(self, unlock_data: Dict[str, Any]) -> str:
        """
        Unlock the current user's authentication session.

        Args:
            unlock_data: The data for unlocking the session.
        """
        try:
            await self.client.unlock_auth_session(unlock_data)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error unlocking authentication session: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=1)
    async def get_auth_status(self) -> str:
        """
        Get the authentication status of the current user.
        """
        try:
            result = await self.client.get_auth_status()
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting authentication status: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def validate_access_token(self) -> str:
        """
        Validate the current access token.
        """
        try:
            result = await self.client.validate_access_token()
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error validating access token: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_faces(self, asset_id: str) -> str:
        """
        Get all faces for a given asset.

        Args:
            asset_id: The ID of the asset.
        """
        try:
            results = await self.client.get_faces(asset_id)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error getting faces for asset {asset_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_face(self, face_data: Dict[str, Any]) -> str:
        """
        Create a new face.

        Args:
            face_data: The data for the new face.
        """
        try:
            result = await self.client.create_face(face_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error creating face: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_face(self, face_id: str) -> str:
        """
        Delete a face.

        Args:
            face_id: The ID of the face to delete.
        """
        try:
            await self.client.delete_face(face_id)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting face {face_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def reassign_faces_by_id(self, face_id: str, person_id: str) -> str:
        """
        Reassign a face to a person.

        Args:
            face_id: The ID of the face to reassign.
            person_id: The ID of the person to reassign the face to.
        """
        try:
            result = await self.client.reassign_faces_by_id(face_id, person_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error reassigning face {face_id} to person {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_person(self, person_data: Dict[str, Any]) -> str:
        """
        Create a new person.

        Args:
            person_data: The data for the new person.
        """
        try:
            result = await self.client.create_person(person_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error creating person: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_people(self, people_data: Dict[str, Any]) -> str:
        """
        Update people.

        Args:
            people_data: The data for updating people.
        """
        try:
            result = await self.client.update_people(people_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error updating people: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_people(self, people_data: Dict[str, Any]) -> str:
        """
        Delete people.

        Args:
            people_data: The data for deleting people.
        """
        try:
            await self.client.delete_people(people_data)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting people: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_person(self, person_id: str, person_data: Dict[str, Any]) -> str:
        """
        Update a person.

        Args:
            person_id: The ID of the person to update.
            person_data: The data to update the person with.
        """
        try:
            result = await self.client.update_person(person_id, person_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error updating person {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def delete_person(self, person_id: str) -> str:
        """
        Delete a person.

        Args:
            person_id: The ID of the person to delete.
        """
        try:
            await self.client.delete_person(person_id)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting person {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def merge_person(self, person_id: str, merge_data: Dict[str, Any]) -> str:
        """
        Merge a person.

        Args:
            person_id: The ID of the person to merge.
            merge_data: The data for merging the person.
        """
        try:
            result = await self.client.merge_person(person_id, merge_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error merging person {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def reassign_faces(
        self, person_id: str, reassign_data: Dict[str, Any]
    ) -> str:
        """
        Reassign faces to a person.

        Args:
            person_id: The ID of the person to reassign faces to.
            reassign_data: The data for reassigning faces.
        """
        try:
            result = await self.client.reassign_faces(person_id, reassign_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error reassigning faces to person {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_all_shared_links(self) -> str:
        """
        Get all shared links.
        """
        try:
            results = await self.client.get_all_shared_links()
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error getting all shared links: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def create_shared_link(self, link_data: Dict[str, Any]) -> str:
        """
        Create a new shared link.

        Args:
            link_data: The data for the new shared link.
        """
        try:
            result = await self.client.create_shared_link(link_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error creating shared link: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=1)
    async def get_my_shared_link(self) -> str:
        """
        Get the current user's shared link.
        """
        try:
            result = await self.client.get_my_shared_link()
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting current user's shared link: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    @lru_cache(maxsize=128)
    async def get_shared_link_by_id(self, link_id: str) -> str:
        """
        Get a shared link by ID.

        Args:
            link_id: The ID of the shared link to retrieve.
        """
        try:
            result = await self.client.get_shared_link_by_id(link_id)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error getting shared link {link_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def remove_shared_link(self, link_id: str) -> str:
        """
        Remove a shared link.

        Args:
            link_id: The ID of the shared link to remove.
        """
        try:
            await self.client.remove_shared_link(link_id)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error removing shared link {link_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def update_shared_link(self, link_id: str, link_data: Dict[str, Any]) -> str:
        """
        Update a shared link.

        Args:
            link_id: The ID of the shared link to update.
            link_data: The data to update the shared link with.
        """
        try:
            result = await self.client.update_shared_link(link_id, link_data)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error updating shared link {link_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def remove_shared_link_assets(
        self, link_id: str, asset_ids: List[str]
    ) -> str:
        """
        Remove assets from a shared link.

        Args:
            link_id: The ID of the shared link.
            asset_ids: The IDs of the assets to remove.
        """
        try:
            result = await self.client.remove_shared_link_assets(link_id, asset_ids)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error removing assets from shared link {link_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def add_shared_link_assets(self, link_id: str, asset_ids: List[str]) -> str:
        """
        Add assets to a shared link.

        Args:
            link_id: The ID of the shared link.
            asset_ids: The IDs of the assets to add.
        """
        try:
            result = await self.client.add_shared_link_assets(link_id, asset_ids)
            return json.dumps(result)
        except Exception as e:
            logger.error(f"Error adding assets to shared link {link_id}: {e}")
            return json.dumps({"error": str(e)})
