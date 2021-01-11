"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/8
"""
# coding: utf-8
import os
import pathlib
import sys

import cv2
from imutils.paths import list_images

# from ..FaceRecog import Facer <- this is not allowed
PROJECT_DIR = str(pathlib.Path(__file__).parent.parent)  # Horus
sys.path.append(PROJECT_DIR)


def create_dir(fp: str):
    if not os.path.exists(fp):
        os.mkdir(fp)


def get_member_fg(member_name: str, member_img_dir):
    save_cnt = 0
    for term, img_path in enumerate(list_images(member_img_dir)):
        print(f"term: {term}")
        fg = get_face_grid_from_portrait(img_path, 0.2)
        if fg is not None:
            save_cnt += 1
            sub_dir = f"{save_dir}/{member_name}-img"
            create_dir(sub_dir)
            save_path = f"{sub_dir}/{member_name}_{save_cnt}.png"
            cv2.imwrite(save_path, fg)
            print(f"{member_name} - save count: {save_cnt}")



save_dir = 'fg'
create_dir(save_dir)
project_dir = pathlib.Path(__file__).parent.parent  # horus

if __name__ == '__main__':
    mn = 'jet'
    md = f"{project_dir}/DATA/{mn}-img"
    get_member_fg(mn, md)

    mn = 'lotus'
    md = f"{project_dir}/DATA/{mn}-img"
    get_member_fg(mn, md)
