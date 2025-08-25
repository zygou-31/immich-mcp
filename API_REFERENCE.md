# 📖 API Reference

**Important Note:** All tool endpoints listed below must be prefixed with `/mcp`. For example, the `discover_tools` tool is available at `/mcp/discover_tools`.

### Available Tools

#### `discover_tools(query: str)`
Discovers relevant tools based on a natural language query.

**Parameters:**
- `query` (str): A natural language query describing the desired functionality.

**Returns:** A JSON string containing a list of recommended tools, including their names and descriptions.

#### `get_asset_info(asset_id: str, key: Optional[str] = None, slug: Optional[str] = None)`
Gets detailed information about a specific asset.

**Parameters:**
- `asset_id` (str): The unique identifier of the asset.
- `key` (str, optional): The key for the asset, used for shared links.
- `slug` (str, optional): The slug for the asset, used for shared links.

**Returns:** JSON string containing asset details.

#### `search_metadata(...)`
Search assets by metadata criteria. This tool accepts a large number of optional parameters based on the Immich API.

**Example Parameters:**
- `is_favorite: bool = True`
- `city: str = "London"`
- `person_ids: List[str] = ["..."]`
- ... and many more. See the tool's docstring for a full list.

**Returns:** JSON string containing search results.

#### `search_smart(...)`
Smart search using AI to find assets based on natural language queries.

**Parameters:**
- `query` (str): Natural language search query.
- ... and many other optional filter parameters. See the tool's docstring.

**Returns:** JSON string containing AI-powered search results.

#### `search_people(name: str, with_hidden: Optional[bool] = None)`
Search for people in the photo library.

**Parameters:**
- `name` (str): The name of the person to search for.
- `with_hidden` (bool, optional): Whether to include hidden people in the results.

**Returns:** JSON string containing a list of people.

#### `search_places(name: str)`
Search for places and locations in the photo library.

**Parameters:**
- `name` (str): The name of the place to search for.

**Returns:** JSON string containing a list of places.

#### `get_search_suggestions(...)`
Get search suggestions based on partial queries.

**Parameters:**
- `type` (str): The type of suggestion to get (e.g., "CITY", "MAKE").
- ... and other optional filter parameters. See the tool's docstring.

**Returns:** JSON string containing a list of suggestions.

#### `search_random(...)`
Get random assets from the photo library, with optional filters.

**Example Parameters:**
- `size: int = 10`
- `is_favorite: bool = True`
- ... and many more. See the tool's docstring.

**Returns:** JSON string containing a list of random assets.

#### `get_all_people(...)`
Get all people from the photo library, with optional filters.

**Example Parameters:**
- `page: int = 1`
- `with_hidden: bool = False`
- ... and other optional parameters. See the tool's docstring.

**Returns:** JSON string containing a list of people.

#### `get_person(person_id: str)`
Get detailed information about a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person.

**Returns:** JSON string containing person details.

#### `get_person_statistics(person_id: str)`
Get statistics for a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person.

**Returns:** JSON string containing statistics.

#### `get_person_thumbnail(person_id: str)`
Get a thumbnail image for a specific person.

**Parameters:**
- `person_id` (str): The unique identifier of the person.

**Returns:** Base64 encoded thumbnail image data.

#### `get_all_albums(asset_id: Optional[str] = None, shared: Optional[bool] = None)`
Retrieves all albums from your Immich library.

**Parameters:**
- `asset_id` (str, optional): Filter albums containing this asset.
- `shared` (bool, optional): Filter for shared or non-shared albums.

**Returns:** JSON string containing an array of album objects.

#### `create_album(album_name: str, description: str = "", asset_ids: Optional[List[str]] = None, album_users: Optional[List[Dict[str, List[str]]]] = None)`
Creates a new album.

**Parameters:**
- `album_name` (str): Name of the new album.
- `description` (str, optional): Album description.
- `asset_ids` (list, optional): List of asset IDs to include.
- `album_users` (list, optional): List of users to share with.

**Returns:** JSON string containing created album details.

#### `get_album_info(album_id: str, key: Optional[str] = None, slug: Optional[str] = None, without_assets: Optional[bool] = None)`
Gets information about a specific album.

**Parameters:**
- `album_id` (str): The unique identifier of the album.
- `key` (str, optional): Key for shared links.
- `slug` (str, optional): Slug for shared links.
- `without_assets` (bool, optional): Exclude asset information.

**Returns:** JSON string containing album details.

#### `delete_album(album_id: str)`
Deletes an album from Immich.

**Parameters:**
- `album_id` (str): The unique identifier of the album to delete.

**Returns:** JSON string containing status.

#### `add_assets_to_album(album_id: str, asset_ids: List[str], key: Optional[str] = None, slug: Optional[str] = None)`
Adds assets to an existing album.

**Parameters:**
- `album_id` (str): The unique identifier of the album.
- `asset_ids` (list): List of asset IDs to add.
- `key` (str, optional): Key for shared links.
- `slug` (str, optional): Slug for shared links.

**Returns:** JSON string containing results.

#### `remove_assets_from_album(album_id: str, asset_ids: List[str])`
Removes assets from an album.

**Parameters:**
- `album_id` (str): The unique identifier of the album.
- `asset_ids` (list): List of asset IDs to remove.

**Returns:** JSON string containing results.

#### `search_memories(for_date: Optional[str] = None, is_saved: Optional[bool] = None, is_trashed: Optional[bool] = None, memory_type: Optional[str] = None)`
Search for memories.

**Parameters:**
- `for_date` (str, optional): The date to search for memories for.
- `is_saved` (bool, optional): Whether to search for saved memories.
- `is_trashed` (bool, optional): Whether to search for trashed memories.
- `memory_type` (str, optional): The type of memory to search for.

**Returns:** JSON string containing a list of memories.

#### `create_memory(memory_data: Dict[str, Any])`
Create a new memory.

**Parameters:**
- `memory_data` (dict): The data for the new memory.

**Returns:** JSON string containing the created memory.

#### `get_memory_statistics(for_date: Optional[str] = None, is_saved: Optional[bool] = None, is_trashed: Optional[bool] = None, memory_type: Optional[str] = None)`
Get memory statistics.

**Parameters:**
- `for_date` (str, optional): The date to get statistics for.
- `is_saved` (bool, optional): Whether to get statistics for saved memories.
- `is_trashed` (bool, optional): Whether to get statistics for trashed memories.
- `memory_type` (str, optional): The type of memory to get statistics for.

**Returns:** JSON string containing the memory statistics.

#### `get_memory(memory_id: str)`
Get a specific memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.

**Returns:** JSON string containing the memory.

#### `update_memory(memory_id: str, memory_data: Dict[str, Any])`
Update a memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.
- `memory_data` (dict): The data to update the memory with.

**Returns:** JSON string containing the updated memory.

#### `delete_memory(memory_id: str)`
Delete a memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.

**Returns:** JSON string containing the status of the operation.

#### `add_memory_assets(memory_id: str, asset_ids: List[str])`
Add assets to a memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.
- `asset_ids` (list): The IDs of the assets to add.

**Returns:** JSON string containing the response from the server.

#### `remove_memory_assets(memory_id: str, asset_ids: List[str])`
Remove assets from a memory.

**Parameters:**
- `memory_id` (str): The ID of the memory.
- `asset_ids` (list): The IDs of the assets to remove.

**Returns:** JSON string containing the response from the server.

### Users (admin)

#### `search_users_admin(user_id: Optional[str] = None, with_deleted: Optional[bool] = None)`
Search for users with admin privileges.

**Parameters:**
- `user_id` (str, optional): The ID of the user to search for.
- `with_deleted` (bool, optional): Whether to include deleted users in the results.

**Returns:** JSON string containing a list of users.

#### `create_user_admin(user_data: Dict[str, Any])`
Create a new user with admin privileges.

**Parameters:**
- `user_data` (dict): The data for the new user.

**Returns:** JSON string containing the created user.

#### `get_user_admin(user_id: str)`
Get detailed information about a specific user with admin privileges.

**Parameters:**
- `user_id` (str): The unique identifier of the user to retrieve.

**Returns:** JSON string containing user details.

#### `update_user_admin(user_id: str, user_data: Dict[str, Any])`
Update a user with admin privileges.

**Parameters:**
- `user_id` (str): The ID of the user to update.
- `user_data` (dict): The data to update the user with.

**Returns:** JSON string containing the updated user.

#### `delete_user_admin(user_id: str, force: bool = False)`
Delete a user with admin privileges.

**Parameters:**
- `user_id` (str): The ID of the user to delete.
- `force` (bool, optional): Whether to force the deletion.

**Returns:** JSON string containing the deleted user.

#### `get_user_preferences_admin(user_id: str)`
Get preferences for a specific user with admin privileges.

**Parameters:**
- `user_id` (str): The unique identifier of the user.

**Returns:** JSON string containing the user's preferences.

#### `update_user_preferences_admin(user_id: str, preferences_data: Dict[str, Any])`
Update preferences for a specific user with admin privileges.

**Parameters:**
- `user_id` (str): The ID of the user.
- `preferences_data` (dict): The data to update the preferences with.

**Returns:** JSON string containing the updated preferences.

#### `restore_user_admin(user_id: str)`
Restore a deleted user with admin privileges.

**Parameters:**
- `user_id` (str): The ID of the user to restore.

**Returns:** JSON string containing the restored user.

#### `get_user_statistics_admin(user_id: str, is_favorite: Optional[bool] = None, is_trashed: Optional[bool] = None, visibility: Optional[str] = None)`
Get statistics for a specific user with admin privileges.

**Parameters:**
- `user_id` (str): The unique identifier of the user.
- `is_favorite` (bool, optional): Whether to filter by favorite status.
- `is_trashed` (bool, optional): Whether to filter by trashed status.
- `visibility` (str, optional): The visibility of the assets.

**Returns:** JSON string containing the user's statistics.

### Users

#### `search_users()`
Search for users.

**Returns:** JSON string containing a list of users.

#### `get_my_user()`
Get the current user's information.

**Returns:** JSON string containing the current user's information.

#### `update_my_user(user_data: Dict[str, Any])`
Update the current user's information.

**Parameters:**
- `user_data` (dict): The data to update the user with.

**Returns:** JSON string containing the updated user information.

#### `get_user(user_id: str)`
Get a user's information.

**Parameters:**
- `user_id` (str): The ID of the user to retrieve.

**Returns:** JSON string containing the user's information.

#### `delete_user_license()`
Delete the current user's license.

**Returns:** JSON string containing the status of the operation.

#### `get_user_license()`
Get the current user's license.

**Returns:** JSON string containing the user's license.

#### `set_user_license(license_key: str)`
Set the current user's license.

**Parameters:**
- `license_key` (str): The license key to set.

**Returns:** JSON string containing the user's license.

#### `delete_user_onboarding()`
Delete the current user's onboarding status.

**Returns:** JSON string containing the status of the operation.

#### `get_user_onboarding()`
Get the current user's onboarding status.

**Returns:** JSON string containing the user's onboarding status.

#### `set_user_onboarding(onboarding_data: Dict[str, Any])`
Set the current user's onboarding status.

**Parameters:**
- `onboarding_data` (dict): The onboarding data to set.

**Returns:** JSON string containing the user's onboarding status.

#### `get_my_preferences()`
Get the current user's preferences.

**Returns:** JSON string containing the user's preferences.

#### `update_my_preferences(preferences_data: Dict[str, Any])`
Update the current user's preferences.

**Parameters:**
- `preferences_data` (dict): The preferences to update.

**Returns:** JSON string containing the updated preferences.

#### `delete_profile_image()`
Delete the current user's profile image.

**Returns:** JSON string containing the status of the operation.

#### `create_profile_image(file_path: str)`
Create a profile image for the current user.

**Parameters:**
- `file_path` (str): The path to the image file.

**Returns:** JSON string containing the response from the server.

#### `get_profile_image(user_id: str)`
Get a user's profile image.

**Parameters:**
- `user_id` (str): The ID of the user.

**Returns:** Base64 encoded profile image data.

### API Keys

#### `get_api_keys()`
Get all API keys.

**Returns:** JSON string containing a list of API keys.

#### `create_api_key(key_data: Dict[str, Any])`
Create a new API key.

**Parameters:**
- `key_data` (dict): The data for the new API key.

**Returns:** JSON string containing the created API key.

#### `get_api_key(key_id: str)`
Get an API key.

**Parameters:**
- `key_id` (str): The ID of the API key to retrieve.

**Returns:** JSON string containing the API key.

#### `update_api_key(key_id: str, key_data: Dict[str, Any])`
Update an API key.

**Parameters:**
- `key_id` (str): The ID of the API key to update.
- `key_data` (dict): The data to update the API key with.

**Returns:** JSON string containing the updated API key.

#### `delete_api_key(key_id: str)`
Delete an API key.

**Parameters:**
- `key_id` (str): The ID of the API key to delete.

**Returns:** JSON string containing the status of the operation.

### Authentication

#### `sign_up_admin(user_data: Dict[str, Any])`
Sign up a new admin user.

**Parameters:**
- `user_data` (dict): The data for the new admin user.

**Returns:** JSON string containing the created admin user.

#### `change_password(password_data: Dict[str, Any])`
Change the current user's password.

**Parameters:**
- `password_data` (dict): The data for changing the password.

**Returns:** JSON string containing the response from the server.

#### `login(login_data: Dict[str, Any])`
Log in a user.

**Parameters:**
- `login_data` (dict): The data for logging in.

**Returns:** JSON string containing the response from the server.

#### `logout()`
Log out the current user.

**Returns:** JSON string containing the response from the server.

#### `reset_pin_code(pin_code_data: Dict[str, Any])`
Reset the current user's pin code.

**Parameters:**
- `pin_code_data` (dict): The data for resetting the pin code.

**Returns:** JSON string containing the status of the operation.

#### `setup_pin_code(pin_code_data: Dict[str, Any])`
Set up a pin code for the current user.

**Parameters:**
- `pin_code_data` (dict): The data for setting up the pin code.

**Returns:** JSON string containing the status of the operation.

#### `change_pin_code(pin_code_data: Dict[str, Any])`
Change the current user's pin code.

**Parameters:**
- `pin_code_data` (dict): The data for changing the pin code.

**Returns:** JSON string containing the status of the operation.

#### `lock_auth_session()`
Lock the current user's authentication session.

**Returns:** JSON string containing the status of the operation.

#### `unlock_auth_session(unlock_data: Dict[str, Any])`
Unlock the current user's authentication session.

**Parameters:**
- `unlock_data` (dict): The data for unlocking the session.

**Returns:** JSON string containing the status of the operation.

#### `get_auth_status()`
Get the authentication status of the current user.

**Returns:** JSON string containing the authentication status.

#### `validate_access_token()`
Validate the current access token.

**Returns:** JSON string containing the validation status.

### Faces

#### `get_faces(asset_id: str)`
Get all faces for a given asset.

**Parameters:**
- `asset_id` (str): The ID of the asset.

**Returns:** JSON string containing a list of faces.

#### `create_face(face_data: Dict[str, Any])`
Create a new face.

**Parameters:**
- `face_data` (dict): The data for the new face.

**Returns:** JSON string containing the created face.

#### `delete_face(face_id: str)`
Delete a face.

**Parameters:**
- `face_id` (str): The ID of the face to delete.

**Returns:** JSON string containing the status of the operation.

#### `reassign_faces_by_id(face_id: str, person_id: str)`
Reassign a face to a person.

**Parameters:**
- `face_id` (str): The ID of the face to reassign.
- `person_id` (str): The ID of the person to reassign the face to.

**Returns:** JSON string containing the updated person.

### People

#### `create_person(person_data: Dict[str, Any])`
Create a new person.

**Parameters:**
- `person_data` (dict): The data for the new person.

**Returns:** JSON string containing the created person.

#### `update_people(people_data: Dict[str, Any])`
Update people.

**Parameters:**
- `people_data` (dict): The data for updating people.

**Returns:** JSON string containing the updated people.

#### `delete_people(people_data: Dict[str, Any])`
Delete people.

**Parameters:**
- `people_data` (dict): The data for deleting people.

**Returns:** JSON string containing the status of the operation.

#### `update_person(person_id: str, person_data: Dict[str, Any])`
Update a person.

**Parameters:**
- `person_id` (str): The ID of the person to update.
- `person_data` (dict): The data to update the person with.

**Returns:** JSON string containing the updated person.

#### `delete_person(person_id: str)`
Delete a person.

**Parameters:**
- `person_id` (str): The ID of the person to delete.

**Returns:** JSON string containing the status of the operation.

#### `merge_person(person_id: str, merge_data: Dict[str, Any])`
Merge a person.

**Parameters:**
- `person_id` (str): The ID of the person to merge.
- `merge_data` (dict): The data for merging the person.

**Returns:** JSON string containing the response from the server.

#### `reassign_faces(person_id: str, reassign_data: Dict[str, Any])`
Reassign faces to a person.

**Parameters:**
- `person_id` (str): The ID of the person to reassign faces to.
- `reassign_data` (dict): The data for reassigning faces.

**Returns:** JSON string containing the updated people.

### Shared Links

#### `get_all_shared_links()`
Get all shared links.

**Returns:** JSON string containing a list of shared links.

#### `create_shared_link(link_data: Dict[str, Any])`
Create a new shared link.

**Parameters:**
- `link_data` (dict): The data for the new shared link.

**Returns:** JSON string containing the created shared link.

#### `get_my_shared_link()`
Get the current user's shared link.

**Returns:** JSON string containing the current user's shared link.

#### `get_shared_link_by_id(link_id: str)`
Get a shared link by ID.

**Parameters:**
- `link_id` (str): The ID of the shared link to retrieve.

**Returns:** JSON string containing the shared link.

#### `remove_shared_link(link_id: str)`
Remove a shared link.

**Parameters:**
- `link_id` (str): The ID of the shared link to remove.

**Returns:** JSON string containing the status of the operation.

#### `update_shared_link(link_id: str, link_data: Dict[str, Any])`
Update a shared link.

**Parameters:**
- `link_id` (str): The ID of the shared link to update.
- `link_data` (dict): The data to update the shared link with.

**Returns:** JSON string containing the updated shared link.

#### `remove_shared_link_assets(link_id: str, asset_ids: List[str])`
Remove assets from a shared link.

**Parameters:**
- `link_id` (str): The ID of the shared link.
- `asset_ids` (list): The IDs of the assets to remove.

**Returns:** JSON string containing the response from the server.

#### `add_shared_link_assets(link_id: str, asset_ids: List[str])`
Add assets to a shared link.

**Parameters:**
- `link_id` (str): The ID of the shared link.
- `asset_ids` (list): The IDs of the assets to add.

**Returns:** JSON string containing the response from the server.

### API Endpoints

When running the server, you can access:

- **Interactive API Docs**: http://localhost:8626/docs
- **ReDoc Documentation**: http://localhost:8626/redoc
- **Health Check**: http://localhost:8626/health
