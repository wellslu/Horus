"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2020/12/29
"""
# coding: utf-8
import os
import pathlib
import ntpath
import subprocess
import multiprocessing as mp

import pyheif
import whatimage
from PIL import Image
from tqdm import tqdm


def create_dir(fp):
    if not os.path.exists(fp):
        os.mkdir(fp)


def get_extension(fp: str) -> str:
    return str(ntpath.basename(fp)).split('.')[-1]


def ffmpeg_convert(src, dest):
    subprocess.call(['ffmpeg', '-i', src, dest])


def convert_video(src_dir: str, save_dir: str):
    for file_name in tqdm(os.listdir(src_dir)):
        video_path = f"{src_dir}/{file_name}"

        video_ext = get_extension(video_path)
        video_name = file_name.replace(f".{video_ext}", '')
        save_path = f"{save_dir}/{video_name}.mp4"

        if video_ext in ['MOV', 'mov']:
            ffmpeg_convert(video_path, save_path)


if __name__ == '__main__':
    # get data root directory
    project_dir = pathlib.Path(__file__).parent.parent  # horus
    root_data_dir = f"{project_dir}/RAW_DATA"

    # gen output dir
    OUTPUT_DIR = f"{project_dir}/output/mp4"
    create_dir(OUTPUT_DIR)

    SRC_DIR = f"{root_data_dir}/clips"

    convert_video(SRC_DIR, OUTPUT_DIR)
