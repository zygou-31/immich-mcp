import asyncio
import httpx
import os
import subprocess
import time
import uuid
from pathlib import Path

IMMICH_URL = os.environ.get("IMMICH_URL", "http://localhost:2283")
API_KEY = os.environ["IMMICH_API_KEY"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
MCP_URL = "http://localhost:8626"
PICTURES_DIR = Path("data/pictures")

headers = {"x-api-key": API_KEY, "Accept": "application/json"}


async def upload_asset(session, image_path: Path):
    """Uploads a single asset to Immich."""
    device_asset_id = f"test-asset-{image_path.name}-{uuid.uuid4()}"
    device_id = "test-device"
    file_created_at = datetime.fromtimestamp(image_path.stat().st_mtime).isoformat()
    file_modified_at = datetime.fromtimestamp(image_path.stat().st_mtime).isoformat()

    with open(image_path, "rb") as f:
        files = {
            "assetData": (image_path.name, f, "image/jpeg"),
            "deviceAssetId": (None, device_asset_id),
            "deviceId": (None, device_id),
            "fileCreatedAt": (None, file_created_at),
            "fileModifiedAt": (None, file_modified_at),
            "isFavorite": (None, "false"),
        }
        print(f"Uploading {image_path.name}...")
        response = await session.post(
            f"{IMMICH_URL}/api/asset/upload", headers=headers, files=files
        )
        response.raise_for_status()
        return response.json()["id"]


async def main():
    # 1. Start mcp-immich server
    print("Starting mcp-immich server...")
    server_process = subprocess.Popen(["immich-mcp"])
    time.sleep(5)  # Give it a moment to start

    # 2. Wait for mcp-immich to be healthy
    async with httpx.AsyncClient() as client:
        for _ in range(20):
            try:
                response = await client.get(f"{MCP_URL}/health")
                if response.status_code == 200:
                    print("mcp-immich server is healthy.")
                    break
            except httpx.ConnectError:
                print("Waiting for mcp-immich server...")
                await asyncio.sleep(2)
        else:
            raise Exception("mcp-immich server did not become healthy in time.")

    # 3. Upload images
    async with httpx.AsyncClient(timeout=30) as session:
        image_paths = list(PICTURES_DIR.glob("*.jpg"))
        asset_ids = await asyncio.gather(
            *[upload_asset(session, path) for path in image_paths]
        )
        print(f"Uploaded {len(asset_ids)} assets.")

    # 4. Trigger jobs
    print("Triggering jobs...")
    async with httpx.AsyncClient(timeout=30) as client:
        # Regenerate thumbnails
        response = await client.post(
            f"{IMMICH_URL}/api/assets/jobs",
            headers=headers,
            json={"name": "regenerate-thumbnail", "assetIds": asset_ids},
        )
        response.raise_for_status()
        print("Thumbnail regeneration job triggered.")

        # Refresh metadata and faces
        response = await client.post(
            f"{IMMICH_URL}/api/assets/jobs",
            headers=headers,
            json={"name": "refresh-metadata", "assetIds": asset_ids},
        )
        response.raise_for_status()
        print("Metadata and faces refresh job triggered.")

    # 5. Wait for jobs to complete
    print("Waiting for jobs to complete...")
    async with httpx.AsyncClient(timeout=300) as client:
        while True:
            response = await client.get(f"{IMMICH_URL}/api/jobs", headers=headers)
            response.raise_for_status()
            jobs_status = response.json()
            pending_jobs = (
                jobs_status["thumbnailGeneration"]["pending"]
                + jobs_status["metadataExtraction"]["pending"]
                + jobs_status["faceDetection"]["pending"]
                + jobs_status["facialRecognition"]["pending"]
                + jobs_status["smartSearch"]["pending"]
            )
            if pending_jobs == 0:
                print("All jobs completed.")
                break
            print(f"Waiting for {pending_jobs} jobs to complete...")
            await asyncio.sleep(10)

    # 6. Run assertions
    print("Running assertions...")
    async with httpx.AsyncClient() as client:
        mcp_headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = await client.post(
            f"{MCP_URL}/search/metadata",
            headers=mcp_headers,
            json={},
        )
        response.raise_for_status()
        results = response.json()
        assert (
            len(results["assets"]) >= 10
        ), f"Expected at least 10 assets, but found {len(results['assets'])}"
        print("Assertion passed: Found at least 10 assets.")

    print("Functional tests passed!")

    # 7. Stop mcp-immich server
    server_process.terminate()


if __name__ == "__main__":
    from datetime import datetime
    import asyncio
    asyncio.run(main())
