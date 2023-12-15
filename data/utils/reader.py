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

from tqdm import tqdm


def read_lines_from_openalex_data(path, save_to_database):
    processed_files_filepath = os.path.join(path, 'processed_files.json')
    processed_data = {}
    if os.path.exists(processed_files_filepath):
        with open(processed_files_filepath, 'r') as processed_files_file:
            processed_data = json.load(processed_files_file)

    for date_folder in os.listdir(path):
        date_folder_path = os.path.join(path, date_folder)
        if os.path.isdir(date_folder_path):
            for part_file in os.listdir(date_folder_path):
                part_file_path = os.path.join(date_folder_path, part_file)
                relative_path = os.path.relpath(part_file_path, path)
                if part_file.endswith(".gz") and (
                        relative_path not in processed_data or relative_path == list(processed_data.keys())[-1]):
                    with gzip.open(part_file_path, 'rt') as gz_file:
                        total_lines = sum(1 for line in gz_file)
                        gz_file.seek(0)
                        processed_lines = processed_data.get(relative_path, 0)
                        with tqdm(total=total_lines, desc=f'Processing {relative_path}', unit=' lines') as pbar:
                            gz_file.seek(0)
                            for _ in range(processed_lines):
                                next(gz_file)  # 跳过已处理行
                                pbar.update(1)
                            for line in gz_file:
                                json_data = json.loads(line)
                                save_to_database(json_data)
                                pbar.update(1)
                                processed_lines += 1
                                if processed_lines % 1000 == 0:
                                    processed_data[relative_path] = processed_lines
                                    with open(processed_files_filepath, 'w') as processed_files_file:
                                        json.dump(processed_data, processed_files_file, indent=2)
                    processed_data[relative_path] = processed_lines
                    with open(processed_files_filepath, 'w') as processed_files_file:
                        json.dump(processed_data, processed_files_file, indent=2)
