# Generated by Django 4.2.7 on 2023-11-28 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("science", "0002_alter_works_updated_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="works",
            name="abstract_inverted_index",
            field=models.JSONField(null=True),
        ),
    ]
