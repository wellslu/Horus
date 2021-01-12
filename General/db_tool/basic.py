"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8
from typing import Union

import pandas as pd
import pymysql
from pandas import DataFrame
from pymysql.connections import Connection

from . import cfg


def get_db_conn() -> Connection:
    host = cfg.HOST
    port = cfg.PORT
    user = cfg.USER
    password = cfg.PASSWORD
    db = cfg.DB
    try:
        conn = pymysql.connect(host=host, port=port,
                               user=user, passwd=password,
                               database=db, charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
    except Exception as e:
        print(f'[WARN] - Failed to connect database: {host}:{port} -> {db}  USER: {user}')
        print(f'error: {e}')


def get_table_data_with_conn(conn: Connection, table_name: str, db_name=None) -> Union[list, tuple]:
    """
    - if the table is empty, it will return a tuple

    :param conn:
    :param table_name:
    :param db_name:
    :return:
    """
    if db_name is None:
        db_name = cfg.DB

    query = f"""
        SELECT * from {db_name}.{table_name}
    """

    with conn.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def get_table_df_with_conn(conn: Connection, table_name: str, db_name=None) -> DataFrame:
    """
    - if the table is empty, it will return an empty DataFrame

    :param conn:
    :param table_name:
    :param db_name:
    :return:
    """
    if db_name is None:
        db_name = cfg.DB

    query = f"""
        SELECT * from {db_name}.{table_name}
    """

    return pd.read_sql_query(query, conn)


def insert_data_with_conn(conn: Connection, table_name: str, data: Union[dict], db_name=None):
    if db_name is None:
        db_name = cfg.DB

    # query of table-mapping
    query = ''
    if table_name is 'member':
        mid = data.get('mid')
        face_img = data.get('face_img')
        query = f"""
            INSERT INTO {db_name}.{table_name}
            (mid, face_img)
            VALUES
            ('{mid}', '{face_img}')
        """

    with conn.cursor() as cursor:
        cursor.execute(query)
