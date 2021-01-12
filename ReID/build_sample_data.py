# encoding: utf-8
"""
@author: yen-nan ho
@contact: aaron1aaron2@gmail.com
"""
import os
import random
import numpy as np
import pandas as pd

from predict.fastreid.utils.file_io import PathManager


def get_sample(input_folder, output_folder, sample_size, input_pid, output_tid) -> None:
    """
    Sample from under the `input_folder` and copy to the `output_folder`. 

    Args:
        input_folder (str): There are many document folders(Named after the PID) below the path.
        output_folder (str):  
        sample_size (int): Number of samples per output_tid.
        input_pid (int): Take the pedestrian photo under the PID document folder as the sampled data. 
                         (the PID folder must be under the path) 
        output_tid (list): TID to be given after sampling.
                         (multiple samples will be output if the length of input list is greater than 1)

    """
    track_imgs = os.listdir(os.path.join(input_folder, str(input_pid)))
    track_imgs_num = [int(i.split('.')[0]) for i in track_imgs]
    last_num = len(track_imgs)

    total_sample_size = len(output_tid) * sample_size

    sample_nums = np.random.randint(last_num, size=total_sample_size)
    sample_nums = [num for num in sample_nums if num in track_imgs_num]

    while len(sample_nums) != total_sample_size:
        new_num = np.random.randint(last_num)
        while (new_num in sample_nums) | (new_num not in track_imgs_num):
            new_num = np.random.randint(last_num)
        sample_nums.append(new_num)

    sample_nums.sort()

    print("\nsample num: {} -> {}".format(last_num, len(sample_nums)))

    output_folders = [os.path.join(output_folder, str(i)) for i in output_tid]
    for folder in output_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

    for i, path in enumerate(output_folders):
        nums = sample_nums[sample_size * i:sample_size * (i + 1)]
        print("copy file: {} -> {}\n\t\t{}".format(input_folder, path, nums))
        for num in nums:
            PathManager.copy(os.path.join(input_folder, "{}/{}.png".format(input_pid, num)),
                             os.path.join(path, "{}.png".format(num)),
                             overwrite=True)


if __name__ == "__main__":

    sample_dt = {'1': 3, '2': 3, '3': 1, '4': 2, '5': 1}  # {"input_id":"output_id"}

    # 隨機生成對應數量的
    output_nums = list(range(1, sum(sample_dt.values()) + 1))
    random.shuffle(output_nums)

    locat = 0
    for i in sample_dt:
        num = sample_dt[i]
        sample_dt[i] = output_nums[locat:locat + num]
        sample_dt[i].sort()
        locat += num

    # sample_dt -> {'1': [1, 4, 8], '2': [3, 5, 6], '4': [2, 7]}

    for pid in sample_dt:
        get_sample(
            input_folder="../JDE/results/cid_png",
            output_folder="data",
            sample_size=10,
            input_pid=pid,
            output_tid=sample_dt[pid])

    sample_ls = []
    for pid in sample_dt:
        sample_ls.extend([(i, pid) for i in sample_dt[pid]])

    df = pd.DataFrame(sample_ls)
    df.columns = ['TID', 'ReID(target)']
    df.sort_values('TID', inplace=True)

    df.to_csv('data/main.csv', index=False)
