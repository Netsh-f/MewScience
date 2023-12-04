# ------- Litang Save The World! -------
#
# @Time    : 2023/11/28 19:54
# @Author  : Lynx
# @File    : documents.py
#

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from science.models import Works


@registry.register_document
class WorkDocument(Document):
    language = fields.KeywordField()
    type = fields.KeywordField()
    authors = fields.NestedField(
        properties={
            'id': fields.KeywordField(),
            'display_name': fields.TextField(),
            'orcid': fields.KeywordField(),
        }
    )

    class Index:
        name = 'work'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Works
        fields = [
            "id",
            "title",
            "publication_date",
        ]
