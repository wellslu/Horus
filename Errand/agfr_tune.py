"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/10
"""
# coding: utf-8
import sys
import pathlib

PROJECT_DIR = str(pathlib.Path(__file__).parent.parent)  # Horus
sys.path.append(PROJECT_DIR)

from typing import Union
from FaceRecog.Facer.Detect.face_capturer import FaceCapturer
from FaceRecog.Facer.Detect.lmk_scanner import LMKScanner
from FaceRecog.Facer.shortcut import get_face_grid_from_portrait
from FaceRecog.Facer.Recognize.adam_geitgey import AGFaceRecog
from FaceRecog.thirdparty.IIIDDFA.get_pose import get_pose
from FaceRecog.Facer.ult.data_store import load_pkl, save_as_json
from numpy import ndarray
from imutils.paths import list_images
import time
import numpy as np
from pprint import pprint as pp
from tqdm import tqdm


def member_verify(img: Union[str, ndarray], member_pkl):
    global zero, not_zero
    st = time.time()

    fg = get_face_grid_from_portrait(img, fc, lmk_scr)
    if fg is None:
        return

    yaw, pitch, roll = get_pose(fg)
    if yaw > 30 or pitch > 30:
        return

    face_encode = fr.get_face_encode(fg)
    if face_encode is None:
        return

    result, score = fr.verify_member(member_pkl, face_encode)
    et = time.time()
    cost = et - st

    if score == 0:
        zero += 1
    else:
        not_zero += 1

    result_rd.append(result)
    score_rd.append(score)
    cost_rd.append(cost)


def workspace(img_dir: str, member_pkl):
    for img_path in tqdm(list(list_images(img_dir))):
        member_verify(img_path, member_pkl)
        # break


# record
zero = 0
not_zero = 0

result_rd = list()
score_rd = list()
cost_rd = list()

if __name__ == '__main__':
    jet_pkl_path = '../MEMBER/jet.pkl'
    JET_PKL = load_pkl(jet_pkl_path)

    lotus_pkl_path = '../MEMBER/lotus.pkl'
    LOTUS_PKL = load_pkl(lotus_pkl_path)

    fc = FaceCapturer()
    fc.load_detector()

    lmk_scr = LMKScanner()
    lmk_scr.load_detector()

    fr = AGFaceRecog()

    IMG_DIR = '../TEST-IMG/lotus'
    workspace(IMG_DIR, LOTUS_PKL)

    RECORD = {
        'result': result_rd,
        'score': score_rd,
        'cost': cost_rd,
        'zero': zero,
        'not_zero': not_zero,
        'result_avg': np.mean(result_rd),
        'score_avg': np.mean(score_rd),
        'cost_avg': np.mean(cost_rd)
    }

    pp(RECORD)
    print()
    print(f"zero: {RECORD['zero']}")
    print(f"not zero: {RECORD['not_zero']}")
    print(f"result avg: {RECORD['result_avg']}")
    print(f"score avg: {RECORD['score_avg']}")
    print(f"cost avg: {RECORD['cost_avg']}")

    save_as_json(RECORD, 'agfr_tune.json')
