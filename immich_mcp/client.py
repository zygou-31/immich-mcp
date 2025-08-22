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

    async def get_all_shared_links(self) -> List[Dict[str, Any]]:
        """
        Get all shared links.

        Returns:
            List[Dict[str, Any]]: A list of shared links.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("shared-links")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def create_shared_link(self, link_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new shared link.

        Args:
            link_data: The data for the new shared link.

        Returns:
            Dict[str, Any]: The created shared link.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("shared-links")
            response = await client.post(
                url,
                headers=self.headers,
                json=link_data,
            )
            response.raise_for_status()
            return response.json()

    async def get_my_shared_link(self) -> Dict[str, Any]:
        """
        Get the current user's shared link.

        Returns:
            Dict[str, Any]: The current user's shared link.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("shared-links/me")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_shared_link_by_id(self, link_id: str) -> Dict[str, Any]:
        """
        Get a shared link by ID.

        Args:
            link_id: The ID of the shared link to retrieve.

        Returns:
            Dict[str, Any]: The shared link.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"shared-links/{link_id}")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def remove_shared_link(self, link_id: str) -> None:
        """
        Remove a shared link.

        Args:
            link_id: The ID of the shared link to remove.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"shared-links/{link_id}")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def update_shared_link(
        self, link_id: str, link_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a shared link.

        Args:
            link_id: The ID of the shared link to update.
            link_data: The data to update the shared link with.

        Returns:
            Dict[str, Any]: The updated shared link.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"shared-links/{link_id}")
            response = await client.patch(
                url,
                headers=self.headers,
                json=link_data,
            )
            response.raise_for_status()
            return response.json()

    async def remove_shared_link_assets(
        self, link_id: str, asset_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Remove assets from a shared link.

        Args:
            link_id: The ID of the shared link.
            asset_ids: The IDs of the assets to remove.

        Returns:
            List[Dict[str, Any]]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"shared-links/{link_id}/assets")
            response = await client.request(
                "DELETE",
                url,
                headers=self.headers,
                json={"ids": asset_ids},
            )
            response.raise_for_status()
            return response.json()

    async def add_shared_link_assets(
        self, link_id: str, asset_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Add assets to a shared link.

        Args:
            link_id: The ID of the shared link.
            asset_ids: The IDs of the assets to add.

        Returns:
            List[Dict[str, Any]]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"shared-links/{link_id}/assets")
            response = await client.put(
                url,
                headers=self.headers,
                json={"ids": asset_ids},
            )
            response.raise_for_status()
            return response.json()

    async def create_person(self, person_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new person.

        Args:
            person_data: The data for the new person.

        Returns:
            Dict[str, Any]: The created person.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("people")
            response = await client.post(
                url,
                headers=self.headers,
                json=person_data,
            )
            response.raise_for_status()
            return response.json()

    async def update_people(self, people_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Update people.

        Args:
            people_data: The data for updating people.

        Returns:
            List[Dict[str, Any]]: The updated people.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("people")
            response = await client.put(
                url,
                headers=self.headers,
                json=people_data,
            )
            response.raise_for_status()
            return response.json()

    async def delete_people(self, people_data: Dict[str, Any]) -> None:
        """
        Delete people.

        Args:
            people_data: The data for deleting people.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("people")
            response = await client.request(
                "DELETE",
                url,
                headers=self.headers,
                json=people_data,
            )
            response.raise_for_status()

    async def update_person(
        self, person_id: str, person_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a person.

        Args:
            person_id: The ID of the person to update.
            person_data: The data to update the person with.

        Returns:
            Dict[str, Any]: The updated person.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"people/{person_id}")
            response = await client.put(
                url,
                headers=self.headers,
                json=person_data,
            )
            response.raise_for_status()
            return response.json()

    async def delete_person(self, person_id: str) -> None:
        """
        Delete a person.

        Args:
            person_id: The ID of the person to delete.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"people/{person_id}")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def merge_person(
        self, person_id: str, merge_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Merge a person.

        Args:
            person_id: The ID of the person to merge.
            merge_data: The data for merging the person.

        Returns:
            List[Dict[str, Any]]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"people/{person_id}/merge")
            response = await client.post(
                url,
                headers=self.headers,
                json=merge_data,
            )
            response.raise_for_status()
            return response.json()

    async def reassign_faces(
        self, person_id: str, reassign_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Reassign faces to a person.

        Args:
            person_id: The ID of the person to reassign faces to.
            reassign_data: The data for reassigning faces.

        Returns:
            List[Dict[str, Any]]: The updated people.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"people/{person_id}/reassign")
            response = await client.put(
                url,
                headers=self.headers,
                json=reassign_data,
            )
            response.raise_for_status()
            return response.json()

    async def search_users(self) -> List[Dict[str, Any]]:
        """
        Search for users.

        Returns:
            List[Dict[str, Any]]: A list of users.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def sign_up_admin(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign up a new admin user.

        Args:
            user_data: The data for the new admin user.

        Returns:
            Dict[str, Any]: The created admin user.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/admin-sign-up")
            response = await client.post(
                url,
                headers=self.headers,
                json=user_data,
            )
            response.raise_for_status()
            return response.json()

    async def change_password(self, password_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Change the current user's password.

        Args:
            password_data: The data for changing the password.

        Returns:
            Dict[str, Any]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/change-password")
            response = await client.post(
                url,
                headers=self.headers,
                json=password_data,
            )
            response.raise_for_status()
            return response.json()

    async def login(self, login_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log in a user.

        Args:
            login_data: The data for logging in.

        Returns:
            Dict[str, Any]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/login")
            response = await client.post(
                url,
                headers=self.headers,
                json=login_data,
            )
            response.raise_for_status()
            return response.json()

    async def logout(self) -> Dict[str, Any]:
        """
        Log out the current user.

        Returns:
            Dict[str, Any]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/logout")
            response = await client.post(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def reset_pin_code(self, pin_code_data: Dict[str, Any]) -> None:
        """
        Reset the current user's pin code.

        Args:
            pin_code_data: The data for resetting the pin code.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/pin-code")
            response = await client.request(
                "DELETE",
                url,
                headers=self.headers,
                json=pin_code_data,
            )
            response.raise_for_status()

    async def setup_pin_code(self, pin_code_data: Dict[str, Any]) -> None:
        """
        Set up a pin code for the current user.

        Args:
            pin_code_data: The data for setting up the pin code.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/pin-code")
            response = await client.post(
                url,
                headers=self.headers,
                json=pin_code_data,
            )
            response.raise_for_status()

    async def change_pin_code(self, pin_code_data: Dict[str, Any]) -> None:
        """
        Change the current user's pin code.

        Args:
            pin_code_data: The data for changing the pin code.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/pin-code")
            response = await client.put(
                url,
                headers=self.headers,
                json=pin_code_data,
            )
            response.raise_for_status()

    async def lock_auth_session(self) -> None:
        """
        Lock the current user's authentication session.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/session/lock")
            response = await client.post(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def unlock_auth_session(self, unlock_data: Dict[str, Any]) -> None:
        """
        Unlock the current user's authentication session.

        Args:
            unlock_data: The data for unlocking the session.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/session/unlock")
            response = await client.post(
                url,
                headers=self.headers,
                json=unlock_data,
            )
            response.raise_for_status()

    async def get_auth_status(self) -> Dict[str, Any]:
        """
        Get the authentication status of the current user.

        Returns:
            Dict[str, Any]: The authentication status.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/status")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def validate_access_token(self) -> Dict[str, Any]:
        """
        Validate the current access token.

        Returns:
            Dict[str, Any]: The validation status.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("auth/validateToken")
            response = await client.post(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_faces(self, asset_id: str) -> List[Dict[str, Any]]:
        """
        Get all faces for a given asset.

        Args:
            asset_id: The ID of the asset.

        Returns:
            List[Dict[str, Any]]: A list of faces.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("faces")
            response = await client.get(
                url,
                headers=self.headers,
                params={"assetId": asset_id},
            )
            response.raise_for_status()
            return response.json()

    async def create_face(self, face_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new face.

        Args:
            face_data: The data for the new face.

        Returns:
            Dict[str, Any]: The created face.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("faces")
            response = await client.post(
                url,
                headers=self.headers,
                json=face_data,
            )
            response.raise_for_status()
            return response.json()

    async def delete_face(self, face_id: str) -> None:
        """
        Delete a face.

        Args:
            face_id: The ID of the face to delete.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"faces/{face_id}")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def reassign_faces_by_id(
        self, face_id: str, person_id: str
    ) -> Dict[str, Any]:
        """
        Reassign a face to a person.

        Args:
            face_id: The ID of the face to reassign.
            person_id: The ID of the person to reassign the face to.

        Returns:
            Dict[str, Any]: The updated person.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"faces/{face_id}")
            response = await client.put(
                url,
                headers=self.headers,
                json={"personId": person_id},
            )
            response.raise_for_status()
            return response.json()

    async def get_my_user(self) -> Dict[str, Any]:
        """
        Get the current user's information.

        Returns:
            Dict[str, Any]: The current user's information.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def update_my_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update the current user's information.

        Args:
            user_data: The data to update the user with.

        Returns:
            Dict[str, Any]: The updated user information.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me")
            response = await client.put(
                url,
                headers=self.headers,
                json=user_data,
            )
            response.raise_for_status()
            return response.json()

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get a user's information.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            Dict[str, Any]: The user's information.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"users/{user_id}")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def delete_user_license(self) -> None:
        """Delete the current user's license."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me/license")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def get_user_license(self) -> Dict[str, Any]:
        """Get the current user's license."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me/license")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def set_user_license(self, license_key: str) -> Dict[str, Any]:
        """
        Set the current user's license.

        Args:
            license_key: The license key to set.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me/license")
            response = await client.put(
                url,
                headers=self.headers,
                json={"licenseKey": license_key},
            )
            response.raise_for_status()
            return response.json()

    async def delete_user_onboarding(self) -> None:
        """Delete the current user's onboarding status."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me/onboarding")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def get_user_onboarding(self) -> Dict[str, Any]:
        """Get the current user's onboarding status."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me/onboarding")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def set_user_onboarding(
        self, onboarding_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Set the current user's onboarding status.

        Args:
            onboarding_data: The onboarding data to set.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me/onboarding")
            response = await client.put(
                url,
                headers=self.headers,
                json=onboarding_data,
            )
            response.raise_for_status()
            return response.json()

    async def get_my_preferences(self) -> Dict[str, Any]:
        """Get the current user's preferences."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me/preferences")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def update_my_preferences(
        self, preferences_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update the current user's preferences.

        Args:
            preferences_data: The preferences to update.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/me/preferences")
            response = await client.put(
                url,
                headers=self.headers,
                json=preferences_data,
            )
            response.raise_for_status()
            return response.json()

    async def delete_profile_image(self) -> None:
        """Delete the current user's profile image."""
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/profile-image")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def create_profile_image(self, file_path: str) -> Dict[str, Any]:
        """
        Create a profile image for the current user.

        Args:
            file_path: The path to the image file.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("users/profile-image")
            with open(file_path, "rb") as f:
                response = await client.post(
                    url,
                    headers=self.headers,
                    files={"file": f},
                )
            response.raise_for_status()
            return response.json()

    async def get_profile_image(self, user_id: str) -> bytes:
        """
        Get a user's profile image.

        Args:
            user_id: The ID of the user.

        Returns:
            The profile image as bytes.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"users/{user_id}/profile-image")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.content

    async def get_api_keys(self) -> List[Dict[str, Any]]:
        """
        Get all API keys.

        Returns:
            List[Dict[str, Any]]: A list of API keys.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("api-keys")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def create_api_key(self, key_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new API key.

        Args:
            key_data: The data for the new API key.

        Returns:
            Dict[str, Any]: The created API key.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("api-keys")
            response = await client.post(
                url,
                headers=self.headers,
                json=key_data,
            )
            response.raise_for_status()
            return response.json()

    async def get_api_key(self, key_id: str) -> Dict[str, Any]:
        """
        Get an API key.

        Args:
            key_id: The ID of the API key to retrieve.

        Returns:
            Dict[str, Any]: The API key.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"api-keys/{key_id}")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def update_api_key(
        self, key_id: str, key_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an API key.

        Args:
            key_id: The ID of the API key to update.
            key_data: The data to update the API key with.

        Returns:
            Dict[str, Any]: The updated API key.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"api-keys/{key_id}")
            response = await client.put(
                url,
                headers=self.headers,
                json=key_data,
            )
            response.raise_for_status()
            return response.json()

    async def delete_api_key(self, key_id: str) -> None:
        """
        Delete an API key.

        Args:
            key_id: The ID of the API key to delete.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"api-keys/{key_id}")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def search_users_admin(
        self, user_id: Optional[str] = None, with_deleted: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for users with admin privileges.

        Args:
            user_id: The ID of the user to search for.
            with_deleted: Whether to include deleted users in the results.

        Returns:
            List[Dict[str, Any]]: A list of users matching the search criteria.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {}
            if user_id is not None:
                params["id"] = user_id
            if with_deleted is not None:
                params["withDeleted"] = with_deleted
            url = self._get_url("admin/users")
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def create_user_admin(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user with admin privileges.

        Args:
            user_data: The data for the new user.

        Returns:
            Dict[str, Any]: The created user.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("admin/users")
            response = await client.post(
                url,
                headers=self.headers,
                json=user_data,
            )
            response.raise_for_status()
            return response.json()

    async def get_user_admin(self, user_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific user with admin privileges.

        Args:
            user_id: The unique identifier of the user to retrieve.

        Returns:
            Dict[str, Any]: User object containing comprehensive information.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"admin/users/{user_id}")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def update_user_admin(
        self, user_id: str, user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a user with admin privileges.

        Args:
            user_id: The ID of the user to update.
            user_data: The data to update the user with.

        Returns:
            Dict[str, Any]: The updated user.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"admin/users/{user_id}")
            response = await client.put(
                url,
                headers=self.headers,
                json=user_data,
            )
            response.raise_for_status()
            return response.json()

    async def delete_user_admin(
        self, user_id: str, force: bool = False
    ) -> Dict[str, Any]:
        """
        Delete a user with admin privileges.

        Args:
            user_id: The ID of the user to delete.
            force: Whether to force the deletion.

        Returns:
            Dict[str, Any]: The deleted user.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"admin/users/{user_id}")
            response = await client.request(
                "DELETE",
                url,
                headers=self.headers,
                json={"force": force},
            )
            response.raise_for_status()
            return response.json()

    async def get_user_preferences_admin(self, user_id: str) -> Dict[str, Any]:
        """
        Get preferences for a specific user with admin privileges.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            Dict[str, Any]: The user's preferences.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"admin/users/{user_id}/preferences")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def update_user_preferences_admin(
        self, user_id: str, preferences_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update preferences for a specific user with admin privileges.

        Args:
            user_id: The ID of the user.
            preferences_data: The data to update the preferences with.

        Returns:
            Dict[str, Any]: The updated preferences.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"admin/users/{user_id}/preferences")
            response = await client.put(
                url,
                headers=self.headers,
                json=preferences_data,
            )
            response.raise_for_status()
            return response.json()

    async def restore_user_admin(self, user_id: str) -> Dict[str, Any]:
        """
        Restore a deleted user with admin privileges.

        Args:
            user_id: The ID of the user to restore.

        Returns:
            Dict[str, Any]: The restored user.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"admin/users/{user_id}/restore")
            response = await client.post(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_user_statistics_admin(
        self,
        user_id: str,
        is_favorite: Optional[bool] = None,
        is_trashed: Optional[bool] = None,
        visibility: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get statistics for a specific user with admin privileges.

        Args:
            user_id: The unique identifier of the user.
            is_favorite: Whether to filter by favorite status.
            is_trashed: Whether to filter by trashed status.
            visibility: The visibility of the assets.

        Returns:
            Dict[str, Any]: The user's statistics.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {}
            if is_favorite is not None:
                params["isFavorite"] = is_favorite
            if is_trashed is not None:
                params["isTrashed"] = is_trashed
            if visibility is not None:
                params["visibility"] = visibility
            url = self._get_url(f"admin/users/{user_id}/statistics")
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def search_memories(
        self,
        for_date: Optional[str] = None,
        is_saved: Optional[bool] = None,
        is_trashed: Optional[bool] = None,
        memory_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for memories.

        Args:
            for_date: The date to search for memories for.
            is_saved: Whether to search for saved memories.
            is_trashed: Whether to search for trashed memories.
            memory_type: The type of memory to search for.

        Returns:
            List[Dict[str, Any]]: A list of memories.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {}
            if for_date is not None:
                params["for"] = for_date
            if is_saved is not None:
                params["isSaved"] = is_saved
            if is_trashed is not None:
                params["isTrashed"] = is_trashed
            if memory_type is not None:
                params["type"] = memory_type
            url = self._get_url("memories")
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def create_memory(self, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new memory.

        Args:
            memory_data: The data for the new memory.

        Returns:
            Dict[str, Any]: The created memory.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url("memories")
            response = await client.post(
                url,
                headers=self.headers,
                json=memory_data,
            )
            response.raise_for_status()
            return response.json()

    async def get_memory_statistics(
        self,
        for_date: Optional[str] = None,
        is_saved: Optional[bool] = None,
        is_trashed: Optional[bool] = None,
        memory_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get memory statistics.

        Args:
            for_date: The date to get statistics for.
            is_saved: Whether to get statistics for saved memories.
            is_trashed: Whether to get statistics for trashed memories.
            memory_type: The type of memory to get statistics for.

        Returns:
            Dict[str, Any]: The memory statistics.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            params = {}
            if for_date is not None:
                params["for"] = for_date
            if is_saved is not None:
                params["isSaved"] = is_saved
            if is_trashed is not None:
                params["isTrashed"] = is_trashed
            if memory_type is not None:
                params["type"] = memory_type
            url = self._get_url("memories/statistics")
            response = await client.get(
                url,
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return response.json()

    async def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """
        Get a specific memory.

        Args:
            memory_id: The ID of the memory.

        Returns:
            Dict[str, Any]: The memory.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"memories/{memory_id}")
            response = await client.get(
                url,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def update_memory(
        self, memory_id: str, memory_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a memory.

        Args:
            memory_id: The ID of the memory.
            memory_data: The data to update the memory with.

        Returns:
            Dict[str, Any]: The updated memory.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"memories/{memory_id}")
            response = await client.put(
                url,
                headers=self.headers,
                json=memory_data,
            )
            response.raise_for_status()
            return response.json()

    async def delete_memory(self, memory_id: str) -> None:
        """
        Delete a memory.

        Args:
            memory_id: The ID of the memory.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"memories/{memory_id}")
            response = await client.delete(
                url,
                headers=self.headers,
            )
            response.raise_for_status()

    async def add_memory_assets(
        self, memory_id: str, asset_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Add assets to a memory.

        Args:
            memory_id: The ID of the memory.
            asset_ids: The IDs of the assets to add.

        Returns:
            List[Dict[str, Any]]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"memories/{memory_id}/assets")
            response = await client.put(
                url,
                headers=self.headers,
                json={"ids": asset_ids},
            )
            response.raise_for_status()
            return response.json()

    async def remove_memory_assets(
        self, memory_id: str, asset_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Remove assets from a memory.

        Args:
            memory_id: The ID of the memory.
            asset_ids: The IDs of the assets to remove.

        Returns:
            List[Dict[str, Any]]: The response from the server.
        """
        async with httpx.AsyncClient(timeout=10) as client:
            url = self._get_url(f"memories/{memory_id}/assets")
            response = await client.request(
                "DELETE",
                url,
                headers=self.headers,
                json={"ids": asset_ids},
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
