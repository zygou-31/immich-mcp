import requests
import json
import os
import time

IMMICH_URL = os.environ.get("IMMICH_URL", "http://localhost:2283")
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "password"


def main():
    # 1. Sign up admin user
    print("Creating admin user...")
    try:
        r = requests.post(
            f"{IMMICH_URL}/api/auth/sign-up-admin",
            json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD,
                "name": "Admin",
            },
        )
        r.raise_for_status()
        print("Admin user created.")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 and "already exists" in e.response.text:
            print("Admin user already exists.")
        else:
            raise

    # 2. Login as admin
    print("Logging in as admin...")
    r = requests.post(
        f"{IMMICH_URL}/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    r.raise_for_status()
    access_token = r.json()["accessToken"]
    print("Logged in successfully.")

    # 3. Create API key
    print("Creating API key...")
    r = requests.post(
        f"{IMMICH_URL}/api/api-key",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "test-key", "permissions": ["all"]},
    )
    r.raise_for_status()
    api_key = r.json()["secret"]
    print("API key created.")

    # 4. Print API key
    print(f"::set-output name=api-key::{api_key}")


if __name__ == "__main__":
    main()
