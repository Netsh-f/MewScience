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
    USER_NOT_EXIST = 10003
    WORK_NOT_FOUND = 10004

    # portal
    ALREADY_CLAIM_PORTAL = 20001
    APPLICATION_NOT_FOUND = 20002
    ALREADY_FOLLOWED = 20003

    # transfer
    TRANSFEREE_NOT_REGISTERED = 30001
    PATENT_NOT_FOUND = 30002
    PROJECT_NOT_FOUND = 30003
    REWARD_NOT_FOUND = 30004

    # message
    MSG_NOT_FOUND = 40001
