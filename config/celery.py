import os

from celery import Celery

celery = Celery('config')
celery.config_from_object(os.environ.get('DJANGO_SETTINGS_MODULE'), namespace='CELERY')
celery.autodiscover_tasks()
