from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Message(models.Model):
    class MsgType(models.IntegerChoices):
        CLAIM_REVIEW = 0, # available research_id
        FOLLOW_UPDATE = 1,
        WORKS_TRANSFER = 2,
        TRANSFER_RESPONSE = 3, # available research_id

    class WorkType(models.IntegerChoices):
        PATENT = 0,
        PROJECT = 1,
        REWARD = 2,

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # set a special value for admin message
    research_id = models.BigIntegerField(default=-1)
    link_content = models.CharField(max_length=255, null=True)
    link_id = models.BigIntegerField(null=True)
    msg_type = models.IntegerField(choices=MsgType, default=1)
    work_type = models.IntegerField(choices=WorkType, null=True)
