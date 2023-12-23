from django.db import models


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    application_code = models.CharField(max_length=10)
    authors = models.JSONField()
    supporting_units = models.CharField(max_length=128)
    funds = models.FloatField()
    abstract_c = models.BinaryField()
    abstract_e = models.BinaryField()


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