"""
============================
# @Time    : 2023/11/21 19:35
# @Author  : Elaikona
# @FileName: import_works.py
===========================
"""
import logging
import time

import requests
from django.core.management.base import BaseCommand

from data.models import ImportStatus
from data.utils.regex_utils import get_id
from science.models import Works


class Command(BaseCommand):
    help = 'script to import works from openalex'

    def add_arguments(self, parser):
        parser.add_argument('num')

    def handle(self, *args, **options):
        num = options.get("num")
        import_status = ImportStatus.objects.all().first()
        start_page = import_status.work_page
        for i in range(start_page, start_page + int(num)):
            start_time = time.time()
            api = f"https://api.openalex.org/works?per-page=200&page={i}"
            response_json = requests.get(api).json()
            for work in response_json['results']:
                if work['is_retracted'] or work['is_paratext']:  # 被撤回 or 为副文本
                    continue
                authors = []
                for authorship in work['authorships']:
                    author = authorship['author']
                    authors.append({
                        'id': get_id(author['id']),
                        'display_name': author['display_name'],
                        'orcid': author['orcid'],
                    })
                concepts = []
                for concept in work['concepts']:
                    concepts.append({
                        'id': get_id(concept['id']),
                        'display_name': concept['display_name'],
                        'score': concept['score'],
                    })
                locations = []
                for location in work['locations']:
                    source = location['source']
                    if source is None:
                        continue
                    locations.append({
                        'is_oa': location['is_oa'],
                        'landing_page_url': location['landing_page_url'],
                        'pdf_url': location['pdf_url'],
                        'source': {
                            'id': get_id(source['id']),
                            'display_name': source['display_name'],
                        },
                        'license': location['license'],
                        'version': location['version'],
                        'is_accepted': location['is_accepted'],
                        'is_published': location['is_published'],
                    })
                referenced_works = []
                for referenced_work in work['referenced_works']:
                    referenced_works.append(get_id(referenced_work))
                related_works = []
                for related_work in work['related_works']:
                    related_works.append(get_id(related_work))
                json_data = {
                    'id': get_id(work['id']),
                    'title': work['title'],
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
                    'updated_date': work['updated_date'],
                    'created_date': work['created_date'],
                }
                Works.objects.create(data=json_data)
            end_time = time.time()
            print(f"page {i} import successfully, using {end_time - start_time}s.")
        import_status.work_page = start_page + int(num)
        import_status.save()
