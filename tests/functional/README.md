# Functional Tests

## Purpose

This directory contains a script for running functional tests against a live Immich instance. These tests are kept separate from the unit tests because they require a running server and valid API credentials.

## Running the Tests

The functional tests are executed via the `run_functional_tests.py` Python script.

### Prerequisites

- A running Immich instance.
- `curl` and `jq` must be installed and available in your `PATH`.
- A Python virtual environment with the project's `dev` dependencies installed (`pip install -e ".[dev]"`).

### Configuration

The test script requires the following environment variables to be set:

- `IMMICH_BASE_URL`: The base URL of your Immich instance (e.g., `http://immich.local:2283`). The script and server will handle appending the necessary `/api` path.
- `IMMICH_API_KEY`: A valid API key for your Immich instance.

### Execution

To run the tests, execute the following command from the root of the repository:

```bash
.venv/bin/python tests/functional/run_functional_tests.py
```

### What is Tested?

The script starts the MCP server in the background and then uses an MCP client to perform the following actions:

1.  **`ping`**: Pings the MCP server, which in turn pings the real Immich server.
2.  **`user://me`**: Fetches the current user's details.
3.  **`users://list`**: Fetches the list of all users.
4.  **`partners://list`**: Fetches the list of partners.
5.  **`apikey://me`**: Fetches the details of the current API key.
6.  **`apikeys://list` and `apikey://{id}`**: Fetches the list of all API keys, then uses the ID of the first key to fetch its details individually.

The script will print the results of each test and exit with a non-zero status code if any test fails.
