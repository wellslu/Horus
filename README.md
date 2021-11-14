# Horus
A Human Tracking System
<hr>
<br>

# Download the src code of Horus
#### Horus contains a submodule - [Facer](https://github.com/jet-chien/Facer). For downloading the whole source code, please use these command:
```shell script
git clone --recurse-submodules https://github.com/jet-chien/Horus.git
```
#### or
```shell script
git clone --recurse-submodules git@github.com:jet-chien/Facer.git
``` 


<br>


# Dev Environment
### Database
> MySQL 8.0
### Python
> anaconda - python 3.7.9
```bash
conda create --name horus python=3.7 -y
```
<br>

# Trinity Module
## I. MOT TRACKING

### Folder : ```JDE```

### Weight
- https://drive.google.com/file/d/1nlnuYfGNuHWZztQHXwVZSL_FvfE551pA

### Prerequisite
```shell script
pip install -r requirements.txt
```

### How to use
```shell script
python (main_file).py --input-video path/to/your/input/video --weights path/to/model/weights
               --output-format video --output-root path/to/output/root
```

### reference
https://github.com/Zhongdao/Towards-Realtime-MOT
<br>

## II. PERSON REID

### Folder : ```ReID```

### Prerequisite
```shell script
pip install -r requirements.txt
```

### How to use
####  1. `ReID.utils.get_data` 
download pretrain model on google drive.
```python
from ReID.utils import get_data

get_data(path="pretrain")
```
####  2. `ReID.reid.ReidMatch`
Modules that use models to compute photos
```python
from ReID.reid import ReidMatch

demo = ReidMatch(model_file="ReID/pretrain_model",
                 example_img="ReID/predict/img_example.png", # image to warm up model.
                 parallel=False)

# 使用 Reid 模型將行人照片轉換成特徵向量
img_path = PATH TO YOUR IMG
img_feature = demo.image_to_feature(img_path) 

# 計算 a、b 兩個向量之間的余弦相似度
demo.cosine_similarity(a, b)

# 比較兩個資料夾底下的圖片之間相似度。(本專案將比較的資料夾定義為一段追蹤，也就是說每段追蹤會存在同個資料夾底下)
result = demo.match_two_folder('data/1', 'data/2', output_folder="demo/test", 
                                result_output="demo/test/test.json", result_table_output="demo/test/test.csv", 
                                sim_threshold=0.8, sup_threshold=0.9, sample_nums=5, sample_in_bin=3)
                                
# 比較路徑底下的所有資料夾間的關係。(本專案將比較的資料夾定義為一段追蹤，也就是說每段追蹤會存在同個資料夾底下)
df, gp_result = demo.match_folders_under_path(root_path="data", output_path="demo/pairtest",
                                       sim_threshold=0.6, sup_threshold=0.7, sample_nums=5, sample_in_bin=3) 
```
####  3. `ReID.reid_pipeline.Agent` 
Keep track of DB data and send back the people who have exceeded the threshold.
```python
from ReID.reid_pipeline import Agent


update_freq = 5 # second
max_epoch = 10000

def get_latest_cus_df():
    """write your own load data methon. (return: pd.dataframe)"""
    return data
    
reid_agent = Agent(
            output_folder="ReID/feature", # 已跑過照片特徵儲存路徑。
            model_file="ReID/pretrain", # 預訓練模型路徑
            example_img="TEST/test_img/reid_example.png", # Reid 模型的測試照片
            first_check_frame=12, # 第一次檢查門檻
            second_check_frame=50, # 第二次檢查門檻
            timeout=600, # 斷開時間
            frame_dead_num=10 # 超過 10 個 frame 未更新時認定該追蹤結束。
)

epoch = 0
while True:
    epoch_start_time = time.time()
    new_data = get_latest_cus_df()
    while new_data.shape[0] == 0:
        time.sleep(update_freq)
        new_data = get_latest_cus_df()

    # 導入新資料，偵測到的新資料會自動加入到任務列表(reid_agent.task_queue)中等待
    reid_agent.get_new_update(new_data)

    # 當任務列表(reid_agent.task_queue)中有任務，就啟動模型計算新資料與舊資料間的相似度，將結果加入更新列表(reid_agent.update_ls)。
    if reid_agent.task_queue.qsize()!=0:
        print(f'[Reid][INFO] - working on epoch{epoch}/{max_epoch}')
        reid_agent.run()

    # 當更新列表(reid_agent.update_ls)中有待更新的任務，更新新的資料到 DB。
    if len(reid_agent.update_ls) != 0:
        print(f'[Reid][INFO] - updating on epoch{epoch}/{max_epoch} - {reid_agent.update_ls}')

        while get_latest_cus_status() == False:
            time.sleep(2)
                
        """ write your DB update flow"""
        
        reid_agent.clear_update_ls()

    # 當 epoch 執行時間 小於 update_freq，等待到 update_freq 時間到
    epoch_run_time = time.time() - epoch_start_time
    if  epoch_run_time < update_freq:
        time.sleep(update_freq - epoch_run_time)
    
    # 紀錄第幾個 epoch，當達到最大值。則停止追蹤
    epoch+=1
    if epoch > max_epoch:
        break
            
```
<br>

## III. FACE RECOGNITION

### Folder : ```FaceRecog```

### Prerequisite
#### install requirements
```shell script
pip install -r requirements.txt
```
<br>

#### check environment setting
> clone Horus repository
```shell script
git clone https://github.com/jet-chien/Horus.git
```
<br>

> change directory to ```TEST```
```shell script
cd Horus/TEST
```
<br>

> run test script ```face_recog_test.py```
```shell script
python face_recog_test.py
```
<br>

> If you get message ```[VITAL] - Environment setting succeed!``` in your terminal console, congratulations! You are able to use ```FaceRecog``` module.
<br>

### How to use
#### to fetch face grid (face block or face roi) from img
```python
# a tool to capture face from image 
from FaceRecog.Facer import FaceCapturer

# a tool to scan face landmarks from image
from FaceRecog.Facer import LMKScanner

# cheat function
from FaceRecog.Facer.shortcut import get_face_grid_from_portrait

face_capturer = FaceCapturer()
face_capturer.load_detector()

lmk_scanner = LMKScanner()
lmk_scanner.load_detector()

img = 'path_to_img' # it can be ndarray as well

face_grid = get_face_grid_from_portrait(img, face_capturer, lmk_scanner)

# view face grid
from FaceRecog.Facer.ult import show
show(face_grid)
```

#### verify faces
```python
# Face Recognition tool, by Adam Geitgey, https://pypi.org/project/face-recognition/
from FaceRecog.Facer import AGFaceRecog

ag_face_recog = AGFaceRecog()
face_encode = ag_face_recog.get_face_encode(face_grid)
result, similarity = ag_face_recog.verify_member(ls_of_know_face_encode, unknown_face_encode)
```
<br>

# Demo Video
[![IMAGE ALT TEXT HERE](http://img.youtube.com/vi/jHEIXSSqw_I/0.jpg)](https://www.youtube.com/watch?v=jHEIXSSqw_I)
<br>
