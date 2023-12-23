import zlib

from django.db import models
from rest_framework import serializers


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    application_code = models.CharField(max_length=10)
    authors = models.JSONField()
    supporting_units = models.CharField(max_length=128)
    funds = models.FloatField()
    abstract_c = models.TextField()
    abstract_e = models.TextField()


class ProjectOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['authors']


class Patent(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, default='')
    authors = models.TextField()
    authors_r = models.JSONField(default=dict)
    year = models.IntegerField()
    number = models.CharField(max_length=32, default='')
    authorized_institutions = models.CharField(max_length=128, default='')


class PatentOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patent
        exclude = ['authors_r', 'id']


class Reward(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, default='')
    authors = models.TextField()
    authors_r = models.JSONField(default=dict)
    year = models.IntegerField()
    award_institution = models.CharField(max_length=128, default='')


class RewardOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        exclude = ['authors_r', 'id']