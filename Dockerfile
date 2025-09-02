# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy files required for installation
COPY pyproject.toml README.md LICENSE ./
COPY src ./src

# Install uv and then the project dependencies
RUN pip install uv
RUN uv pip install --system --no-cache .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["uvicorn", "immich_mcp.main:app", "--host", "0.0.0.0", "--port", "8000"]
