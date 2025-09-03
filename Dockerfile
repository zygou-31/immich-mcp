# syntax=docker/dockerfile:1
FROM python:3.13-slim

ARG PACKAGE

# Copy the prebuilt package tarball into the container
COPY ${PACKAGE} /tmp/package.tar.gz

# Install dependencies and package
RUN apt-get update && apt-get install -y --no-install-recommends \
    && pip install --no-cache-dir /tmp/package.tar.gz \
    && rm /tmp/package.tar.gz \
    && rm -rf /var/lib/apt/lists/*

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "immich_mcp.main:app", "--host", "0.0.0.0", "--port", "8000"]
