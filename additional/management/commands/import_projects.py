import zlib
import json

from django.core.management.base import BaseCommand
from additional.models import Project


class Command(BaseCommand):
    help = 'Inserts project data using bulk_create'

    def handle(self, *args, **options):
        data = []
        with open("D:\\output1.txt", "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                j = json.loads(line)
                data.append(Project(id=int(j["ratifyNo"]), title=j["projectName"], application_code=j["code"],
                                    authors=json.loads('{}'), supporting_units=j["dependUnit"], funds=float(j["supportNum"]),
                                    abstract_c=j['projectAbstractC'],
                                    abstract_e=j['projectAbstractE']))
        Project.objects.bulk_create(data)
        print("Success")
