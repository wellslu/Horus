"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/10
"""
# coding: utf-8
import pathlib

# add project directory to path
PROJECT_DIR = pathlib.Path(__file__).parent.parent  # Horus


def test_import() -> bool:
    global curr_stage
    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage})- successfully import package: FaceRecog"
    print(msg)

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage}) - successfully import package: FaceRecog.Facer"
    print(msg)

    msg = f"[INFO] ({curr_stage}/{stage}) - successfully import package: FaceRecog.thirdparty.IIIDDFA"
    print(msg)

    return True


def test_face_recognition() -> bool:
    global curr_stage
    from FaceRecog.Facer.ult.data_store import load_pkl
    from FaceRecog.Facer.shortcut import get_face_grid_from_portrait
    from FaceRecog.Facer.Detect.face_capturer import FaceCapturer
    from FaceRecog.Facer.Detect.lmk_scanner import LMKScanner

    img = load_pkl('test-img/puff_guerlain.pkl')

    face_capturer = FaceCapturer()
    face_capturer.load_detector()

    lmk_scanner = LMKScanner()
    lmk_scanner.load_detector()

    fg = get_face_grid_from_portrait(img, face_capturer, lmk_scanner)
    if fg is None:
        return False

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage}) - successfully get face grid from image"
    print(msg)

    from FaceRecog.thirdparty.IIIDDFA.get_pose import get_pose
    face_pose = get_pose(fg)
    if face_pose is None:
        return False

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{stage}) - successfully get face grid from image"
    print(msg)

    from FaceRecog.Facer import AGFaceRecog
    ag_face_recog = AGFaceRecog()
    print(ag_face_recog)




def main():
    check = test_import()
    if not check:
        print(FAILED)
        return

    check = test_face_recognition()


if __name__ == '__main__':
    stage = 7
    curr_stage = 0
    FAILED = 'Environment setting failed'
    main()
