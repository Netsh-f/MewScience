from django.db import models


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    application_code = models.CharField(max_length=8)
    authors = models.JSONField()
    supporting_units = models.CharField(max_length=64)
    funds = models.FloatField()
    abstract = models.CharField(max_length=1024)
    url = models.CharField(max_length=128)


class Patent(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    authors = models.JSONField()
    year = models.IntegerField()


class Reward(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    authors = models.JSONField()
    year = models.IntegerField()
    award_institution = models.CharField(max_length=64)