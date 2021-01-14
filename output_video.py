"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/14
"""
# coding: utf-8
import ntpath
from typing import Union
import cv2
from tqdm import tqdm
from imutils.paths import list_images

def mk_video(video):
    print('start')
    vt = VideoTool()
    origin_video = vt.get_video_meta(f'results/{video}')
    print(origin_video)
    vt.images_to_video('results/frame', 'output.mp4', 60)

class VideoTool:
    CLIP_FILE_INDENT = 3
    CLIP_DURATION = 60
    OUTPUT_DEFAULT_FPS = 24

    @staticmethod
    def get_video_name(f: str) -> (str, str):
        f_data = ntpath.basename(f).split('.')
        return f_data[0], f_data[-1]

    @staticmethod
    def get_fourcc(fn: str) -> int:
        _, ext = VideoTool.get_video_name(fn)
        if ext == 'mp4':
            return cv2.VideoWriter_fourcc(*'mp4v')

        elif ext == 'avi':
            return cv2.VideoWriter_fourcc(*'XVID')

        else:
            return cv2.VideoWriter_fourcc(*'mp4v')

    @staticmethod
    def images_to_video(img_list: Union[str, list], output_path: str, fps=OUTPUT_DEFAULT_FPS):
        img_path_ls = list()
        if isinstance(img_list, str):
            img_path_ls = list(list_images(img_list))
            img_path_ls.sort()

        msg = "loading images..."
        print(msg)
        img_queue = list()
        for img_path in tqdm(img_path_ls):
            img_queue.append(cv2.imread(img_path))

        fourcc = VideoTool.get_fourcc(output_path)
        height, width, _ = img_queue[0].shape
        size = (width, height)
        out = cv2.VideoWriter(output_path, fourcc, fps, size)

        msg = "writing images..."
        print(msg)
        for frame in tqdm(img_queue):
            out.write(frame)

        out.release()

    @staticmethod
    def get_video_meta(video_file: str) -> dict:
        result = dict()
        v = cv2.VideoCapture(video_file)
        width = int(v.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(v.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = v.get(cv2.CAP_PROP_FPS)
        result['width'] = width
        result['height'] = height
        result['fps'] = fps

        return result


if __name__ == '__main__':
    print('start')
    vt = VideoTool()
    origin_video = vt.get_video_meta('results/video_2.mp4')
    print(origin_video)
    vt.images_to_video('results/frame', 'output.mp4', 60)
