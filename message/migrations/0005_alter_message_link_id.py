# Generated by Django 4.2.7 on 2023-12-23 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_remove_message_research_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='link_id',
            field=models.BigIntegerField(null=True),
        ),
    ]