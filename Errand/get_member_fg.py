"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/8
"""
# coding: utf-8
import os
import pathlib
from FaceRecog.Facer.shortcut import get_face_grid_from_portrait

def create_dir(fp: str):
    if not os.path.exists(fp):
        os.mkdir(fp)


def get_member_fg(member_name: str, member_img_dir):
    for img_path in os.listdir(member_img_dir):
        pass
        # fg = get_face_grid_from_portrait(img_path, 0.2)
        # if fg is not None:
        #     print(fg)
        #     break


save_dir = 'fg'
create_dir(save_dir)
project_dir = pathlib.Path(__file__).parent.parent  # horus

if __name__ == '__main__':
    mn = 'jet'
    md = f"{project_dir}/DATA/{mn}-img"
    get_member_fg(mn, md)
