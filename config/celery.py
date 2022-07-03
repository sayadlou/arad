import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

celery = Celery('config')
celery.config_from_object(settings, namespace='CELERY')
celery.autodiscover_tasks()
