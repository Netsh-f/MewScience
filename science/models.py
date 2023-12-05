from django.db import models


# Create your models here.

class Works(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=511, null=True)
    publication_date = models.DateField(null=True)
    language = models.CharField(max_length=2, null=True)
    type = models.CharField(max_length=32, null=True)
    authors = models.JSONField(null=True)
    cited_by_count = models.IntegerField(null=True)
    biblio = models.JSONField(null=True)
    keywords = models.JSONField(null=True)
    x_concepts = models.JSONField(null=True)
    locations = models.JSONField(null=True)
    referenced_works = models.JSONField(null=True)
    related_works = models.JSONField(null=True)
    abstract_inverted_index = models.JSONField(null=True)
    counts_by_year = models.JSONField(null=True)
    updated_date = models.DateTimeField(null=True)
    created_date = models.DateField(null=True)



class Authors(models.Model):
    id = models.BigIntegerField(primary_key=True)
    orcid = models.CharField(max_length=64, null=True)
    display_name = models.CharField(max_length=128, null=True)
    works_count = models.IntegerField(null=True)
    cited_by_count = models.IntegerField(null=True)
    summary_stats = models.JSONField(null=True)
    last_known_institution = models.JSONField(null=True)
    concepts = models.JSONField(null=True)
    counts_by_year = models.JSONField(null=True)
    updated_date = models.DateTimeField(null=True)
    created_date = models.DateField(null=True)



class Sources(models.Model):
    id = models.BigIntegerField(primary_key=True)
    display_name = models.CharField(max_length=255, null=True)
    host_organization = models.BigIntegerField(null=True)
    host_organization_name = models.CharField(max_length=255, null=True)
    works_count = models.IntegerField(null=True)
    cited_by_count = models.IntegerField(null=True)
    summary_stats = models.JSONField(null=True)
    homepage_url = models.URLField(max_length=512, null=True)
    country_code = models.CharField(max_length=2, null=True)
    type = models.CharField(max_length=32, null=True)
    x_concepts = models.JSONField(null=True)
    counts_by_year = models.JSONField(null=True)
    updated_date = models.DateTimeField(null=True)
    created_date = models.DateField(null=True)



class Institutions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ror = models.URLField(max_length=255, null=True)
    display_name = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=2, null=True)
    type = models.CharField(max_length=32, null=True)
    homepage_url = models.URLField(max_length=512, null=True)
    image_url = models.URLField(max_length=512, null=True)
    works_count = models.IntegerField(null=True)
    cited_by_count = models.IntegerField(null=True)
    summary_stats = models.JSONField(null=True)
    geo = models.JSONField(null=True)
    associated_institutions = models.JSONField(null=True)
    counts_by_year = models.JSONField(null=True)
    x_concepts = models.JSONField(null=True)
    updated_date = models.DateTimeField(null=True)
    created_date = models.DateField(null=True)


class Concepts(models.Model):
    id = models.BigIntegerField(primary_key=True)
    display_name = models.CharField(max_length=255, null=True)
    level = models.SmallIntegerField(null=True)
    description = models.TextField(null=True)
    works_count = models.IntegerField(null=True)
    cited_by_count = models.IntegerField(null=True)
    summary_stats = models.JSONField(null=True)
    image_url = models.URLField(max_length=512, null=True)
    ancestors = models.JSONField(null=True)
    related_concepts = models.JSONField(null=True)
    counts_by_year = models.JSONField(null=True)
    updated_date = models.DateTimeField(null=True)
    created_date = models.DateField(null=True)
