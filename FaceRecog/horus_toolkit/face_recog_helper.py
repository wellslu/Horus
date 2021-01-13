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
from ..Facer.ult import get_img_ls
from .db_tool import get_table_df_with_conn
from ..horus_fr_api import do_face_pipeline
from ..cls.recog_result import RecogResult


class FaceRecogHelper:
    IMG_COUNT_THRESH = 1

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

    def recognize(self):
        msg = "[INFO] - start recognizing..."
        print(msg)

        customer_df = get_table_df_with_conn(self.db_conn, self.customer_table_name)
        print(customer_df)

        self._workspace(customer_df)

    def _workspace(self, cus_df: DataFrame):
        for i, row in cus_df.iterrows():
            cus_img_dir = row['customer_img']
            cus_img_ls = get_img_ls(cus_img_dir)

            if len(cus_img_ls) >= FaceRecogHelper.IMG_COUNT_THRESH:
                self._face_recog_worker(cus_img_ls)

    def _face_recog_worker(self, cus_img_ls: list):
        for cus_img_path in cus_img_ls:
            if cus_img_path in self.fp_failed_pool:
                continue

            face_encoding = do_face_pipeline(cus_img_path, self.face_capturer, self.lmk_scanner, self.ag_face_recog)
            if face_encoding is None:
                self.fp_failed_pool.add(cus_img_path)
                continue

    def _member_verify(self, face_encoding: ndarray):
        """
        recog_result:
        - result : bool
        - has_member


        :param face_encoding:
        :return:
        """
        member_cand_ls = list()

        # compare with member face data
        for mid, member_encoding in self.mf_data.items():
            result, similarity = self.ag_face_recog.verify_member(member_encoding, face_encoding)
            if result:
                member_cand_ls.append((mid, similarity))

        # sort and find highly likely member
        print(member_cand_ls)



