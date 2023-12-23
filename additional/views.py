from rest_framework.decorators import api_view

from additional.request_serializers import ProjectSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['POST'])
@validate_request(ProjectSerializer)
def get_project(request, serializer):
    return api_response(ErrorCode.SUCCESS, serializer.validated_data)
