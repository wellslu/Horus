import numpy as np
import cv2
import os
import time
import pandas as pd
from JDE.utils.utils import mkdir_if_missing
from JDE.utils.sql import SQL

def tlwhs_to_tlbrs(tlwhs):
    tlbrs = np.copy(tlwhs)
    if len(tlbrs) == 0:
        return tlbrs
    tlbrs[:, 2] += tlwhs[:, 0]
    tlbrs[:, 3] += tlwhs[:, 1]
    return tlbrs


def get_color(idx):
    idx = idx * 3
    color = ((37 * idx) % 255, (17 * idx) % 255, (29 * idx) % 255)

    return color


def resize_image(image, max_size=800):
    if max(image.shape[:2]) > max_size:
        scale = float(max_size) / max(image.shape[:2])
        image = cv2.resize(image, None, fx=scale, fy=scale)
    return image


def plot_tracking(image, cid_png, tlwhs, obj_ids, sql, opt, scores=None, frame_id=0, fps=0., ids2=None):
    opt.customer[1] = False
    customer_table = pd.DataFrame(sql.read_customer_table())

    im = np.ascontiguousarray(np.copy(image))
    im_h, im_w = im.shape[:2]

    top_view = np.zeros([im_w, im_w, 3], dtype=np.uint8) + 255

    text_scale = max(1.2, image.shape[1] / 1600.)
    text_thickness = 2 if text_scale > 1.1 else 2
    line_thickness = max(1, int(image.shape[1] / 500.))

    radius = max(5, int(im_w / 140.))
    cv2.putText(im, 'frame: %d fps: %.2f num: %d' % (frame_id, fps, len(tlwhs)),
                (0, int(15 * text_scale)), cv2.FONT_HERSHEY_PLAIN, text_scale, (0, 0, 255), thickness=2)

    # 先截下每個人在每一侦的照片&更新資料庫
    for i, tlwh in enumerate(tlwhs):
        x1, y1, w, h = tlwh
        obj_id = obj_ids[i]
        mkdir_if_missing(cid_png + f'/{obj_id}')
        cv2.imwrite(os.path.join(cid_png + f'/{obj_id}', f'{frame_id}.png'),
                    im[int(y1 if y1 > 0 else 0): int(y1 + h if y1 + h > 0 else 0),
                    int(x1 if x1 > 0 else 0): int(x1 + w if x1 + w > 0 else 0)])
        if len(customer_table) != 0 and len(customer_table[customer_table['cid'] == obj_id]) != 0:
            sql_code = f'''UPDATE customer 
                                        SET leave_time={frame_id}
                                        WHERE cid=\'{obj_id}\''''
            flag = True
            while flag:
                try:
                    sql.write_customer_table(sql_code)
                    flag = False
                except Exception as e :
                    print(e)
                    time.sleep(0.2)
                    sql = SQL()
            
        else:
            sql_code = f'''INSERT INTO `customer` (`cid`, `customer_img`, `enter_time`, `leave_time`) 
                                        VALUES (\'{obj_id}\', \'results/cid_png/{obj_id}\', {frame_id}, {frame_id})'''
            sql.write_customer_table(sql_code)
    for i, tlwh in enumerate(tlwhs):
        x1, y1, w, h = tlwh
        intbox = tuple(map(int, (x1, y1, x1 + w, y1 + h)))
        obj_id = obj_ids[i]
        id_text = '{}'.format(obj_id)
        if len(customer_table) == 0:
            df = pd.DataFrame()
        else:
            df = customer_table[customer_table['cid'] == obj_id]
        if len(df) != 0:
            mid = list(df['mid'])[0]
        else:
            mid = None
        if len(df) != 0 and list(df['last_cid'])[0] is not None and list(df['last_cid'])[0] != -1 and not np.isnan(list(df['last_cid'])[0]):
            id_text = str(list(df['last_cid'])[0])
        if ids2 is not None:
            id_text = id_text + ', {}'.format(int(ids2[i]))
        _line_thickness = 1 if obj_id <= 0 else line_thickness
        color = get_color(abs(int(str(obj_id)[-1])))
        if mid is None:
            cv2.rectangle(im, intbox[0:2], intbox[2:4], color=color, thickness=line_thickness)
            cv2.putText(im, str(id_text), (intbox[0], intbox[1] + 30), cv2.FONT_HERSHEY_PLAIN,
                        text_scale, (0, 0, 255), thickness=text_thickness)
        else:
            cv2.rectangle(im, intbox[0:2], intbox[2:4], (208, 216, 129), thickness=line_thickness)
            cv2.putText(im, f'cid : {id_text}   mid : {mid}', (intbox[0], intbox[1] + 30),
                        cv2.FONT_HERSHEY_PLAIN, text_scale, (208, 216, 129), thickness=text_thickness)
    opt.customer[0] = customer_table
    opt.customer[1] = True
    return im


def plot_trajectory(image, tlwhs, track_ids):
    image = image.copy()
    for one_tlwhs, track_id in zip(tlwhs, track_ids):
        color = get_color(int(track_id))
        for tlwh in one_tlwhs:
            x1, y1, w, h = tuple(map(int, tlwh))
            cv2.circle(image, (int(x1 + 0.5 * w), int(y1 + h)), 2, color, thickness=2)

    return image


def plot_detections(image, tlbrs, scores=None, color=(255, 0, 0), ids=None):
    im = np.copy(image)
    text_scale = max(1, image.shape[1] / 800.)
    thickness = 2 if text_scale > 1.3 else 1
    for i, det in enumerate(tlbrs):
        x1, y1, x2, y2 = np.asarray(det[:4], dtype=np.int)
        if len(det) >= 7:
            label = 'det' if det[5] > 0 else 'trk'
            if ids is not None:
                text = '{}# {:.2f}: {:d}'.format(label, det[6], ids[i])
                cv2.putText(im, text, (x1, y1 + 30), cv2.FONT_HERSHEY_PLAIN, text_scale, (0, 255, 255),
                            thickness=thickness)
            else:
                text = '{}# {:.2f}'.format(label, det[6])

        if scores is not None:
            text = '{:.2f}'.format(scores[i])
            cv2.putText(im, text, (x1, y1 + 30), cv2.FONT_HERSHEY_PLAIN, text_scale, (0, 255, 255),
                        thickness=thickness)

        cv2.rectangle(im, (x1, y1), (x2, y2), color, 2)

    return im
