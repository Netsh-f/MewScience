# Generated by Django 4.2.7 on 2023-12-05 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Authors",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("orcid", models.CharField(max_length=64, null=True)),
                ("display_name", models.CharField(max_length=128, null=True)),
                ("works_count", models.IntegerField(null=True)),
                ("cited_by_count", models.IntegerField(null=True)),
                ("summary_stats", models.JSONField(null=True)),
                ("last_known_institution", models.JSONField(null=True)),
                ("concepts", models.JSONField(null=True)),
                ("counts_by_year", models.JSONField(null=True)),
                ("updated_date", models.DateTimeField(null=True)),
                ("created_date", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Concepts",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("display_name", models.CharField(max_length=255, null=True)),
                ("level", models.SmallIntegerField(null=True)),
                ("description", models.TextField(null=True)),
                ("works_count", models.IntegerField(null=True)),
                ("cited_by_count", models.IntegerField(null=True)),
                ("summary_stats", models.JSONField(null=True)),
                ("image_url", models.URLField(max_length=255, null=True)),
                ("ancestors", models.JSONField(null=True)),
                ("related_concepts", models.JSONField(null=True)),
                ("counts_by_year", models.JSONField(null=True)),
                ("updated_date", models.DateTimeField(null=True)),
                ("created_date", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Institutions",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("ror", models.URLField(max_length=255, null=True)),
                ("display_name", models.CharField(max_length=255, null=True)),
                ("country_code", models.CharField(max_length=2, null=True)),
                ("type", models.CharField(max_length=32, null=True)),
                ("homepage_url", models.URLField(max_length=255, null=True)),
                ("image_url", models.URLField(max_length=255, null=True)),
                ("works_count", models.IntegerField(null=True)),
                ("cited_by_count", models.IntegerField(null=True)),
                ("summary_stats", models.JSONField(null=True)),
                ("geo", models.JSONField(null=True)),
                ("associated_institutions", models.JSONField(null=True)),
                ("counts_by_year", models.JSONField(null=True)),
                ("x_concepts", models.JSONField(null=True)),
                ("updated_date", models.DateTimeField(null=True)),
                ("created_date", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Sources",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("display_name", models.CharField(max_length=255, null=True)),
                ("host_organization", models.BigIntegerField(null=True)),
                ("host_organization_name", models.CharField(max_length=255, null=True)),
                ("works_count", models.IntegerField(null=True)),
                ("cited_by_count", models.IntegerField(null=True)),
                ("summary_stats", models.JSONField(null=True)),
                ("homepage_url", models.URLField(max_length=255, null=True)),
                ("country_code", models.CharField(max_length=2, null=True)),
                ("type", models.CharField(max_length=32, null=True)),
                ("x_concepts", models.JSONField(null=True)),
                ("counts_by_year", models.JSONField(null=True)),
                ("updated_date", models.DateTimeField(null=True)),
                ("created_date", models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Works",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=511, null=True)),
                ("publication_date", models.DateField(null=True)),
                ("language", models.CharField(max_length=2, null=True)),
                ("type", models.CharField(max_length=32, null=True)),
                ("authors", models.JSONField(null=True)),
                ("cited_by_count", models.IntegerField(null=True)),
                ("biblio", models.JSONField(null=True)),
                ("keywords", models.JSONField(null=True)),
                ("x_concepts", models.JSONField(null=True)),
                ("locations", models.JSONField(null=True)),
                ("referenced_works", models.JSONField(null=True)),
                ("related_works", models.JSONField(null=True)),
                ("abstract_inverted_index", models.JSONField(null=True)),
                ("counts_by_year", models.JSONField(null=True)),
                ("updated_date", models.DateTimeField(null=True)),
                ("created_date", models.DateField(null=True)),
            ],
        ),
    ]
