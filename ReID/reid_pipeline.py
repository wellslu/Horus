# encoding: utf-8
"""
@author: yen-nan ho
@contact: aaron1aaron2@gmail.com
@gitHub: https://github.com/aaron1aaron2
@Create Date: 2021/1/13
"""
import sys
sys.path.append('..')

import os
import time
import pandas as pd

try:
   from queue import SimpleQueue
except ImportError:
   from queue import Queue as SimpleQueue

from .reid import ReidMatch

__all__ = ["Agent"]

class Agent:
    def __init__(self, output_folder, model_file, example_img, first_check_frame,
                 second_check_frame, timeout, frame_dead_num):
        self.output_folder = output_folder
        # time
        self.timeout = timeout
        self.start_time = time.time()
        self.last_run_time = time.time()

        # reid methon
        self.frame_dead_num = frame_dead_num
        self.first_check_frame = first_check_frame
        self.second_check_frame = second_check_frame
        self.demo = ReidMatch(model_file=model_file,
                              example_img=example_img, # image to warm up model.
                              parallel=False)
        # data update
        # self.data_track = None 
        self.blank_out_ls = []
        self.update_ls = []
        self.finish_ls = []

        self.finish_dt = {} # {cid:customer_img}
        self.track_record_dt = {} # {cid:{'leave_time':, 'customer_img':, 'count':}}

        self.task_queue = SimpleQueue() # item in queue : [(cid, customer_img)] # methon: qsize(), empty(), put(), get()

        self.customer_record = pd.DataFrame()

    def get_new_update(self, data:pd.DataFrame):
        # self.data_track = data.copy()
        new = data.copy()
        new['frame_num'] = new.leave_time - new.enter_time
        new = new[new['frame_num'] >= self.first_check_frame]
        track = new[(~new['cid'].isin(self.finish_dt.keys())) & (~new['cid'].isin(self.blank_out_ls))]

        for cid, img_path, leave_time, frame_num in track[['cid', 'customer_img', 'leave_time', 'frame_num']].values:
            if cid in self.track_record_dt.keys():
                if self.track_record_dt[cid]['leave_time'] == leave_time:
                    self.track_record_dt[cid]['count'] += 1
                else:
                    self.track_record_dt[cid]['count'] = 0

                # 判斷為結束追蹤
                if self.track_record_dt[cid]['count'] >= self.frame_dead_num:
                    self.track_record_dt.pop(cid)
                    if frame_num < 50:
                        # 未符合 50 第一次結果作廢
                        self.update_ls.append((cid, -1))
                        self.blank_out_ls.append(cid)
                    else:
                        # 符合 50 張 -> second check
                        self.task_queue.put((cid, img_path))
                        self.finish_dt.update({cid:img_path})
                        self.finish_ls.append(cid)
                    
            else:
                # first check
                self.track_record_dt.update({cid:{'img_path':img_path, 'leave_time':leave_time, 'count':0}})
                self.task_queue.put((cid, img_path))

    def run(self):
        while self.task_queue.qsize() != 0:
            self.last_run_time = time.time()

            cid, path = self.task_queue.get()

            for cid_record in self.finish_ls[::-1]:
                cid_record_path = self.finish_dt[cid_record]
                output = self.demo.match_two_folder(path, cid_record_path, output_folder=self.output_folder, 
                                                sim_threshold=0.8, sup_threshold=0.9, sample_nums=5, sample_in_bin=3)
                if output['Result']['match_result']:
                    self.update_ls.append((cid, cid_record))
                    break


if __name__ == "__main__":
    CUSTOMER = pd.read_csv('customer.csv')
    
    update_freq = 1 # second
    max_epoch = 100

    reid_agent = Agent(
        output_folder="ReID/feature",
        first_check_frame=12, 
        second_check_frame=50,
        timeout=600,
        frame_dead_num=10
    )

    epoch = 0
    while True:
        epoch_start_time = time.time()

        reid_agent.get_new_update(CUSTOMER)
        reid_agent.run()

        # 更新運行時間
        if reid_agent.timeout <= (time.time() - reid_agent.last_run_time):
            print('timeout - No operation within {} minutes'.format(reid_agent.timeout/60))
            break

        epoch_run_time = time.time() - epoch_start_time

        if  epoch_run_time < update_freq:
            time.sleep(update_freq - epoch_run_time)
        
        epoch+=1
        if epoch > max_epoch:
            break
                        