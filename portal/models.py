from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Application(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0,
        PASSED = 1,
        FAILED = 2,

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    research_id = models.BigIntegerField()
    status = models.IntegerField(choices=Status.choices, default=Status.PENDING)
    creat_time = models.DateTimeField(auto_now_add=True)
    audit_time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1023)
    file = models.CharField(max_length=255)
