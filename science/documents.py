# ------- Litang Save The World! -------
#
# @Time    : 2023/11/28 19:54
# @Author  : Lynx
# @File    : documents.py
#

from elasticsearch_dsl import Index
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from MewScience.document import mewScience


@registry.register_document
@mewScience.document
class WorkDocument(Document):
    class Index:
        title = fields.TextField(attr="get_work_title")