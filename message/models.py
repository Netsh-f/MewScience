from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Message(models.Model):
    class MsgType(models.IntegerChoices):
        CLAIM_REVIEW = 0, 'Claim Review'# available research_id
        FOLLOW_UPDATE = 1, 'Follow Update'
        WORKS_TRANSFER = 2, 'Works Transfer'
        TRANSFER_RESPONSE = 3, 'Transfer Response' # available research_id

    class WorkType(models.IntegerChoices):
        PATENT = 0, 'Patent'
        PROJECT = 1, 'Project'
        REWARD = 2, 'Reward'

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # set a special value for admin message
    research_id = models.BigIntegerField(default=-1)
    link_content = models.CharField(max_length=255, null=True)
    link_id = models.BigIntegerField(null=True)
    msg_type = models.IntegerField(choices=MsgType.choices, default=1)
    work_type = models.IntegerField(choices=WorkType.choices, null=True)
