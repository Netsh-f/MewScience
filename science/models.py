from django.db import models


# Create your models here.

class Works(models.Model):
    data = models.JSONField()
    def get_work_title(self):
        return self.data.get("title", "")


class Authors(models.Model):
    data = models.JSONField()


class Sources(models.Model):
    data = models.JSONField()


class Institutions(models.Model):
    data = models.JSONField()


class Concepts(models.Model):
    data = models.JSONField()
