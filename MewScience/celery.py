# ------- Litang Save The World! -------
#
# @Time    : 2023/12/22 19:43
# @Author  : Lynx
# @File    : celery.py
#
# Create the Celery app
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MewScience.settings')

app = Celery('MewScience')
# Configure the broker and result backend
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'autosc': {
        'task': 'data.tasks.update_data',
        'schedule': crontab(),
    },
}