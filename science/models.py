from django.db import models


# Create your models here.

class Works(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    language = models.CharField(max_length=2, null=True)
    type = models.CharField(max_length=32)
    authors = models.JSONField()
    cited_by_count = models.IntegerField()
    biblio = models.JSONField()
    keywords = models.JSONField()
    concepts = models.JSONField()
    locations = models.JSONField()
    referenced_works = models.JSONField()
    related_works = models.JSONField()
    abstract_inverted_index = models.JSONField(null=True)
    counts_by_year = models.JSONField()
    updated_date = models.DateTimeField()
    created_date = models.DateField()


class Authors(models.Model):
    data = models.JSONField()


class Sources(models.Model):
    data = models.JSONField()


class Institutions(models.Model):
    data = models.JSONField()


class Concepts(models.Model):
    data = models.JSONField()
