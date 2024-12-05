import os
import sys
from celery import Celery
from celery.exceptions import TimeoutError

app = Celery('core')

if __name__ == "__main__":
    try:
        # Ping Celery worker to check its liveness
        response = app.control.ping(timeout=10)
        if not response:
            raise TimeoutError("No response from Celery worker")
        sys.exit(0)
    except Exception as e:
        print(f"Celery worker liveness check failed: {e}")
        sys.exit(1)
