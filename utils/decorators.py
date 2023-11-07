"""
============================
# @Time    : 2023/11/6 16:22
# @Author  : Elaikona
# @FileName: decorators.py
===========================
"""
from functools import wraps

from utils.error_code import ErrorCode
from utils.response_util import api_response


def validate_request(serializer_class):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                return view_func(request, serializer=serializer, *args, **kwargs)
            else:
                return api_response(ErrorCode.INVALID_DATA, "invalid data")

        return wrapped_view

    return decorator
