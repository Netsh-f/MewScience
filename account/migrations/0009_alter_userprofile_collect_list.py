# Generated by Django 4.2.7 on 2023-12-25 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_alter_userprofile_collect_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="collect_list",
            field=models.JSONField(default=dict),
        ),
    ]