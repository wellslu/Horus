import pandas as pd
import pymysql


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


def create_table(conn: pymysql.connections.Connection):
    with conn.cursor() as cursor:
        query = """
        CREATE TABLE IF NOT EXISTS `teacher`( \
        `TEACHER_ID` INT(2) NOT NULL, \
        `FIRST_NAME` VARCHAR(20) NOT NULL, \
        `LAST_NAME` VARCHAR(20) NOT NULL, \
        `AGE` VARCHAR(2) NOT NULL \
        )ENGINE=InnoDB
        """
        cursor.execute(query)


def insert_data(conn: pymysql.connections.Connection):
    with conn.cursor() as cursor:
        query = """
        INSERT INTO `test`.`teacher` 
        (`TEACHER_ID`, `FIRST_NAME`, `LAST_NAME`, `AGE`) 
        VALUES 
        (1, 'JAY', 'CHEN', 25)
        """
        cursor.execute(query)


def get_data(conn: pymysql.connections.Connection) -> list:
    with conn.cursor() as cursor:
        query = """
        SELECT * FROM test.teacher
        """
        cursor.execute(query)
        return cursor.fetchall()


def get_data_as_df(conn: pymysql.connections.Connection) -> pd.DataFrame:
    # return pd.read_sql_table('teacher', conn) # only supported for SQLAlchemy connectable.
    query = """
    SELECT * FROM test.teacher
    """
    # return pd.read_sql(query, conn) # ok
    return pd.read_sql_query(query, conn)  # ok


conn = get_db_conn()

df = get_data_as_df(conn)
print(df)

data = get_data(conn)
print(data)

# # create_table(conn)
# insert_data(conn)
#
# conn.commit()
# conn.close()
# print('done')
