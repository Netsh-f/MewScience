"""
============================
# @Time    : 2023/12/9 20:03
# @Author  : Elaikona
# @FileName: reader.py
===========================
"""
import gzip
import json
import os


def read_lines_from_openalex_data(path, save_to_database):
    for date_folder in os.listdir(path):
        date_folder_path = os.path.join(path, date_folder)

        # 检查是否为文件夹
        if os.path.isdir(date_folder_path):
            print(f"---import {date_folder_path}")

            # 遍历每个日期文件夹下的part文件
            for part_file in os.listdir(date_folder_path):
                part_file_path = os.path.join(date_folder_path, part_file)

                # 检查是否为gzip文件
                if part_file.endswith(".gz"):
                    print(f"import {part_file_path}")

                    # 打开gzip文件并读取内容
                    with gzip.open(part_file_path, 'rt') as gz_file:
                        # 逐行读取JSON数据
                        for line in gz_file:
                            json_data = json.loads(line)
                            save_to_database(json_data)
                    print(f"import {part_file_path} completed")
            print(f"---import {date_folder_path} completed")
