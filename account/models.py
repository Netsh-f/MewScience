from django.contrib.auth.models import User
from django.db import models
from typing import List, Tuple


class UserProfile(models.Model):
    class Identify(models.IntegerChoices):
        NORMAL = 0,
        ADMIN = 1,

    def add_follow_list(self, research_id: str, research_name: str):
        if self.follow_list == None:
            self.follow_list = f"[{research_id},{research_name}]"
        else:
            self.follow_list = self.follow_list.join(f",[{research_id},{research_name}]")

    def get_follow_list(self) -> List[Tuple[str, ...]]:
        if self.follow_list is None:
            return []
        else:
            follow_list = self.follow_list[1:-1]
            research_list = follow_list.split('],[')
            result = [tuple(item.split(',')) for item in research_list]
            return result

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identity = models.PositiveSmallIntegerField(choices=Identify.choices, default=Identify.NORMAL)
    researcher_id = models.BigIntegerField(null=True)
    follow_list = models.TextField(null=True)
