import json
from django.core.management.base import BaseCommand

from additional.models import Reward


class Command(BaseCommand):
    help = 'Inserts patent data using bulk_create'

    def handle(self, *args, **options):
        data = []
        with open("D:\\output1.txt", "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                j = json.loads(line)
                data.append(Reward(title=j["zhTitle"],
                                   authors=j["authors"],
                                   year=int(j["publishYear"]),
                                   award_institution=j["issuedBy"]))
        Reward.objects.bulk_create(data)
        print("Success")
