# Generated by Django 4.2.7 on 2023-12-23 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('additional', '0003_alter_patent_title_alter_reward_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patent',
            name='title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='reward',
            name='title',
            field=models.TextField(),
        ),
    ]