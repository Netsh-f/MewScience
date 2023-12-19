"""
============================
# @Time    : 2023/11/28 19:15
# @Author  : Elaikona
# @FileName: works.py
===========================
"""
from rest_framework.decorators import api_view

from science.request_serializers import SearchWorksSerializer
from utils.decorators import validate_request


@api_view(['GET'])
@validate_request(SearchWorksSerializer)
def search_work(request, serializer):
    pass
