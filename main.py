# coding: utf-8
import time
from threading import Thread

from FaceRecog.horus_fr_api import get_mf_data, do_face_recog
from FaceRecog.horus_toolkit.db_tool import get_db_conn
from FaceRecog.Facer.shortcut import get_face_capturer, get_lmk_scanner
from FaceRecog.horus_toolkit import UpdateTimer
from FaceRecog.horus_toolkit import sec_to_hms

from pprint import pprint as pp

# >>>>>> listened variables >>>>>>
fr_uidx = 0


# <<<<<< listened variables <<<<<<


# >>>>>> face recognition module >>>>>>


def face_recog_launch():
    msg = '[INFO] - face recog thread start.'
    print(msg)

    # const var
    member_table_name = 'member'
    customer_table_name = 'customer'
    listen_duration = 0.5  # minutes
    listen_duration *= listen_duration * 60

    # pre-work (about 4 sec)
    fr_db_conn = get_db_conn()
    face_capturer = get_face_capturer()
    lmk_scanner = get_lmk_scanner()
    ag_face_recog = ''
    mf_data = get_mf_data(fr_db_conn, member_table_name)

    last_fr_uidx = fr_uidx
    u_timer = UpdateTimer()

    work_flag = True
    while work_flag:
        # print(f"fr_uidx from mot : {fr_uidx}  last_fr_uidx : {last_fr_uidx} \n")

        # check update status
        if fr_uidx != last_fr_uidx:
            print(f"prepare to work, nud: {sec_to_hms(u_timer.no_update_duration())} \n")

            # to do work
            do_face_recog(face_capturer, lmk_scanner, mf_data,
                          fr_db_conn, member_table_name, customer_table_name)

            last_fr_uidx = fr_uidx
            u_timer.reset()
            # work_flag = False # ***

        else:
            # print('wait for update...')
            pass

        # check no update duration
        if u_timer.no_update_duration() > listen_duration:
            work_flag = False
            duration_str = sec_to_hms(u_timer.no_update_duration())
            msg = f"[VITAL] - The database has not updated for {duration_str}, prepare to close job. \n"
            print(msg)


# <<<<<< face recognition module <<<<<<

# >>>>>> mot module >>>>>>
def mot_pretend():
    global fr_uidx

    msg = '[INFO] - mot thread start.\n'
    print(msg)

    sleep_interval = 5

    flag = True
    while flag:
        time.sleep(sleep_interval)
        fr_uidx += 1
        # print(f"fr_uidx from mot : {fr_uidx} \n")

        # flag = False # ***

    msg = '[INFO] - mot thread finished. \n'
    print(msg)


# <<<<<< mot module <<<<<<


if __name__ == '__main__':
    mot_thread = Thread(target=mot_pretend)
    mot_thread.start()

    face_recog_thread = Thread(target=face_recog_launch)
    face_recog_thread.start()
