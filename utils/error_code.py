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

    # global
    INVALID_DATA = 10001

    # account
    USERNAME_ALREADY_EXISTS = 20001
    WRONG_USERNAME_OR_PASSWORD = 20002
