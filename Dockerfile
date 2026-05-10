FROM python:3.12.3-slim

# Prevent Python from writing .pyc files + ensure logs show in real time
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# System dependencies (needed for some pip packages like boto3/httpx builds)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project
COPY . .

ENV AWS_REGION=ap-southeast-2

# Run ingestion service
CMD ["python", "main.py"]