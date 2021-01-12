# coding: utf-8

import pathlib
from collections import namedtuple
from math import degrees, asin, sin
from typing import Union

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
import torchvision.transforms as transforms

from . import mobilenet_v1
from .utils.ddfa import ToTensorGjz, NormalizeGjz
from .utils.estimate_pose import parse_pose

STD_SIZE = 120

MODELS_DIR = f"{pathlib.Path(__file__).parent}/models"


def _workspace(args):
    # 1. load pre-tained model
    checkpoint_fp = f"{MODELS_DIR}/phase1_wpdc_vdc.pth.tar"
    arch = 'mobilenet_1'

    checkpoint = torch.load(checkpoint_fp, map_location=lambda storage, loc: storage)['state_dict']
    model = getattr(mobilenet_v1, arch)(num_classes=62)  # 62 = 12(pose) + 40(shape) +10(expression)

    model_dict = model.state_dict()

    # because the model is trained by multiple gpus, prefix module should be removed
    for k in checkpoint.keys():
        model_dict[k.replace('module.', '')] = checkpoint[k]

    model.load_state_dict(model_dict)

    if args.mode == 'gpu':
        cudnn.benchmark = True
        model = model.cuda()

    model.eval()

    # 3. forward
    transform = transforms.Compose([ToTensorGjz(), NormalizeGjz(mean=127.5, std=128)])
    for img_fp in args.files:
        img = None
        if isinstance(img_fp, str):
            img = cv2.imread(img_fp)
        elif isinstance(img_fp, np.ndarray):
            img = img_fp

        # forward: one step
        img = cv2.resize(img, dsize=(STD_SIZE, STD_SIZE), interpolation=cv2.INTER_LINEAR)
        input = transform(img).unsqueeze(0)

        with torch.no_grad():
            if args.mode == 'gpu':
                input = input.cuda()

            param = model(input)
            param = param.squeeze().cpu().numpy().flatten().astype(np.float32)

            P, pose = parse_pose(param)

            yaw = _get_abs_angle(pose[0])
            pitch = _get_abs_angle(pose[1])
            roll = _get_abs_angle(pose[2])

            return yaw, pitch, roll


def _dict2namedtuple(dictionary):
    return namedtuple('NamedTuple', dictionary.keys())(**dictionary)


def _get_abs_angle(val: float):
    return abs(degrees(asin(sin(val))))


def get_pose(img: Union[str, np.ndarray]) -> Union[tuple, None]:
    args = dict()
    args['files'] = [img]
    args['mode'] = 'cpu'  # gpu | cpu
    args['show_flg'] = False
    args['bbox_init'] = 'two'  # two | one
    args['dump_res'] = False
    args['dump_vertex'] = False
    args['dump_ply'] = False
    args['dump_pts'] = False
    args['dump_roi_box'] = False
    args['dump_pose'] = True
    args['dump_depth'] = False
    args['dump_pncc'] = False
    args['dump_paf'] = False
    args['paf_size'] = 3
    args['dump_obj'] = False
    args['dlib_bbox'] = True
    args['dlib_landmark'] = True

    # for k, v in args.items():
    #     print(f"{k} = {v}")

    try:
        return _workspace(_dict2namedtuple(args))
    except Exception as e:
        msg = f"Failed to get YPR via 3DDFA. Error: {e}"
        print(msg)
