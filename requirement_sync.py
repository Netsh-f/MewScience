# ------- Litang Save The World! -------
#
# @Time    : 2023/12/25 23:07
# @Author  : Lynx
# @File    : requirement_sync.py.py
#
import subprocess

import subprocess

banned_list = ['distribute', 'pip', 'setuptools', 'wheel']

subprocess.run('pip list --format=freeze > requirements.txt', shell=True)

with open('requirements.txt', 'r') as file:
    lines = file.readlines()

filtered_lines = [line for line in lines if not any(line.startswith(pkg) for pkg in banned_list)]

with open('requirements.txt', 'w') as file:
    file.writelines(filtered_lines)