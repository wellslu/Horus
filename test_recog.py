"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/9
"""
# coding: utf-8
import time

from FaceRecog.Facer.shortcut import get_face_grid_from_portrait
from FaceRecog.thirdparty.IIIDDFA.get_pose import get_pose

img_path = 'TEST-IMG/jet1.jpg'

if __name__ == '__main__':
    st = time.time()
    fg = get_face_grid_from_portrait(img_path)
    ed = time.time()
    print(ed - st)

    st = time.time()
    pose = get_pose(fg)
    ed = time.time()
    print(ed - st)

    print(pose)

    pass
