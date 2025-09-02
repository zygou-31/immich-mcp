# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install uv, which will be used to install the package
RUN pip install uv

# Copy the source distribution from the build job
COPY dist/*.tar.gz ./app.tar.gz

# Install the package from the source distribution
# This also installs the runtime dependencies.
RUN uv pip install --system --no-cache ./app.tar.gz

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
# The package is installed in site-packages, so uvicorn can find it.
CMD ["uvicorn", "immich_mcp.main:app", "--host", "0.0.0.0", "--port", "8000"]
