"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/10
"""
# coding: utf-8
import pathlib

PROJECT_DIR = pathlib.Path(__file__).parent.parent  # Horus

import os
from FaceRecog.Facer.Detect.face_capturer import FaceCapturer
from FaceRecog.Facer.Detect.lmk_scanner import LMKScanner
from FaceRecog.Facer.shortcut import get_face_grid_from_portrait
from FaceRecog.Facer.Recognize.adam_geitgey import AGFaceRecog
from FaceRecog.thirdparty.IIIDDFA.get_pose import get_pose
from tqdm import tqdm


def move_to_no_fg(sd: str, img_path: str, img_bn: str):
    dest = f"{ROOT_DIR}/{sd}-no-fg/{img_bn}"
    os.replace(img_path, dest)


def move_to_no_fe(sd: str, img_path: str, img_bn: str):
    dest = f"{ROOT_DIR}/{sd}-no-fe/{img_bn}"
    os.replace(img_path, dest)


def move_to_not_front(sd: str, img_path: str, img_bn: str):
    dest = f"{ROOT_DIR}/{sd}-not-front/{img_bn}"
    os.replace(img_path, dest)


def separate_images(member_name: str):
    sd = member_name
    img_dir = f"{ROOT_DIR}/{sd}"

    for f_bn in tqdm(os.listdir(img_dir)):
        img_path = f"{img_dir}/{f_bn}"

        fg = get_face_grid_from_portrait(img_path, fc, lmk_scr)
        if fg is None:
            move_to_no_fg(sd, img_path, f_bn)
            print(f"move to no face grid : {img_path}")
            continue
            # return

        face_encode = fr.get_face_encode(fg)
        if face_encode is None:
            move_to_no_fe(sd, img_path, f_bn)
            print(f"move to no face encode : {img_path}")
            continue

        yaw, pitch, roll = get_pose(fg)
        if yaw > 30 or pitch > 30:
            move_to_not_front(sd, img_path, f_bn)
            print(f"move to not front face : {img_path}")
            continue


if __name__ == '__main__':
    fc = FaceCapturer()
    fc.load_detector()

    lmk_scr = LMKScanner()
    lmk_scr.load_detector()

    fr = AGFaceRecog()

    ROOT_DIR = '../TEST-IMG'
    separate_images('lotus')
