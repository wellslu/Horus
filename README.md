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
- https://drive.google.com/uc?id=1WxPH6WgMPQeOgrkqEu72puAxG82FRb__

### Prerequisite
```
```

### How to use
```
```
<br>

## II. PERSON REID

### Folder : ```ReID```

### Prerequisite
```shell script
pip install -r requirements.txt
```

### How to use
####  `ReID.utils.get_data` 
```python
from ReID.utils import get_data
```
####  `ReID.reid_pipeline.Agent` 
Keep track of DB data and send back the people who have exceeded the threshold.
```python
from ReID.reid_pipeline import Agent

update_freq = 5 # second
max_epoch = 10000
db_conn = YOUR DB CONNECT

def get_latest_cus_df():
    """write your own load data methon. (return: pd.dataframe)"""
    return data
    
reid_agent = Agent(
            output_folder="ReID/feature",
            model_file="ReID/pretrain",
            example_img="TEST/test_img/reid_example.png",
            first_check_frame=12, 
            second_check_frame=50,
            timeout=600,
            frame_dead_num=10
)

epoch = 0
while True:
    epoch_start_time = time.time()
    new_data = get_latest_cus_df()
    while new_data.shape[0] == 0:
        time.sleep(update_freq)
        new_data = get_latest_cus_df()

    # 導入新資料，偵測到的新資料會自動加入到 reid_agent.task_queue 中等待
    reid_agent.get_new_update(new_data)

    
    if reid_agent.task_queue.qsize()!=0:
        print(f'[Reid][INFO] - working on epoch{epoch}/{max_epoch}')
        reid_agent.run()
            
    elif len(reid_agent.update_ls) != 0:
        print(f'[Reid][INFO] - updating on epoch{epoch}/{max_epoch} - {reid_agent.update_ls}')

        while get_latest_cus_status() == False:
            time.sleep(2)
                

        exe_query_many(db_conn,
                            query="UPDATE customer SET `last_cid` = %s WHERE `cid` = %s",
                            data=[(v,i) for i,v in reid_agent.update_ls])
        db_conn.commit()
        if len(reid_agent.update_ls) == 0:
            reid_agent.clear_update_ls()

    else:
        print(f'[Reid][INFO] - waiting on epoch{epoch}/{max_epoch}')
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
