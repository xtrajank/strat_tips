# Use Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy backend files
COPY backend /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose backend port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
