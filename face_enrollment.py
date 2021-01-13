"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8
from pandas import DataFrame

from FaceRecog.horus_toolkit import gen_member_id
from FaceRecog.horus_toolkit.db_tool import get_db_conn, get_table_df_with_conn, insert_data_with_conn


def gen_new_mid(table_df: DataFrame) -> str:
    used_mid = table_df['mid'].values

    new_mid = ''
    flag = True
    while flag:
        new_mid = gen_member_id()
        if new_mid not in used_mid:
            flag = False

    return new_mid


def enroll_with_pkl(pkl_path: str):
    conn = get_db_conn()
    table_df = get_table_df_with_conn(conn, TABLE_NAME)
    new_mid = gen_new_mid(table_df)
    data = {'mid': new_mid, 'face_img': pkl_path}
    insert_data_with_conn(conn, TABLE_NAME, data)

    conn.commit()
    conn.close()
    print(f"new member: {new_mid} was added.")


if __name__ == '__main__':
    TABLE_NAME = 'member'

    pickle_path = 'mf_data/jet.pkl'
    enroll_with_pkl(pickle_path)

    pickle_path = 'mf_data/lotus.pkl'
    enroll_with_pkl(pickle_path)
