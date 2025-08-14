# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project's dependency file and install dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Copy the rest of the application's source code from the host to the image's filesystem
COPY . .

# Inform Docker that the container is listening on port 8000
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
