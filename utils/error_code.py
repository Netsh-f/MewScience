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
    INVALID_DATA = 1001
    NOT_LOGGED_IN = 1002
    PERMISSION_DENIED = 1003
    # map all the error that available data can't be found in es
    ELASTIC_ERROR = 1004

    # file
    FILE_NOT_EXIST = 2001
    FILE_TYPE_INVALID = 2002
    FILE_TOO_LARGE = 2003

    # account
    USERNAME_ALREADY_EXISTS = 10001
    WRONG_USERNAME_OR_PASSWORD = 10002

    # portal
    ALREADY_CLAIM_PORTAL = 20001
    APPLICATION_NOT_FOUND = 20002
