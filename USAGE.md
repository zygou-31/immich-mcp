# 🚀 Usage

### Starting the Server

Once installed, you can start the server with the following command:

```bash
immich-mcp
```

This will start the server on `http://0.0.0.0:8626`.

You can also run the server in stdio mode:

```bash
immich-mcp --mode stdio
```

For development, you can use `uvicorn` for auto-reloading:

```bash
uvicorn immich_mcp.cli:app --host 0.0.0.0 --port 8626 --reload
```

### Docker

This project includes a `Dockerfile` and `docker-compose.yml` for easy containerization.

#### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (if using `docker-compose.yml`)

#### Building the Docker Image

To build the Docker image, run the following command from the project root:

```bash
docker build -t immich-mcp .
```

#### Running with Docker

You can run the container using `docker run`. You'll need to provide the required environment variables.

```bash
docker run -d \
  --name immich-mcp-container \
  -p 8626:8626 \
  -e IMMICH_BASE_URL="https://your-immich-server.com" \
  -e IMMICH_API_KEY="your-immich-api-key" \
  -e AUTH_TOKEN="your-secret-auth-token" \
  -e MCP_PORT="8626" \
  -e MCP_BASE_URL="/mcp" \
  immich-mcp
```

*Note: `MCP_PORT` and `MCP_BASE_URL` are optional.*

#### Running with Docker Compose

For a more streamlined experience, you can use Docker Compose.

1.  **Create a `.env` file:**

    Copy the `.env.example` to `.env` and fill in your Immich server details.

    ```bash
    cp .env.example .env
    ```

    Your `.env` file should look like this:

    ```
    IMMICH_BASE_URL=https://your-immich-server.com
    IMMICH_API_KEY=your-api-key-here
    AUTH_TOKEN=your-secret-auth-token-here
    ```

2.  **Start the service:**

    Run the following command to build and start the service in detached mode:

    ```bash
    docker-compose up --build -d
    ```

3.  **Stopping the service:**

    To stop the service, run:

    ```bash
    docker-compose down
    ```

For more detailed usage examples, see [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md).
