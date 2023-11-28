"""
============================
# @Time    : 2023/11/28 19:15
# @Author  : Elaikona
# @FileName: works.py
===========================
"""

from rest_framework.decorators import api_view

from science.documents import WorkDocument
from science.models import Works
from science.request_serializers import SearchWorksSerializer
from science.serializers import WorksSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['GET'])
@validate_request(SearchWorksSerializer)
def search_work(request, serializer):
    title = serializer.validated_data['title']
    # result_works = Works.objects.filter(data__title__icontains=title).all()
    result = WorkDocument.search().query("match", title=title).to_queryset().all()
    return api_response(ErrorCode.SUCCESS, data=WorksSerializer(result, many=True).data)
