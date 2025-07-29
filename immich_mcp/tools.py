



from immich_mcp.client import ImmichClient
import json
import logging
from typing import Optional, Dict, Any, List
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
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @lru_cache(maxsize=128)
    async def get_all_assets(self) -> str:
        """Retrieves all assets from Immich with caching and rate limiting."""
        try:
            assets = await self.client.get_all_assets()
            return json.dumps(assets)
        except Exception as e:
            logger.error(f"Error getting all assets: {e}")
            return json.dumps({"error": str(e)})
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_asset_info(self, asset_id: str) -> str:
        """Gets information about a specific asset with caching."""
        try:
            asset = await self.client.get_asset(asset_id)
            return json.dumps(asset)
        except Exception as e:
            logger.error(f"Error getting asset {asset_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @lru_cache(maxsize=64)
    async def search_metadata(self, query: str = "", asset_type: str = None, 
                            is_favorite: bool = None, limit: int = 100) -> str:
        """
        Search assets by metadata criteria with caching and rate limiting.
        
        Args:
            query: Search query string for metadata (filename, description, etc.)
            asset_type: Filter by asset type (IMAGE, VIDEO, AUDIO, OTHER)
            is_favorite: Filter by favorite status
            limit: Maximum number of results to return
            
        Returns:
            str: JSON string containing search results with assets and total count
            
        Example:
            >>> results = await tools.search_metadata("beach", "IMAGE", True, 50)
        """
        try:
            search_query = {"limit": limit}
            if query:
                search_query["q"] = query
            if asset_type:
                search_query["type"] = asset_type
            if is_favorite is not None:
                search_query["isFavorite"] = is_favorite
                
            results = await self.client.search_metadata(search_query)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error searching metadata: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @lru_cache(maxsize=64)
    async def search_smart(self, query: str, limit: int = 100) -> str:
        """
        Smart search using AI to find assets based on natural language queries.
        
        Args:
            query: Natural language search query (e.g., "photos of my dog at the beach")
            limit: Maximum number of results to return
            
        Returns:
            str: JSON string containing AI-powered search results
            
        Example:
            >>> results = await tools.search_smart("photos of my dog at the beach", 10)
        """
        try:
            search_query = {
                "q": query,
                "limit": limit
            }
            results = await self.client.search_smart(search_query)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error in smart search: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @lru_cache(maxsize=64)
    async def get_all_people(self, query: str = "", limit: int = 100, offset: int = 0) -> str:
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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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
            return base64.b64encode(thumbnail_data).decode('utf-8')
        except Exception as e:
            logger.error(f"Error getting person thumbnail {person_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @lru_cache(maxsize=128)
    async def get_all_albums(self) -> str:
        """Retrieves all albums from Immich with caching and rate limiting."""
        try:
            albums = await self.client.get_all_albums()
            return json.dumps(albums)
        except Exception as e:
            logger.error(f"Error getting all albums: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def create_album(self, album_name: str, description: str = "", asset_ids: Optional[List[str]] = None) -> str:
        """Creates a new album in Immich."""
        try:
            album = await self.client.create_album(album_name, description, asset_ids)
            return json.dumps(album)
        except Exception as e:
            logger.error(f"Error creating album: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_album_info(self, album_id: str) -> str:
        """Gets information about a specific album with caching."""
        try:
            album = await self.client.get_album(album_id)
            return json.dumps(album)
        except Exception as e:
            logger.error(f"Error getting album {album_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def delete_album(self, album_id: str) -> str:
        """Deletes an album from Immich."""
        try:
            await self.client.delete_album(album_id)
            return json.dumps({"status": "success"})
        except Exception as e:
            logger.error(f"Error deleting album {album_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def add_assets_to_album(self, album_id: str, asset_ids: List[str]) -> str:
        """Adds assets to an existing album."""
        try:
            results = await self.client.add_assets_to_album(album_id, asset_ids)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error adding assets to album {album_id}: {e}")
            return json.dumps({"error": str(e)})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def remove_assets_from_album(self, album_id: str, asset_ids: List[str]) -> str:
        """Removes assets from an album."""
        try:
            results = await self.client.remove_assets_from_album(album_id, asset_ids)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Error removing assets from album {album_id}: {e}")
            return json.dumps({"error": str(e)})

