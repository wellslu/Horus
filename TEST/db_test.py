import pandas as pd
import pymysql
import time
import datetime


def get_db_conn() -> pymysql.connections.Connection:
    host = '163.14.137.58'
    port = 8080
    user = 'admin'
    password = 'iflab'
    db = 'test'
    try:
        conn = pymysql.connect(host=host, port=port,
                               user=user, passwd=password,
                               database=db, charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        return conn
    except Exception as e:
        print(f'[WARN] - Failed to connect database: {host}:{port} -> {db}  USER: {user}')
        print(f'error: {e}')


def get_data(conn: pymysql.connections.Connection) -> list:
    with conn.cursor() as cursor:
        query = """
        SELECT * FROM test.customer
        """
        cursor.execute(query)
        return cursor.fetchall()


def get_data_as_df(conn: pymysql.connections.Connection) -> pd.DataFrame:
    # return pd.read_sql_table('teacher', conn) # only supported for SQLAlchemy connectable.

    query = """
    SELECT * FROM test.customer
    """
    # return pd.read_sql(query, conn) # ok
    return pd.read_sql_query(query, conn)  # ok


def insert_data(conn: pymysql.connections.Connection):
    """
    columns in customer table
    - cid : not null
    - last_cid
    - mid
    - customer_img
    - enter_time
    - leave_time

    :param conn:
    :return:
    """
    with conn.cursor() as cursor:
        # a insert example
        cid = 'c-test'
        customer_img = 'abs/path/to/img'
        enter_time = datetime.datetime.now()
        time.sleep(2)
        leave_time = datetime.datetime.now()
        query = f"""
        INSERT INTO test.customer
        (cid, customer_img, enter_time, leave_time) 
        VALUES 
        ('{cid}', '{customer_img}', '{enter_time}', '{leave_time}')
        """
        cursor.execute(query)


if __name__ == '__main__':
    conn = get_db_conn()

    print('get data: \n', get_data(conn))

    print('get data as df: \n', get_data_as_df(conn))

    insert_data(conn)
    conn.commit()
    conn.close()
    print('done')
