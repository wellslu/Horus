# encoding: utf-8
"""
@author: yen-nan ho
@contact: aaron1aaron2@gmail.com
@gitHub: https://github.com/aaron1aaron2
@Create Date: 2021/1/5
"""

import sys
import pathlib
# add project directory to path
PROJECT_DIR = str(pathlib.Path(__file__).parent.parent)  # Horus
sys.path.append(PROJECT_DIR)


def test_import() -> bool:
    global curr_stage

    import ReID
    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{STAGE})- successfully import package: ReID"
    print(msg)

    import ReID.reid
    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{STAGE}) - successfully import package: ReID.reid"
    print(msg)

    return True


def test_reid() -> bool:
    global curr_stage
    from ReID.reid import ReidMatch

    # step1: load model
    demo = ReidMatch(model_file="../ReID/pretrain_model",
                     example_img="../ReID/predict/img_example.png", # image to warm up model.
                     parallel=False)
    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{STAGE}) - successfully load reid model"
    print(msg)

    # step2: load model
    result = demo.match_two_folder('../ReID/data/1', '../ReID/data/2', output_folder="../ReID/demo(test)", 
                                    result_output="../ReID/demo(test)/test.json", result_table_output="../ReID/demo(test)/test.csv", 
                                    sim_threshold=0.8, sup_threshold=0.9, sample_nums=5, sample_in_bin=3)

    curr_stage += 1
    msg = f"[INFO] ({curr_stage}/{STAGE}) - successfully run function - match_two_folder"
    print(msg)

    return True


def main():
    check = test_import()
    if not check:
        print(FAILED)
        return

    check = test_reid()
    if not check:
        print(FAILED)
        return

    print(SUCCESS)


if __name__ == '__main__':
    STAGE = 4
    curr_stage = 0
    FAILED = '[VITAL] - Environment setting failed!'
    SUCCESS = '[VITAL] - Environment setting succeed!'

    main()
