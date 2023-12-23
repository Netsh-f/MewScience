import json
from django.core.management.base import BaseCommand

from additional.models import Patent


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
                data.append(Patent(number=j["patentNo"],
                                   authors=j["authors"],
                                   title=j["zhTitle"],
                                   year=int(j["publishYear"]),
                                   authorized_institutions=j["issuingUnit"]))
        Patent.objects.bulk_create(data)
        print("Success")
