"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/10
"""
# coding: utf-8
import pathlib

PROJECT_DIR = pathlib.Path(__file__).parent.parent  # Horus

from typing import Union
from FaceRecog.Facer.Detect.face_capturer import FaceCapturer
from FaceRecog.Facer.Detect.lmk_scanner import LMKScanner
from FaceRecog.Facer.shortcut import get_face_grid_from_portrait
from FaceRecog.Facer.Recognize.adam_geitgey import AGFaceRecog
from FaceRecog.thirdparty.IIIDDFA.get_pose import get_pose
from FaceRecog.Facer.ult.data_store import load_pkl, save_as_json, load_json
from numpy import ndarray
from imutils.paths import list_images
import time
import numpy as np
from pprint import pprint as pp
from tqdm import tqdm

fp = 'agfr_tune.json'

d = load_json(fp)

ls = list()
for i in d.get('score'):
    if i > 0:
        ls.append(i)

print(ls)
print(np.mean(ls))
