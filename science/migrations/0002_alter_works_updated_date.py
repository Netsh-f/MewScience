# Generated by Django 4.2.7 on 2023-11-28 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("science", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="works",
            name="updated_date",
            field=models.DateTimeField(),
        ),
    ]
