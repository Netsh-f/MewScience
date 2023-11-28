# ------- Litang Save The World! -------
#
# @Time    : 2023/11/14 21:41
# @Author  : Lynx
# @File    : document.py
#
from elasticsearch_dsl import Index

mewScience = Index('MewScience')
mewScience.settings(
    number_of_shards=1,
    number_of_replicas=0
)