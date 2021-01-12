# coding: utf-8
from JDE.jde_start import jde_launch
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='demo.py')
    parser.add_argument('--cfg', type=str, default='JDE/cfg/yolov3_1088x608.cfg', help='cfg file path')
    parser.add_argument('--weights', type=str, default='JDE/weights/weight.pt', help='path to weights file')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='iou threshold required to qualify as detected')
    parser.add_argument('--conf-thres', type=float, default=0.5, help='object confidence threshold')
    parser.add_argument('--nms-thres', type=float, default=0.4, help='iou threshold for non-maximum suppression')
    parser.add_argument('--min-box-area', type=float, default=200, help='filter out tiny boxes')
    parser.add_argument('--track-buffer', type=int, default=30, help='tracking buffer')
    parser.add_argument('--input-video', type=str, default='video_2.mp4', help='expected input root path')
    parser.add_argument('--output-format', type=str, default='video', choices=['video', 'text'],
                        help='Expected output format. Video or text.')
    parser.add_argument('--output-root', type=str, default='results', help='expected output root path')
    opt = parser.parse_args()
    jde_launch(opt)