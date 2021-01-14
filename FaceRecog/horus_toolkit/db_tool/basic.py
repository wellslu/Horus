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


def get_db_conn(host=None, port=None, user_name=None, password=None, db_name=None) -> Connection:
    if host is None:
        host = cfg.HOST

    if port is None:
        port = cfg.PORT

    if user_name is None:
        user_name = cfg.USER

    if password is None:
        password = cfg.PASSWORD

    if db_name is None:
        db_name = cfg.DB

    try:
        conn = pymysql.connect(host=host, port=port,
                               user=user_name, passwd=password,
                               database=db_name, charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
    except Exception as e:
        print(f'[WARN] - Failed to connect database: {host}:{port} -> {db_name}  USER: {user_name}')
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


def exe_query(conn: Connection, query: str):
    with conn.cursor() as cursor:
        cursor.execute(query)

def exe_query_many(conn: Connection, query: str, data: list):
    with conn.cursor() as cursor:
        cursor.executemany(query, data)

def insert_data_with_conn(conn: Connection, table_name: str, data: Union[dict], db_name=None):
    if db_name is None:
        db_name = cfg.DB

    # query of table-mapping
    query = ''
    if table_name == 'member':
        mid = data.get('mid')
        face_img = data.get('face_img')
        query = f"""
            INSERT INTO {db_name}.{table_name}
            (mid, face_img)
            VALUES
            ('{mid}', '{face_img}')
        """

    exe_query(conn, query)


def update_data_with_conn(conn: Connection, table_name: str, new_data: dict, where: dict):
    """
    - new_data :
    {
        'col_you_to_update' : 'val_to_update'
    }

    - target :
    {
        'condition_col' : 'condition_val'
    }

    * example:
        If you want to update a table which named "student"
        and change "name" to "Jet"
        on the row with "id" "21"

        you should input the arguments like this way:
            update_data_with_conn(
                conn,
                'student',
                {'name' : 'Jet'},
                {'id' : 21}
            )

    :param conn:
    :param table_name:
    :param new_data:
    :param where:
    :return:
    """
    new_data = list(new_data.items())
    where = list(where.items())

    prefix = f"""UPDATE {table_name} SET"""

    infix = ''
    while new_data:
        d = new_data.pop(0)
        infix += f" `{d[0]}` = '{d[1]}'"
        if len(new_data):
            infix += ','
        else:
            infix += ' '

    suffix = f"""WHERE `{where[0][0]}` = {where[0][1]}"""

    # example : UPDATE customer SET `mid` = 'M-h7ed' WHERE `id` = 1
    query = prefix + infix + suffix  # it might not be the best way, cause the datatype of db-table
    # print(query)

    exe_query(conn, query)
