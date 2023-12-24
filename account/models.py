from django.contrib.auth.models import User
from django.db import models
from typing import List, Tuple

default_intro = '暂无简介'
class UserProfile(models.Model):
    class Identify(models.IntegerChoices):
        NORMAL = 0,
        ADMIN = 1,

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identity = models.PositiveSmallIntegerField(choices=Identify.choices, default=Identify.NORMAL)
    researcher_id = models.BigIntegerField(null=True)
    follow_list = models.JSONField(default=dict)
    intro = models.TextField(default=default_intro)
