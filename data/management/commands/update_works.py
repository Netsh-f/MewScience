"""
============================
# @Time    : 2023/12/22 19:31
# @Author  : Elaikona
# @FileName: update_works.py
===========================
"""
import json
import logging
import subprocess
from datetime import datetime, timedelta, date

from django.core.management import BaseCommand

logger = logging.getLogger('__name__')


def get_yesterday_date():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def check_and_download_data(updated_date):
    s3_ls_command = f'aws s3 ls --summarize --human-readable --no-sign-request --recursive "s3://openalex/data/works/updated_date={updated_date}"'
    download_command = f'aws s3 sync "s3://openalex/data/works/updated_date={updated_date}" "/data/openalex-snapshot/data/works/updated_date={updated_date}" --no-sign-request'
    date_str = updated_date.strftime("%Y-%m-%d")
    import_script_command = f'python manage.py import_works --month={date_str.split("-")[1]} --day1={date_str.split("-")[2]} --day2={date_str.split("-")[2]}'
    try:
        ls_output = subprocess.check_output(s3_ls_command, shell=True).decode('utf-8')
        logger.info(ls_output)
        print(ls_output)
        subprocess.run(download_command, shell=True)
        subprocess.run(import_script_command, shell=True)
    except subprocess.CalledProcessError as e:
        logger.info('no data updated yesterday.')


def update_works():
    yesterday_date = get_yesterday_date()
    check_and_download_data(yesterday_date)


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_works()
