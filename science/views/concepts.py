"""
============================
# @Time    : 2023/12/22 21:01
# @Author  : Elaikona
# @FileName: concepts.py
===========================
"""
from rest_framework.decorators import api_view

from MewScience.settings import ES
from science.request_serializers import IdSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['GET'])
@validate_request(IdSerializer)
def get_concept(request, serializer):
    id = serializer.validated_data.get('id')
    result = ES.get(index='concepts', id=id)
    return api_response(ErrorCode.SUCCESS, result['_source'])
