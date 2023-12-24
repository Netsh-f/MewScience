import json
from django.core.management.base import BaseCommand

from additional.models import Reward


class Command(BaseCommand):
    help = 'Inserts patent data using bulk_create'

    def handle(self, *args, **options):
        data = []
        reward_author = {}
        with open("D:\\reward_author", "r", encoding="utf-8") as f:
            for line in f:
                j = json.loads(line)
                for key in j.keys():
                    reward_author[key] = [int(i) for i in j[key]]
        line_count = 0
        with open("D:\\reward_result.txt", "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                j = json.loads(line)
                line_count += 1
                lc = str(line_count)
                if lc in reward_author:
                    authors_r = reward_author[lc]
                else:
                    print("Miss")
                    authors_r = []
                data.append(Reward(id=j['reward_id'],
                                   title=j["zhTitle"],
                                   authors=j["authors"],
                                   authors_r=authors_r,
                                   year=int(j["publishYear"]),
                                   award_institution=j["issuedBy"]))
        Reward.objects.bulk_create(data)
        print("Success")
