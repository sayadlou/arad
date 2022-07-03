import os

from celery import Celery
from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

celery = Celery('config')
celery.config_from_object('config.settings.celery', namespace='CELERY')
celery.autodiscover_tasks()
