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
            print(face_data)

        elif face_img_type in ['jpg', 'png']:
            pass

        elif os.path.isdir(face_img_type):
            pass

        mf_data[mid] = face_data

    return mf_data
