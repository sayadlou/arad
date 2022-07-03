import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

celery = Celery('config')
celery.config_from_object('config.settings.base', namespace='CELERY')
celery.autodiscover_tasks()
