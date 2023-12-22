from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Message(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # set a special value for admin message
    research_id = models.IntegerField(default=-1)
    research_name = models.CharField(max_length=127, null=True)
