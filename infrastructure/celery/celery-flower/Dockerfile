FROM python:3.12-slim

WORKDIR /app

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
