"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/8
"""
# coding: utf-8
import inspect
import os
import pathlib

# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# print(current_dir)
# print(parent_dir)

project_dir = pathlib.Path(__file__).parent.parent  # horus
print(project_dir)

if __name__ == '__main__':
    project_dir = pathlib.Path(__file__).parent.parent  # horus
    print(project_dir)
