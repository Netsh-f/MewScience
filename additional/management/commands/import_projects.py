import zlib
import json

from django.core.management.base import BaseCommand
from additional.models import Project


class Command(BaseCommand):
    help = 'Inserts project data using bulk_create'

    def handle(self, *args, **options):
        data = []
        project_authors = {}
        with open("D:\\author", "r", encoding="utf-8") as f:
            for line in f:
                j = json.loads(line)
                for key in j.keys():
                    project_authors[key] = [int(i) for i in j[key]]
        with open("D:\\output1.txt", "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if len(line) == 0:
                    break
                j = json.loads(line)
                authors = ""
                for par in j["participatantsList"]:
                    authors += par['result'][1] + ";"
                data.append(Project(id=int(j["ratifyNo"]), title=j["projectName"], application_code=j["code"],
                                    authors=authors,
                                    authors_r=json.dumps(project_authors[j["ratifyNo"]]), supporting_units=j["dependUnit"], funds=float(j["supportNum"]),
                                    abstract_c=j['projectAbstractC'],
                                    abstract_e=j['projectAbstractE']))
        Project.objects.bulk_create(data)
        print("Success")
