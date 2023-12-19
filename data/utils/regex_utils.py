"""
============================
# @Time    : 2023/11/21 20:07
# @Author  : Elaikona
# @FileName: regex_utils.py
===========================
"""
import re


def get_id(openalex_id):
    if openalex_id == None:
        return None
    return re.search(r'\d+$', openalex_id).group()
