# ------- Litang Save The World! -------
#
# @Time    : 2023/12/20 23:49
# @Author  : Lynx
# @File    : file_check.py
#
from django.core.files.uploadedfile import UploadedFile

from utils.error_code import ErrorCode
from utils.file_validator import validate_file_type, FileType


def file_check(file: UploadedFile, maxsize: int, type: FileType = None):
    if file is None:
        return False, ErrorCode.FILE_NOT_EXIST
    elif not validate_file_type(file.name, type):
        return False, ErrorCode.FILE_TYPE_INVALID
    elif file.size > maxsize:
        return False, ErrorCode.FILE_TOO_LARGE
    return True, file