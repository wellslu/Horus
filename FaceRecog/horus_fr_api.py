"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8
import ntpath
import os

from pymysql.connections import Connection
from .Facer.ult import load_pkl
from .horus_toolkit.db_tool import get_table_df_with_conn
from FaceRecog.Facer import FaceCapturer, LMKScanner
from pymysql.connections import Connection
from imutils.paths import list_images
from .Facer.shortcut import get_face_grid_from_portrait

IMG_COUNT_THRESH = 1


def get_mf_data(conn: Connection, table_name='member', db_name=None) -> dict:
    mf_data = dict()
    table_df = get_table_df_with_conn(conn, table_name, db_name)

    for i, row in table_df.iterrows():
        mid = row['mid']
        face_img_path = row['face_img']
        face_img_type = ntpath.abspath(face_img_path).split('.')[-1]

        face_data = None
        if face_img_type == 'pkl':
            face_data = load_pkl(face_img_path)

        elif face_img_type in ['jpg', 'png']:
            pass

        elif os.path.isdir(face_img_type):
            pass

        mf_data[mid] = face_data

    return mf_data


def do_face_pipeline(img_path: str, face_capturer: FaceCapturer, lmk_scanner: LMKScanner):
    face_grid = get_face_grid_from_portrait(img_path, face_capturer, lmk_scanner)
    if face_grid is None:
        return

    face_encode = ''


# >>>>>> do face recog >>>>>>
def do_face_recog(face_capturer: FaceCapturer, lmk_scanner: LMKScanner, mf_data: dict,
                  fr_db_conn: Connection, member_table_name: str, customer_table_name: str):
    customer_df = get_table_df_with_conn(fr_db_conn, customer_table_name)
    print(customer_df)

    for i, row in customer_df.iterrows():
        img_dir = row['customer_img']
        img_ls = list(list_images(img_dir))

        if len(img_ls) >= IMG_COUNT_THRESH:
            _face_recog_worker(face_capturer, lmk_scanner, mf_data, img_ls)


def _face_recog_worker(face_capturer: FaceCapturer, lmk_scanner: LMKScanner,
                       mf_data: dict, img_ls: list):
    for img_path in img_ls:
        print(img_path)

# <<<<<< do face recog <<<<<<
