FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for PostGIS and GeoDjango
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    postgresql \
    postgresql-contrib \
    postgresql-12-postgis-3 \
    libpq-dev \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python dependencies
COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --default-timeout=1000 -r requirements.txt

COPY . .

# Start Flower
CMD ["celery", "-A", "core", "flower", "--port=5555", "--loglevel=info", "--scheduler", "django_celery_beat.schedulers:DatabaseScheduler"]
