"""
============================
# @Time    : 2023/11/6 15:50
# @Author  : Elaikona
# @FileName: error_code.py
===========================
"""
from enum import Enum


class ErrorCode(Enum):
    SUCCESS = 0
    FAILED = -1

    INVALID_DATA = 10001
