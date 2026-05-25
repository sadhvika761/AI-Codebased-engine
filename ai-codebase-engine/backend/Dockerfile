FROM python:3.11-slim

WORKDIR /app

# Install git for cloning repositories and curl for the Docker healthcheck
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We need the config from root
COPY config.py /app/config.py
COPY backend/ /app/backend/

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
