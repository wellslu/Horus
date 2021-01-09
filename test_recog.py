"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/9
"""
# coding: utf-8
import time
from typing import Union


from numpy import ndarray

from FaceRecog.Facer.Detect.face_capturer import FaceCapturer
from FaceRecog.Facer.Detect.lmk_scanner import LMKScanner
from FaceRecog.Facer.shortcut import get_face_grid_from_portrait
from FaceRecog.Facer.Recognize.adam_geitgey import AGFaceRecog
from FaceRecog.Facer.ult.data_store import load_pkl
from FaceRecog.Facer.ult.view import show

def get_fg(img: Union[str, ndarray], face_capturer: FaceCapturer,
           lmk_scanner: LMKScanner) -> ndarray:
    s = time.time()
    face_grid = get_face_grid_from_portrait(img, face_capturer, lmk_scanner)
    e = time.time()
    print(f"get fg cost: {e - s}")
    return face_grid


def get_face_encode(img: ndarray) -> ndarray:
    s = time.time()
    face_encoding = fr.get_face_encode(img)
    e = time.time()
    print(f"face encoding cost: {e - s}")
    return face_encoding



# img_path = 'TEST-IMG/puff_ob.jpg'
# img_path = 'TEST-IMG/ys1.jpg'
img_path = 'TEST-SAMPLE/jet_1.png'
# img_path = 'TEST-IMG/lotus_1.png'
# img_path = 'TEST-IMG/v.png'


member_data_path = 'MEMBER/jet-img'

if __name__ == '__main__':
    fc = FaceCapturer()
    fc.load_detector()

    lmk_scr = LMKScanner()
    lmk_scr.load_detector()

    fr = AGFaceRecog()

    jet1 = 'TEST-IMG/jet_1.png'
    lotus1 = 'TEST-IMG/lotus_1.png'
    jet2 = 'TEST-IMG/jet_2.png'
    jet_h = 'TEST-IMG/jet_h.jpg'
    puff1 = 'TEST-IMG/puff_ob.jpg'
    v = 'TEST-IMG/v.png'


    # jet_dir = 'MEMBER/jet-img'
    # st = time.time()
    # fr.data_to_fe_pkl(jet_dir, 'jet.pkl')
    # ed = time.time()
    # print(ed - st)

    jet_encode = load_pkl('jet.pkl')
    # test_encode = get_face_encode(get_fg(jet1, fc, lmk_scr))
    # test_encode = get_face_encode(get_fg(v, fc, lmk_scr))

    test_fg = get_fg(jet1, fc, lmk_scr)
    test_encode = get_face_encode(test_fg)

    s = time.time()
    res = fr.compare_faces(jet_encode, test_encode)
    e = time.time()
    print(e - s)

    print(res)
    score = fr.get_similarity(res)
    print(score)

    # jet1_encode = get_face_encode(get_fg(jet1, fc, lmk_scr))
    # lotus1_encode = get_face_encode(get_fg(lotus1, fc, lmk_scr))
    # jet2_encode = get_face_encode(get_fg(jet2, fc, lmk_scr))
    # puff1_encode = get_face_encode(get_fg(puff1, fc, lmk_scr))
    #
    # print(compare(jet1_encode, jet2_encode))
    # print(compare(jet1_encode, lotus1_encode))
    # print(compare(jet1_encode, puff1_encode))
