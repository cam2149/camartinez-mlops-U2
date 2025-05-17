FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY app/ app/

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install requirements
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000


CMD ["python", "application.py"]