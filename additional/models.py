from django.db import models
from rest_framework import serializers


class Patent(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    authors = models.TextField()
    authors_r = models.JSONField(default=dict)
    year = models.IntegerField()
    number = models.CharField(max_length=32, default='')
    authorized_institutions = models.CharField(max_length=128, default='')


class Reward(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    authors = models.TextField()
    authors_r = models.JSONField(default=dict)
    year = models.IntegerField()
    award_institution = models.CharField(max_length=128, default='')


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=128)
    application_code = models.CharField(max_length=10)
    authors = models.TextField()
    authors_r = models.JSONField(default=dict)
    supporting_units = models.CharField(max_length=128)
    funds = models.FloatField()
    abstract_c = models.TextField()
    abstract_e = models.TextField()
    children_r = models.ManyToManyField(Reward)
    children_p = models.ManyToManyField(Patent)


class PatentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patent
        exclude = ['authors_r']


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        exclude = ['authors_r']


class ProjectOutputSerializer(serializers.ModelSerializer):
    children_p = PatentSerializer(many=True)
    children_r = RewardSerializer(many=True)

    class Meta:
        model = Project
        exclude = ['authors_r']


class PatentOutputSerializer(serializers.ModelSerializer):
    projects = ProjectOutputSerializer(source='project_set', many=True, read_only=True)

    class Meta:
        model = Patent
        exclude = ['authors_r']


class RewardOutputSerializer(serializers.ModelSerializer):
    projects = ProjectOutputSerializer(source='project_set', many=True, read_only=True)

    class Meta:
        model = Reward
        exclude = ['authors_r']
