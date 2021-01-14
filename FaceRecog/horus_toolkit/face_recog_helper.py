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
from .db_tool import get_table_df_with_conn, update_data_with_conn
from ..horus_fr_api import do_face_pipeline
from ..cls.recog_result import RecogResult
from typing import Union


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

    @staticmethod
    def sort_member_candidate(member_cand_ls: list):
        if len(member_cand_ls):
            # sort with similarity
            member_cand_ls.sort(key=lambda x: x[1], reverse=True)

    def recognize(self):
        msg = "[FACE-RECOG][INFO] - Start recognizing..."
        print(msg)

        customer_df = get_table_df_with_conn(self.db_conn, self.customer_table_name)
        print(customer_df)

        # work
        self._workspace(customer_df)

        msg = "[FACE-RECOG][INFO] - Finish all recognizing work"
        print(msg)

    def recognize_df(self, customer_df: DataFrame):
        msg = "[FACE-RECOG][INFO] - Start recognizing..."
        print(msg)

        # work
        self._workspace(customer_df)

        msg = "[FACE-RECOG][INFO] - Finish all recognizing work"
        print(msg)

    def _workspace(self, cus_df: DataFrame):
        for i, row in cus_df.iterrows():
            # if row['id'] != 2:
            #     continue

            if row['mid'] is not None:
                continue

            cus_img_dir = row['customer_img']
            cus_img_ls = get_img_ls(cus_img_dir)

            if len(cus_img_ls) < FaceRecogHelper.IMG_COUNT_THRESH:
                continue

            face_identity = self._face_recog_worker(cus_img_ls)
            if face_identity is not None:
                # update member id to db
                new_data = {'mid': face_identity}
                where = {'id': row['id']}
                update_data_with_conn(self.db_conn, self.customer_table_name, new_data, where)
                self.db_conn.commit()

    def _face_recog_worker(self, cus_img_ls: list) -> Union[str, None]:
        for cus_img_path in cus_img_ls:
            if cus_img_path in self.fp_failed_pool:
                continue

            face_encoding = do_face_pipeline(cus_img_path, self.face_capturer, self.lmk_scanner, self.ag_face_recog)
            if face_encoding is None:
                msg = f"[FACE-RECOG][INFO] - Failed during face pipeline. image: {cus_img_path}"
                # print(msg)
                self.fp_failed_pool.add(cus_img_path)
                continue

            msg = f"[FACE-RECOG][INFO] - Try to find member in image: {cus_img_path}"
            print(msg)
            recog_result = self._find_member(face_encoding)
            if recog_result.has_member:
                msg = f"[FACE-RECOG][INFO] - Recog Result of image: {cus_img_path}\n{recog_result}"
                print(msg)
                return recog_result.ml_member

    def _find_member(self, face_encoding: ndarray) -> RecogResult:
        member_cand_ls = list()

        # compare with member face data
        for mid, member_encoding in self.mf_data.items():
            is_matched, similarity = self.ag_face_recog.verify_member(member_encoding, face_encoding)
            msg = f"[FACE-RECOG][INFO] - Is matched with member: {is_matched}  Similarity: {similarity}"
            print(msg)
            if is_matched:
                member_cand_ls.append((mid, similarity))

        # sort and find highly likely member
        FaceRecogHelper.sort_member_candidate(member_cand_ls)

        if len(member_cand_ls):
            hl_member = member_cand_ls[0][0]
            return RecogResult(True, True, hl_member, member_cand_ls)

        else:
            return RecogResult(True, False, None, member_cand_ls)
