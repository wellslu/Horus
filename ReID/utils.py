# encoding: utf-8
"""
@author: yen-nan ho
@contact: aaron1aaron2@gmail.com
@gitHub: https://github.com/aaron1aaron2
@Create Date: 2021/1/5
"""
import zipfile
import os
import shutil

__all__ = ["get_data"]

def get_data(path, file_id=None, remove_zip=True):
    import gdown

    if not file_id:
        file_id = "10YKwzUB61hIYvqXAdyMslmLPyVBCr84Z" # file_id

    dataset_url = 'https://drive.google.com/uc?id={}'.format(file_id)
    
    data_zip = os.path.join(path, "data.zip")
    if not os.path.exists(path):
        os.makedirs(path)
    
    try:
        gdown.download(dataset_url, data_zip)
    except:
        print("fail to download pretrain model, please download the data at {}".format(dataset_url))

    try:
        print('start extracting dataset ...')
        with zipfile.ZipFile(data_zip, 'r') as zf:
            zf.extractall(path)
        
        if remove_zip:
            os.remove(data_zip)
        
        shutil.move(os.path.join(path, "data"), path)
        os.remove(os.path.join(path, "data"))
        print('the dataset is extracted at: {}'.format(path))
    except:
        print("fail to extracting dataset, please check data at {}".format(data_zip))

    

    
if __name__ == "__main__":

    file_id = "10YKwzUB61hIYvqXAdyMslmLPyVBCr84Z"
    get_data(path="pretrain", file_id=file_id, remove_zip=True)


