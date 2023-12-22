"""
============================
# @Time    : 2023/12/20 21:58
# @Author  : Elaikona
# @FileName: institutions.py
===========================
"""
from rest_framework.decorators import api_view

from MewScience.settings import ES
from science.request_serializers import GetInstitutionSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['GET'])
@validate_request(GetInstitutionSerializer)
def get_institution(request, serializer):
    id = serializer.validated_data.get('id')
    result = ES.get(index='institutions', id=id)
    return api_response(ErrorCode.SUCCESS, result['_source'])
