import os
import gdown

def get_jde_pt():
    if not os.path.exists('JDE/weights'):
        os.mkdir('JDE/weights')
        print('make dir name weights')
    if not os.path.exists('JDE/weights/weight.pt'):
        dataset_url = 'https://drive.google.com/uc?id=1S21sV5Z0p5zo8MRjPZIbDz1Cu8l23uSa'
        weight_path = 'JDE/weights/weight.pt'
        print('start downloading dataset ...')
        gdown.download(dataset_url, weight_path, quiet=False)
        print(f"the weight is download at: {weight_path}")