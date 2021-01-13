"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8
from typing import Union
import time
import datetime
from pymysql.connections import Connection
from .face_recog_helper import FaceRecogHelper
from ..Facer import FaceCapturer, LMKScanner, AGFaceRecog

from .tk_gen import gen_random_token


def gen_member_id(rt_len=4) -> Union[str, None]:
    if rt_len < 4:
        msg = '[WARN] - The length of random token must be greater or equal to 4!'
        print(msg)
        return

    return f"M-{gen_random_token(rt_len)}"


def pause(sec: int):
    time.sleep(sec)


def sec_to_hms(sec: Union[float, int]) -> str:
    if isinstance(sec, float):
        sec = int(sec)
    return str(datetime.timedelta(seconds=sec))


def get_face_recog_helper(face_capturer: FaceCapturer, lmk_scanner: LMKScanner,
                          ag_face_recog: AGFaceRecog, mf_data: dict,
                          fr_db_conn: Connection, member_table_name: str, customer_table_name: str) -> FaceRecogHelper:
    return FaceRecogHelper(
        face_capturer,
        lmk_scanner,
        ag_face_recog,
        mf_data,
        fr_db_conn,
        member_table_name,
        customer_table_name
    )
