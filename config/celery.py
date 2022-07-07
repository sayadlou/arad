from celery import Celery

celery = Celery('config')
celery.config_from_object('config.settings.celery', namespace='CELERY')
celery.autodiscover_tasks()
