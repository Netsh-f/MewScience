import pymysql as pymysql

from .celery import app

pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()

__all__ = ('app')
