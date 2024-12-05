#!/bin/bash
celery -A core flower --port=5555 --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
