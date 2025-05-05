# Running Flask-MVC PDF API with Docker and ngrok

This notebook sets up and runs the Flask-MVC PDF Embed/Extract API using Docker and exposes it through ngrok.

## 1. Setup and Dependencies

First, let's install the necessary dependencies:

```python
# Install Docker
!apt-get update
!apt-get install -y apt-transport-https ca-certificates curl software-properties-common
!curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
!add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
!apt-get update
!apt-get install -y docker-ce docker-compose
!docker --version
!docker-compose --version
```

## 2. Install ngrok

```python
# Install ngrok
!pip install pyngrok
!ngrok -v
```

## 3. Clone the Repository

```python
# Clone the repository
!git clone https://github.com/yahiaAlg/flask_mvc_api.git
%cd flask_mvc_api
```

## 4. Create Required Files

Let's create the Dockerfile:

```python
%%writefile Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

Create docker-compose.yml:

```python
%%writefile docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_APP=run.py
      - FLASK_ENV=production
    restart: unless-stopped
```

Update requirements.txt:

```python
%%writefile requirements.txt
flask>=2.0.0
PyPDF2>=3.0.0
flasgger>=0.9.5
pytest>=7.0.0
gunicorn>=20.1.0
```

## 5. Build and Run with Docker Compose

```python
# Build and start the containers
!docker-compose build
!docker-compose up -d
```

## 6. Setup ngrok and Expose the Service

```python
# Import and configure ngrok
from pyngrok import ngrok
import time

# Wait for the Flask app to fully start
time.sleep(5)

# Create a tunnel to the Flask app
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")
```

## 7. Monitor Docker Logs

```python
# Show logs from the running container
!docker-compose logs
```

## 8. Accessing the Application

```python
# Display information about accessing the app
print("\n=== Flask-MVC PDF API Access Information ===")
print(f"Web Interface: {public_url}")
print(f"API Documentation: {public_url}/apidocs/")
print(f"Embed PDFs Endpoint: {public_url}/api/pdf/create_embedded_pdf")
print(f"Extract PDFs Endpoint: {public_url}/api/pdf/extract_embedded_pdf")
```

## 9. Stop the Service

Run this cell when you want to stop the service:

```python
# Stop the Docker containers
!docker-compose down

# Stop ngrok tunnels
ngrok.kill()
```
