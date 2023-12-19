# ------- Litang Save The World! -------
#
# @Time    : 2023/12/5 20:36
# @Author  : Lynx
# @File    : test_for_mapping.py
#
from django.core.management import BaseCommand

from science.models import Works


class Command(BaseCommand):
    help = "test for model-document mapping"

    def add_arguments(self, parser):
        parser.add_argument("num")
    def handle(self, *args, **options):
        json_data = {
            'id': "111",
            'title': "title",
            'publication_date': work['publication_date'],
            'language': work['language'],
            'type': work['type'],
            'authors': authors,
            'cited_by_count': work['cited_by_count'],
            'biblio': work['biblio'],
            'keywords': work['keywords'],
            'concepts': concepts,
            'locations': locations,
            'referenced_works': referenced_works,
            'related_works': related_works,
            'abstract_inverted_index': work['abstract_inverted_index'],
            'counts_by_year': work['counts_by_year'],
            'updated_date': datetime.strptime(work['updated_date'], "%Y-%m-%dT%H:%M:%S.%f"),
            'created_date': datetime.strptime(work['created_date'], "%Y-%m-%d"),
        }
        Works.objects.create(**json_data)

