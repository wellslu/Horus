"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8
from pymysql.connections import Connection
from numpy import ndarray
from pandas import DataFrame
from ..Facer import FaceCapturer, LMKScanner, AGFaceRecog
# from ..Facer.ult


class FaceRecogHelper:
    def __init__(self, face_capturer: FaceCapturer, lmk_scanner: LMKScanner, ag_face_recog: AGFaceRecog, mf_data: dict,
                 fr_db_conn: Connection, member_table_name: str, customer_table_name: str):
        # recognition core tool
        self.face_capturer = face_capturer
        self.lmk_scanner = lmk_scanner
        self.ag_face_recog = ag_face_recog

        # db connection
        self.db_conn = fr_db_conn

        # const var
        self.member_table_name = member_table_name
        self.customer_table_name = customer_table_name

        # ref data var
        self.mf_data = mf_data

        # data var
        self.fp_failed_pool = set()  # face pipeline failed pool

    def recognize_helper(self, customer_df: DataFrame):
        for i, row in customer_df.iterrows():
            img_dir = row['customer_img']
            img_ls = list(list_images(img_dir))

            if len(img_ls) >= IMG_COUNT_THRESH:
                _face_recog_worker(face_capturer, lmk_scanner, ag_face_recog, mf_data, img_ls)
