"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/10
"""
# coding: utf-8
import sys
import pathlib

# add project directory to path
PROJECT_DIR = str(pathlib.Path(__file__).parent.parent)  # Horus
sys.path.append(PROJECT_DIR)

from FaceRecg.Facer import AGFaceRecog

if __name__ == '__main__':
    fr = AGFaceRecog()

    member_dir = '../MEMBER/jet-img'
    fr.data_to_fe_pkl(member_dir, 'jet.pkl')

    member_dir = '../MEMBER/lotus-img'
    fr.data_to_fe_pkl(member_dir, 'lotus.pkl')
