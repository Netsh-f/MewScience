# ------- Litang Save The World! -------
#
# @Time    : 2023/12/20 23:55
# @Author  : Lynx
# @File    : file_validator.py
#
from enum import Enum
class FileType(Enum):
    IMAGE = 1
    AUDIO = 2

EXTENSIONS = {
    FileType.IMAGE: ['.jpg', '.jpeg', '.png', '.svg'],
    FileType.AUDIO: ['.mp3', '.wav', '.flac'],
}
def validate_file_type(filename: str, mode: FileType = None) -> bool:
    if mode is None:
        return True
    extensions = EXTENSIONS[mode]
    for ext in extensions:
        if filename.endswith(ext):
            return True
    return False