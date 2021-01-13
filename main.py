# coding: utf-8
import time
from threading import Thread

from FaceRecog.horus_fr_api import get_mf_data, do_face_recog
from FaceRecog.horus_toolkit.db_tool import get_db_conn
from FaceRecog.horus_toolkit import FaceRecogHelper
from FaceRecog.horus_toolkit import get_face_recog_helper
from FaceRecog.Facer.shortcut import get_face_capturer, get_lmk_scanner, get_ag_face_recog
from FaceRecog.horus_toolkit import UpdateTimer
from FaceRecog.horus_toolkit import sec_to_hms

from pprint import pprint as pp

# >>>>>> listened variables >>>>>>
fr_uidx = 0


# <<<<<< listened variables <<<<<<


# >>>>>> re-id module >>>>>>
# TODO re-id entry-point
# <<<<<< re-id module <<<<<<


# >>>>>> face recognition module >>>>>>
def launch_face_recog():
    msg = '[INFO] - face recog thread start.'
    print(msg)

    # const var
    member_table_name = 'member'
    customer_table_name = 'customer'
    listen_duration = 0.5  # minutes
    listen_duration *= 60
    print(listen_duration)

    # pre-work (about 4 sec)
    fr_db_conn = get_db_conn()
    face_capturer = get_face_capturer()
    lmk_scanner = get_lmk_scanner()
    ag_face_recog = get_ag_face_recog()
    mf_data = get_mf_data(fr_db_conn, member_table_name)
    fr_helper = get_face_recog_helper(face_capturer,
                                      lmk_scanner,
                                      ag_face_recog,
                                      mf_data,
                                      fr_db_conn,
                                      member_table_name,
                                      customer_table_name)

    # face recog work
    last_fr_uidx = fr_uidx
    u_timer = UpdateTimer()

    work_flag = True
    while work_flag:
        # check update status
        if fr_uidx != last_fr_uidx:
            print(f"prepare to work, nud: {sec_to_hms(u_timer.no_update_duration())} \n")

            # do face recognition
            fr_helper.recognize()

            last_fr_uidx = fr_uidx
            u_timer.reset()
            # work_flag = False  # only do 1 time

        else:
            # print('wait for update...')
            pass

        # check no update duration
        if u_timer.no_update_duration() > listen_duration:
            work_flag = False
            duration_str = sec_to_hms(u_timer.no_update_duration())
            msg = f"[VITAL] - The database has not updated for {duration_str}, prepare to close job. \n"
            print(msg)

    msg = f"[VITAL] - face recog thread finish."
    print(msg)


# <<<<<< face recognition module <<<<<<


# >>>>>> mot module >>>>>>
# TODO mot entry-point
# <<<<<< mot module <<<<<<


# >>>>>> fake mot module >>>>>>
def fake_mot():
    global fr_uidx

    msg = '[INFO] - mot thread start.\n'
    print(msg)

    sleep_interval = 5

    flag = True
    while flag:
        time.sleep(sleep_interval)
        fr_uidx += 1
        flag = False  # ***

    msg = '[INFO] - mot thread finished. \n'
    print(msg)


# <<<<<< fake mot module <<<<<<


if __name__ == '__main__':
    mot_thread = Thread(target=fake_mot)
    mot_thread.start()

    face_recog_thread = Thread(target=launch_face_recog())
    face_recog_thread.start()
