from rest_framework.decorators import api_view

from account.request_serializers import RegisterSerializer
from utils.decorators import validate_request
from utils.error_code import ErrorCode
from utils.response_util import api_response


@api_view(['POST'])
@validate_request(RegisterSerializer)
def register(request, serializer):
    serializer.create(serializer.validated_data)
    return api_response(ErrorCode.SUCCESS, "success")
