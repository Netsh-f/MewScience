from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    class Identify(models.IntegerChoices):
        NORMAL = 0,
        ADMIN = 1,

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identity = models.PositiveSmallIntegerField(choices=Identify.choices, default=Identify.NORMAL)
    researcher_id = models.BigIntegerField(null=True)
