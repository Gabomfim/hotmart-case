# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install system dependencies for ChromaDB and FastAPI
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for FastAPI
EXPOSE 8002

# Command to start the QueryAPI FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
