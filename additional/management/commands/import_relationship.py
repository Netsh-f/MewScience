import json
from django.core.management.base import BaseCommand

from additional.models import Reward, Project, Patent


class Command(BaseCommand):
    help = 'Inserts patent data using bulk_create'

    def handle(self, *args, **options):
        with open("D:\\project_to_patent.txt", "r", encoding="utf-8") as f:
            project_to_patent = json.loads(f.readline())
        for project_no, patent_list in project_to_patent.items():
            project = Project.objects.get(id=int(project_no))
            for patent_no in patent_list:
                patent = Patent.objects.get(number=patent_no)
                project.children_p.add(patent)
        with open("D:\\project_to_reward.txt", "r", encoding="utf-8") as f:
            project_to_reward = json.loads(f.readline())
        for project_no, reward_list in project_to_reward.items():
            project = Project.objects.get(id=int(project_no))
            for reward_no in reward_list:
                reward = Reward.objects.get(id=int(reward_no))
                project.children_r.add(reward)
        print("Success")
