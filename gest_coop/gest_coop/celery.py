# gest_coop/celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gest_coop.settings')

app = Celery('gest_coop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
