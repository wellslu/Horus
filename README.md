# Horus
A Human Tracking System
---
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

### Prerequisite
```
```

### How to use
```
```

## II. PERSON REID

### Folder : ```ReID```

### Prerequisite
```
```

### How to use
```
```

## III. FACE RECOGNITION

### Folder : ```FaceRecog```

### Prerequisite
#### install requirements
```shell script
pip install -r requirements.txt
```
#### check environment setting
> clone Horus repository
```shell script
git clone https://github.com/jet-chien/Horus.git
```

> change directory to ```TEST```
```shell script
cd Horus/TEST
```

> run test script ```face_recog_test.py```
```shell script
python face_recog_test.py
```

> If you get message ```[VITAL] - Environment setting succeed!``` in your terminal console, congratulations! You are able to use ```FaceRecog``` module.

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
