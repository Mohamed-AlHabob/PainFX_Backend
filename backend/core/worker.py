import logging

logging.basicConfig(level=logging.INFO)

from core.celery import app as celery_app

if __name__ == '__main__':
    logging.info("Starting Celery worker...")
    celery_app.start()
