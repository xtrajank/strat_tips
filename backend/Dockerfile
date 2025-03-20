# Use an official Python runtime as base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y npm

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app files
COPY . .

# Install frontend dependencies and build React
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Serve React build inside FastAPI
WORKDIR /app
RUN pip install uvicorn fastapi

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
