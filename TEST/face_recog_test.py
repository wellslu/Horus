"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/10
"""
import pathlib
# coding: utf-8
import sys

# add project directory to path
PROJECT_DIR = str(pathlib.Path(__file__).parent.parent)  # Horus
if PROJECT_DIR is '.':
    sys.path.append('..')
else:
    sys.path.append(PROJECT_DIR)


def test_import() -> bool:
    global curr_stage

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage})- successfully import package: FaceRecog"
    print(msg)

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage}) - successfully import package: FaceRecog.Facer"
    print(msg)

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage}) - successfully import package: FaceRecog.thirdparty.IIIDDFA"
    print(msg)

    return True


def test_face_recognition() -> bool:
    global curr_stage
    from FaceRecog.Facer.ult import load_pkl
    from FaceRecog.Facer.shortcut import get_face_grid_from_portrait
    from FaceRecog.Facer import FaceCapturer
    from FaceRecog.Facer import LMKScanner

    img = load_pkl(img_pkl_path)

    face_capturer = FaceCapturer()
    face_capturer.load_detector()

    lmk_scanner = LMKScanner()
    lmk_scanner.load_detector()

    face_grid = get_face_grid_from_portrait(img, face_capturer, lmk_scanner)
    if face_grid is None:
        return False

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage}) - successfully get face grid from image. Face Grid Shape: {face_grid.shape}"
    print(msg)

    from FaceRecog.thirdparty.IIIDDFA.get_pose import get_pose
    face_pose = get_pose(face_grid)
    if face_pose is None:
        return False

    yaw, pitch, roll = face_pose

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage}) - successfully get face pose from image. Yaw: {yaw}  Pitch: {pitch} Roll: {roll}"
    print(msg)

    from FaceRecog.Facer import AGFaceRecog
    ag_face_recog = AGFaceRecog()
    face_encode = ag_face_recog.get_face_encode(face_grid)
    if face_encode is None:
        return False

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage}) - successfully get face encode"
    print(msg)

    return True


def main():
    check = test_import()
    if not check:
        print(FAILED)
        return

    check = test_face_recognition()
    if not check:
        print(FAILED)
        return

    print(SUCCESS)


if __name__ == '__main__':
    stage = 6
    curr_stage = 0
    img_pkl_path = 'test_img/puff_guerlain.pkl'
    FAILED = '[VITAL] - Environment setting failed!'
    SUCCESS = '[VITAL] - Environment setting succeed!'

    main()
