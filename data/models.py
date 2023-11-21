from django.db import models


# Create your models here.

class ImportStatus(models.Model):
    work_page = models.IntegerField(default=1)
