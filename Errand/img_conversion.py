"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2020/12/29
"""
# coding: utf-8
import os
import pathlib
import multiprocessing as mp

import pyheif
import whatimage
from PIL import Image
from tqdm import tqdm


def create_dir(fp):
    if not os.path.exists(fp):
        os.mkdir(fp)


def heic_to_png(img_path: str, save_path: str):
    with open(img_path, 'rb') as f:
        img_bytes = f.read()
        img_type = whatimage.identify_image(img_bytes)
        # print(f"img type: {img_type}")
        if img_type in ['heic', 'avif']:  # avif
            hei_f = pyheif.read(img_bytes)
            img = Image.frombytes(mode=hei_f.mode, size=hei_f.size, data=hei_f.data)
            img.save(save_path, format='png')


def convert_images(member_name: str, dir_name: str):
    data_dir = f"{root_data_dir}/{dir_name}"
    save_dir = f"{root_output_dir}/{dir_name}"
    create_dir(save_dir)
    for i, img_name in enumerate(os.listdir(data_dir), start=1):
        img_path = f"{data_dir}/{img_name}"
        save_path = f"{save_dir}/{member_name}_{i}.png"
        heic_to_png(img_path, save_path)


def _heic_to_png(task: dict):
    img_path = task['img_path']
    save_path = task['save_path']
    with open(img_path, 'rb') as f:
        img_bytes = f.read()
        img_type = whatimage.identify_image(img_bytes)
        # print(f"img type: {img_type}")
        if img_type in ['heic', 'avif']:  # avif?
            hei_f = pyheif.read(img_bytes)
            img = Image.frombytes(mode=hei_f.mode, size=hei_f.size, data=hei_f.data)
            img.save(save_path, format='png')


def convert_images_mp(member_name: str, dir_name: str):
    data_dir = f"{root_data_dir}/{dir_name}"
    save_dir = f"{root_output_dir}/{dir_name}"
    create_dir(save_dir)

    task_ls = list()
    for i, img_name in enumerate(os.listdir(data_dir), start=1):
        img_path = f"{data_dir}/{img_name}"
        save_path = f"{save_dir}/{member_name}_{i}.png"
        task_ls.append({'img_path': img_path, 'save_path': save_path})

    with mp.Pool() as pool:
        _ = list(
            tqdm(
                pool.imap(_heic_to_png, task_ls), total=len(task_ls)
            )
        )


if __name__ == '__main__':
    # get data root directory
    project_dir = pathlib.Path(__file__).parent.parent  # Horus
    root_data_dir = f"{project_dir}/RAW_DATA"

    print(project_dir)

    # gen output dir
    root_output_dir = f"{project_dir}/output"
    create_dir(root_output_dir)

    print(root_data_dir)
    convert_images_mp('jet', 'jet-img')
    convert_images_mp('lotus', 'lotus-img')
