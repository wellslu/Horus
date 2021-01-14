import pymysql.cursors

class SQL(object):
    def __init__(self):
        config = {'host': '163.14.137.58',
                  'port': 8080,
                  'user': 'admin',
                  'password': 'iflab',
                  'db': 'dev1',
                  'charset': 'utf8mb4',
                  'cursorclass': pymysql.cursors.DictCursor}
        self.connection = pymysql.connect(**config)
        self.cursor = self.connection.cursor()

    def read_customer_table(self):
        sql_code = 'SELECT * FROM customer'
        self.cursor.execute(sql_code)
        result = self.cursor.fetchall()
        self.connection.commit()
        return result

    def write_customer_table(self, sql_code):
        self.cursor.execute(sql_code)
        self.connection.commit()



    def close_sql(self):
        self.cursor.close()
        self.connection.close()