"""
============================
# @Time    : 2023/12/22 19:31
# @Author  : Elaikona
# @FileName: update_works.py
===========================
"""
import json

from django.core.management import BaseCommand

from MewScience.settings import ES


class Command(BaseCommand):
    def handle(self, *args, **options):
        script = """SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");"""
        query = {
            "script": {
                "script": {
                    "source": """
                            doc["publication_date"].value.year < 100
                        """,
                    "lang": "painless",
                }
            }
        }
        body = {
            "query": query,
            "script": script,
        }
        response = ES.update_by_query(index='works', body=body)
        formatted_response = json.dumps(response, indent=2)
        print(formatted_response)
