# 🚀 Deployment

### Production Deployment

#### Using Docker

```bash
# Build production image
docker build -t immich-mcp:latest .

# Run with production settings
docker run -d \
  --name immich-mcp \
  -p 8626:8626 \
  -e IMMICH_BASE_URL=https://your-immich-server.com \
  -e IMMICH_API_KEY=your-api-key \
  -e MCP_PORT="8626" \
  --restart unless-stopped \
  immich-mcp:latest
```

#### Using systemd

Create `/etc/systemd/system/immich-mcp.service`:

```ini
[Unit]
Description=Immich MCP Server
After=network.target

[Service]
Type=exec
User=immich-mcp
WorkingDirectory=/opt/immich-mcp
Environment=IMMICH_BASE_URL=https://your-immich-server.com
Environment=IMMICH_API_KEY=your-api-key
ExecStart=/opt/immich-mcp/venv/bin/python -m immich_mcp.server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable immich-mcp
sudo systemctl start immich-mcp
```

### Reverse Proxy Setup

If you want to run the Immich MCP server behind a reverse proxy under a subpath (e.g., `https://your-domain.com/mcp`), you can use the `MCP_BASE_URL` environment variable.

Set `MCP_BASE_URL` to the desired subpath, for example, `/mcp`.

#### Docker Compose with Caddy

Here's an example of how to use it with Caddy as a reverse proxy in a `docker-compose.yml` file.

1.  **Update your `.env` file:**

    Add `MCP_BASE_URL` to your `.env` file:

    ```
    IMMICH_BASE_URL=https://your-immich-server.com
    IMMICH_API_KEY=your-api-key-here
    MCP_PORT=8626
    MCP_BASE_URL=/mcp
    ```

2.  **Update your `docker-compose.yml`:**

    Add a Caddy service to your `docker-compose.yml` and make sure both services are on the same network.

    ```yaml
    version: '3.8'

    services:
      immich-mcp:
        build: .
        env_file: .env
        restart: unless-stopped
        networks:
          - mcp-net

      caddy:
        image: caddy:2-alpine
        restart: unless-stopped
        ports:
          - "80:80"
          - "443:443"
        volumes:
          - ./Caddyfile:/etc/caddy/Caddyfile
          - caddy_data:/data
          - caddy_config:/config
        networks:
          - mcp-net

    networks:
      mcp-net:

    volumes:
      caddy_data:
      caddy_config:
    ```

3.  **Create a `Caddyfile`:**

    Create a file named `Caddyfile` in the same directory with the following content:

    ```
    your-domain.com {
        handle_path /mcp/* {
            reverse_proxy immich-mcp:8626 {
                header_up Host {host}
                header_up X-Real-IP {remote_ip}
                header_up X-Forwarded-For {remote_ip}
                header_up X-Forwarded-Proto {scheme}
            }
        }

        # Other services you might be running
    }
    ```

With this setup, the Immich MCP server will be available at `https://your-domain.com/mcp`, and the API documentation will be correctly served at `https://your-domain.com/mcp/docs`.

### Environment-Specific Configuration

#### Development
```bash
# .env.development
IMMICH_BASE_URL=http://localhost:2283
IMMICH_API_KEY=dev-key
IMMICH_TIMEOUT=60
```

#### Production
```bash
# .env.production
IMMICH_BASE_URL=https://immich.yourdomain.com
IMMICH_API_KEY=production-key
IMMICH_TIMEOUT=30
```

## CI/CD

This project uses GitHub Actions for CI/CD. The workflow is defined in `.github/workflows/ci.yml` and includes the following jobs:

### Lint & Test

This job runs on every push and pull request to the `main` branch. It performs the following checks:
- Lints the code with `ruff`.
- Checks code formatting with `black`.
- Runs the test suite with `pytest` against multiple Python versions.

### Publish to Docker Hub

This job runs automatically when a new release is created on GitHub. It builds the Docker image and publishes it to [Docker Hub](https://hub.docker.com/r/zygou/immich-mcp).

The image is tagged with the release version (e.g., `v1.0.0`) and `latest`.

#### Configuring Secrets

To allow the workflow to publish to your Docker Hub repository, you need to configure the following secrets in your GitHub repository settings under `Settings` > `Secrets and variables` > `Actions`:

- `DOCKERHUB_USERNAME`: Your Docker Hub username.
- `DOCKERHUB_TOKEN`: A Docker Hub Personal Access Token (PAT) with read/write permissions.
