# ------- Litang Save The World! -------
#
# @Time    : 2023/11/14 21:41
# @Author  : Lynx
# @File    : document.py
#
from elasticsearch_dsl import Index

# The name of your index
mewScience = Index('MewScience')
# See Elasticsearch Indices API reference for available settings
mewScience.settings(
    number_of_shards=1,
    number_of_replicas=0
)