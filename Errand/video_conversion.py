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

def convert_video():
    pass



if __name__ == '__main__':
    # get data root directory
    project_dir = pathlib.Path(__file__).parent.parent  # horus
    root_data_dir = f"{project_dir}/RAW_DATA"

    # gen output dir
    OUTPUT_DIR = f"{project_dir}/output/mp4"
    create_dir(OUTPUT_DIR)

    SRC_DIR = f"{root_data_dir}/clips"

    print(SRC_DIR, OUTPUT_DIR)


