# Generated by Django 4.2.7 on 2023-12-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0007_message_msg_type_message_work_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
