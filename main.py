# coding: utf-8
import time
from threading import Thread

from FaceRecog.horus_fr_api import get_mf_data
from FaceRecog.horus_toolkit.db_tool import get_db_conn

from pprint import pprint as pp

# >>>>>> listened variables >>>>>>
fr_update_index = 0


# <<<<<< listened variables <<<<<<


# >>>>>> face recognition module >>>>>>
def face_recog_launch():
    member_table_name = 'member'
    customer_table_name = 'customer'
    fr_db_conn = get_db_conn()
    mf_data = get_mf_data(fr_db_conn, member_table_name)

    pp(mf_data)


# <<<<<< face recognition module <<<<<<

# >>>>>> mot module >>>>>>
def mot_pretend():
    global fr_update_index
    sleep_interval = 5

    flag = True
    while flag:
        time.sleep(sleep_interval)
        fr_update_index += 1
        return


# <<<<<< mot module <<<<<<


if __name__ == '__main__':
    mot_thread = Thread(target=mot_pretend())
    mot_thread.start()

    face_recog_thread = Thread(target=face_recog_launch())
    face_recog_thread.start()
