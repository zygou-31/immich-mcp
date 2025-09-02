import asyncio
import json
import os
import subprocess
import sys
import time

from pydantic_ai.mcp import MCPServerStreamableHTTP


async def main():
    """
    Main function to run the functional tests using the pydantic-ai client.
    This is the final, final version.
    """
    api_url = os.environ.get("IMMICH_BASE_URL")
    api_key = os.environ.get("IMMICH_API_KEY")

    if not api_url or not api_key:
        print("Error: IMMICH_BASE_URL and IMMICH_API_KEY must be set.", file=sys.stderr)
        sys.exit(1)

    server_host = "127.0.0.1"
    server_port = 8765
    server_address = f"http://{server_host}:{server_port}/mcp"

    server_command = [
        "python",
        "-m",
        "uvicorn",
        "src.immich_mcp.main:app",
        "--host",
        server_host,
        "--port",
        str(server_port),
    ]

    print("Starting server...")
    server_process = subprocess.Popen(
        server_command,
        stdout=sys.stdout,
        stderr=sys.stderr,
        env={**os.environ, "PYTHONPATH": "src"},
    )

    try:
        # Give the server time to start up
        time.sleep(10)

        # Create an MCP client server instance
        server = MCPServerStreamableHTTP(url=server_address)

        async with server:
            print("Client session initialized.")

            client_session = server._client

            # --- Run Tests ---
            print("\n--- Testing ping ---")
            ping_result = await client_session.call_tool("ping", {})
            ping_text = ping_result.content[0].text
            print(f"Response: {ping_text}")
            assert ping_text == "pong", f"Ping failed: {ping_text}"
            print("PASS: Ping successful.")

            print("\n--- Testing user://me ---")
            user_result = await client_session.read_resource("user://me")
            user = json.loads(user_result.contents[0].text)
            print(f"Response: {user}")
            assert user.get("id"), "User response did not contain an ID."
            print(f"PASS: Got user with ID: {user['id']}")

            print("\n--- Testing users://list ---")
            users_list_result = await client_session.read_resource("users://list")
            users_list = json.loads(users_list_result.contents[0].text)
            print(f"Response: {users_list}")
            assert isinstance(users_list, list) and len(users_list) > 0, "Did not get a valid list of users."
            print(f"PASS: Got a list of {len(users_list)} users.")

            print("\n--- Testing partners://list ---")
            partners_list_result = await client_session.read_resource("partners://list")
            partners_list = json.loads(partners_list_result.contents[0].text)
            print(f"Response: {partners_list}")
            assert isinstance(partners_list, list), "Partners list was not a valid list."
            print(f"PASS: Got a list of {len(partners_list)} partners.")

            print("\n--- Testing apikey://me ---")
            my_api_key_result = await client_session.read_resource("apikey://me")
            my_api_key = json.loads(my_api_key_result.contents[0].text)
            print(f"Response: {my_api_key}")
            assert my_api_key.get("id"), "My API key response did not contain an ID."
            print(f"PASS: Got current API key with ID: {my_api_key['id']}")

            print("\n--- Testing apikeys://list and apikey://{id} ---")
            api_keys_list_result = await client_session.read_resource("apikeys://list")
            api_keys_list = json.loads(api_keys_list_result.contents[0].text)
            print(f"List Response: {api_keys_list}")
            assert isinstance(api_keys_list, list) and len(api_keys_list) > 0, (
                "Did not get a valid list of API keys."
            )

            first_key_id = api_keys_list[0].get("id")
            assert first_key_id, "First API key in list has no ID."
            print(f"Found API key ID to test: {first_key_id}")

            specific_key_result = await client_session.read_resource(f"apikey://{first_key_id}")
            specific_key = json.loads(specific_key_result.contents[0].text)
            print(f"Specific Key Response: {specific_key}")
            assert specific_key.get("id") == first_key_id, "Fetched specific key ID does not match."
            print(f"PASS: Successfully fetched specific API key with ID: {first_key_id}")

        print("\nAll functional tests passed!")

    except Exception as e:
        print(f"\nAn error occurred during testing: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        print("\nCleaning up and stopping the server...")
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")


if __name__ == "__main__":
    asyncio.run(main())
