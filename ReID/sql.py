from sqlalchemy import create_engine
import pandas as pd
import datetime


class Sql:
    def __init__(self):
        self.account = 'gauser'
        self.password = 'Lhi5dFLDymIlp8u9'
        self.hostname = '35.202.28.34:3306'
        self.db = 'ga'

    # after check upload the results of check
    def put_sql(self, results):
        engine = create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(self.account, self.password, self.hostname, self.db))
        con = engine.connect()
        sql_code = '''SELECT *
                        FROM check_result 
                       LIMIT 0,0;'''
        df = pd.read_sql_query(sql_code, engine)
        df.drop('id', axis=1, inplace=True)
        results = pd.concat([results, df], ignore_index=True, sort=False)
        results.fillna(value='Missing value', inplace=True)
        results['note'] = None
        results.to_sql(name='check_result', con=con, if_exists='append', index=False)
        con.close()

    # get client name and check_item_name for make log
    def get_name(self, client_id):
        engine = create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(self.account, self.password, self.hostname, self.db))

        con = engine.connect()
        sql_code = '''SELECT * 
                        FROM check_item'''
        item_name_df = pd.read_sql_query(sql_code, engine)

        sql_code = '''SELECT * 
                        FROM client
                       WHERE id = ''' + str(client_id)
        df = pd.read_sql_query(sql_code, engine)
        client_name = df['name'][0]

        sql_code = '''SELECT *
                        FROM report_subject '''
        report_subject = pd.read_sql_query(sql_code, engine)

        sql_code = '''SELECT *
                                FROM check_time_range '''
        check_time_range = pd.read_sql_query(sql_code, engine)
        con.close()

        return item_name_df, client_name, report_subject, check_time_range

    # get crawler last time score
    def get_crawler_lastinfo(self, client_id):
        # noinspection PyBroadException
        try:
            # get last crawler result
            engine = create_engine(
                "mysql+pymysql://{}:{}@{}/{}".format(self.account, self.password, self.hostname, self.db))

            con = engine.connect()
            sql_code = '''SELECT *
                               FROM check_result 
                              WHERE check_item_id = 15 
                                AND client_id = {} 
                           ORDER BY timeindex_id DESC 
                              LIMIT 0,1'''.format(client_id)
            crawler_result = pd.read_sql_query(sql_code, engine)
            crawler_result = crawler_result.drop(['id', 'note'], axis=1)
            if crawler_result['status'][0] == 0:
                crawler_result['status'] = False
            elif crawler_result['status'][0] == 1:
                crawler_result['status'] = True
            # get last crawler score
            sql_code = '''SELECT * 
                               FROM time_index 
                              WHERE id = ''' + str(crawler_result['timeindex_id'][0])
            df = pd.read_sql_query(sql_code, engine)
            crawler_score = df['score'][0]
            con.close()
        except:
            crawler_result, crawler_score = None, None

        return crawler_result, crawler_score

    # create a timeindex before get ga_info
    def build_timeindex(self, con, engine):
        # get max num from table time_index
        timeindex_id = None
        sql_code = '''SELECT COUNT(id)
                        FROM time_index'''
        all_count = con.execute(sql_code)
        for row in all_count:
            timeindex_id = row[0] + 1
        sql_code = '''SELECT *
                        FROM time_index 
                       LIMIT 0,0;'''
        # make upload timeindex df
        time_table = pd.read_sql_query(sql_code, engine)
        time_table['id'] = [timeindex_id]
        time_table['send_mail_status'] = 0
        check_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_table['created_at'] = check_time
        # noinspection PyBroadException
        try:
            time_table.to_sql(name='time_index', con=con, if_exists='append', index=False)
            return check_time, timeindex_id
        except:
            timeindex_id = self.build_timeindex(con, engine)
            return check_time, timeindex_id

    def get_ga_info(self, ga_info_id):
        engine = create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(self.account, self.password, self.hostname, self.db))
        con = engine.connect()

        check_time, timeindex = self.build_timeindex(con, engine)
        # get client ga information
        sql_code = '''SELECT * 
                        FROM ga_info 
                       WHERE id = ''' + str(ga_info_id)
        df = pd.read_sql_query(sql_code, engine)
        client_id = df['client_id'][0]
        account_id = df['ga_account_id'][0]
        account_id = str(account_id)
        webproperty_id = df['ga_property_id'][0]
        view_id = df['ga_view_id'][0]
        view_id = str(view_id)
        domain_id = df['client_web_domain_id'][0]
        domain_id = domain_id.split(',')
        item_id = df['check_item_id'][0]
        item_id = item_id.split(',')
        path_id = df['client_ga_certificate_id'][0]
        creator = int(df['creator'][0])
        report_level = int(df['report_level'][0])
        # get domain
        domain = []
        for domainid in domain_id:
            sql_code = '''SELECT * 
                            FROM client_web_domain 
                           WHERE id = ''' + str(domainid)
            df = pd.read_sql_query(sql_code, engine)
            domain.append(df['domain'][0])
        # get ga certificate api url
        sql_code = '''SELECT *
                        FROM client_ga_certificate
                       WHERE id = ''' + str(path_id)
        df = pd.read_sql_query(sql_code, engine)
        path = df['path'][0]
        path = 'http://hac.iprospect.support/storage/certificate/' + path
        con.close()
        return ga_info_id, client_id, account_id, webproperty_id, view_id, item_id, path, domain, check_time, timeindex, creator, report_level

    # upload error_sheet and score
    def put_error_sql(self, error_path, score, timeindex_id, creator, client_id):
        engine = create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(self.account, self.password, self.hostname, self.db))
        engine.execute('''update time_index set file_path =%s where id= %s ''', (str(error_path), timeindex_id))
        engine.execute('''update time_index set  score=%s where id= %s ''', (int(score), timeindex_id))
        engine.execute('''update time_index set  creator=%s where id= %s ''', (int(creator), timeindex_id))
        engine.execute('''update time_index set  client_id=%s where id= %s ''', (int(client_id), timeindex_id))
