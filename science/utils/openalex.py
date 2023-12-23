"""
============================
# @Time    : 2023/12/23 15:44
# @Author  : Elaikona
# @FileName: openalex.py
===========================
"""
import requests

openalex_url = "https://api.openalex.org"
openalex_works_url = openalex_url + "/works/W"


def get_work_from_openalex(id):
    url = openalex_works_url + str(id)
    response = requests.get(url)
    return response.json()
