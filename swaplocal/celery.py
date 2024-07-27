import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swaplocal.settings')

app = Celery('swaplocal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
