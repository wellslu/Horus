"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/10
"""
# coding: utf-8
import pathlib

# from ..FaceRecog import Facer <- this is not allowed
# add parent directory to path
PROJECT_DIR = pathlib.Path(__file__).parent.parent  # Horus
from FaceRecog.Facer.Recognize.adam_geitgey import AGFaceRecog

if __name__ == '__main__':
    fr = AGFaceRecog()

    member_dir = '../MEMBER/jet-img'
    fr.data_to_fe_pkl(member_dir, 'jet.pkl')

    member_dir = '../MEMBER/lotus-img'
    fr.data_to_fe_pkl(member_dir, 'lotus.pkl')
