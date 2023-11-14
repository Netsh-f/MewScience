from django.db import models


# Create your models here.

class Work(models.Model):
    data = models.JSONField()
