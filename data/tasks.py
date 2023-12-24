# ------- Litang Save The World! -------
#
# @Time    : 2023/12/23 18:18
# @Author  : Lynx
# @File    : tasks.py
#
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone


@shared_task
def update_data():
    last_beat_time = cache.get('last_beat_time')
    current_time = timezone.now()
    cache.set('last_beat_time', current_time)