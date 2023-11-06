"""
============================
# @Time    : 2023/11/6 15:55
# @Author  : Elaikona
# @FileName: response_util.py
===========================
"""
from rest_framework.response import Response

from rest_framework import status

from utils.error_code import ErrorCode


def api_response(errno: ErrorCode, msg: str, data=None) -> Response:
    if data is None:
        data = {}
    return Response({"errno": errno.value, "msg": msg, "data": data}, status=status.HTTP_200_OK)
