# Generated by Django 4.2.7 on 2023-11-28 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("science", "0003_alter_works_abstract_inverted_index"),
    ]

    operations = [
        migrations.AlterField(
            model_name="works",
            name="language",
            field=models.CharField(max_length=2, null=True),
        ),
    ]
