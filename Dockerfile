# Dockerfile for Patient-Care Flask app
FROM python:3.11-slim

# Install a few OS deps (psycopg2, others may need build tools; minimize size)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy app source
COPY . /app

# Expose Flask port
EXPOSE 5000

# Ensure database file is created in /app (volume mapped) on first run
# Use gunicorn to run the app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app", "--workers", "1", "--threads", "4"]
