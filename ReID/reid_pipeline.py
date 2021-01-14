# encoding: utf-8
"""
@author: yen-nan ho
@contact: aaron1aaron2@gmail.com
@gitHub: https://github.com/aaron1aaron2
@Create Date: 2021/1/13
"""
import sys
sys.path.append('..')

import pandas as pd

from queue import SimpleQueue
from ReID.reid import ReidMatch

CUSTOMER = pd.read_csv('customer.csv') # 全域變數.copy()

class Agent:
    def __init__(self):
        self.finish_ls = []
        self.task_queue = SimpleQueue() 
        # item in queue : [(cid, customer_img)] | methon: qsize(), empty(), put(), get()
        self.customer_record = pd.DataFrame(columns=CUSTOMER.columns)

    def get_new_update(self):
        new_customer = CUSTOMER.copy()
        new_customer = new_customer[(new_customer.leave_time - new_customer.enter_time)>=12]
        tracking = new_customer[~new_customer['cid'].isin(FINISH_ls)]

    def main(self):

        demo = ReidMatch(model_file="ReID/pretrain_model",
                        example_img="ReID/predict/img_example.png", # image to warm up model.
                        parallel=False)

        result = demo.match_two_folder('data/1', 'data/2', output_folder="demo/test", 
                                        result_output="demo/test/test.json", result_table_output="demo/test/test.csv", 
                                        sim_threshold=0.8, sup_threshold=0.9, sample_nums=5, sample_in_bin=3)
                        
if __name__ == "__main__":
    pass