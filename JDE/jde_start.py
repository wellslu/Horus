import logging
from JDE.utils.utils import *
from JDE.utils.log import logger
from JDE.utils.timer import Timer
from JDE.utils.parse_config import parse_model_cfg
import JDE.utils.datasets as datasets
from JDE.track import eval_seq
from JDE.utils.weight_gdown import get_jde_pt

logger.setLevel(logging.INFO)


def track(opt):
    result_root = opt.output_root if opt.output_root != '' else '.'
    mkdir_if_missing(result_root)

    cfg_dict = parse_model_cfg(opt.cfg)
    opt.img_size = [int(cfg_dict[0]['width']), int(cfg_dict[0]['height'])]

    # run tracking
    timer = Timer()
    accs = []
    n_frame = 0

    logger.info('Starting tracking...')
    dataloader = datasets.LoadVideo(opt.input_video, opt.img_size)
    result_filename = os.path.join(result_root, 'results.txt')
    cid_png = os.path.join(result_root, 'cid_png')
    frame_rate = dataloader.frame_rate

    frame_dir = None if opt.output_format == 'text' else osp.join(result_root, 'frame')
    # try:
    eval_seq(opt, dataloader, 'mot', result_filename, cid_png,
             save_dir=frame_dir, show_image=False, frame_rate=frame_rate)
    # except Exception as e:
    #     logger.info(e)

    # if opt.output_format == 'video':
    #     output_video_path = osp.join(result_root, 'result.mp4')
    #     cmd_str = 'ffmpeg -f image2 -i {}/%05d.png -c:v copy {}'.format(osp.join(result_root, 'frame'),
    #                                                                     output_video_path)
    #     os.system(cmd_str)


def jde_launch(opt):
    # get jde weight
    get_jde_pt()
    print(opt, end='\n\n')

    track(opt)

if __name__ == '__main__':
    pass