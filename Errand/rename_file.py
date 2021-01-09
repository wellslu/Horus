"""
author: Jet C.
GitHub: https://github.com/jet-chien
Create Date: 2021/1/10
"""
# coding: utf-8
import ntpath
import os
import random
import string

from imutils.paths import list_images

DIGIT_LOWER = list(string.digits + string.ascii_lowercase)
DIGIT_UPPER = list(string.digits + string.ascii_uppercase)
DIGIT_ALL = list(string.digits + string.ascii_letters)


def _get_file_name(base_name: str):
    tokens = base_name.split('.')
    tokens.pop()
    file_name = ''
    while tokens:
        t = tokens.pop(0)
        if len(tokens):
            file_name += f"{t}."
        else:
            file_name += t
    return file_name


def _gen_new_file_name(old_fp: str, mode: str):
    print(old_fp)
    base_name = ntpath.basename(old_fp)  # ex: puff.jpg
    prefix = old_fp.replace(base_name, '')
    print(prefix)

    file_type = base_name.split('.')[-1]
    extension = f".{file_type}"
    file_name = _get_file_name(base_name)


def _rename(rename_dict: dict):
    for old_fp, new_fp in rename_dict.items():
        os.rename(old_fp, new_fp)


def _gen_random_token(rt_len: int, char_type: str) -> str:
    if char_type is 'DL':
        char_pool = DIGIT_LOWER
    elif char_type is 'DU':
        char_pool = DIGIT_UPPER
    else:
        char_pool = DIGIT_ALL

    result = ''
    for _ in range(rt_len):
        char = random.choice(char_pool)
        result += char
    return result


def _gen_rename_random_dict(file_ls: list, rt_len: int, char_type: str):
    result = dict()
    used_rt = list()
    for i, old_fp in enumerate(file_ls, start=1):
        base_name = ntpath.basename(old_fp)
        extension = f".{base_name.split('.')[-1]}"

        flag = True
        rt = ''
        while flag:
            rt = _gen_random_token(rt_len, char_type)
            if rt not in used_rt:
                used_rt.append(rt)
                flag = False

        new_file_name = f"{rt}{extension}"
        new_fp = old_fp.replace(base_name, new_file_name)
        result[old_fp] = new_fp

    return result


def _gen_rename_order_dict(file_ls: list):
    result = dict()
    for i, old_fp in enumerate(file_ls, start=1):
        base_name = ntpath.basename(old_fp)
        extension = f".{base_name.split('.')[-1]}"
        new_file_name = f"{i}{extension}"
        new_fp = old_fp.replace(base_name, new_file_name)
        result[old_fp] = new_fp

    return result


def _gen_rename_dict(file_ls: list, mode: str, rt_len: int, char_type: str):
    if mode is 'random':
        return _gen_rename_random_dict(file_ls, rt_len, char_type)

    elif mode is 'order':
        return _gen_rename_order_dict(file_ls)


def rename_all_images(dir_path: str, mode='random', rt_len=6, char_type='DL'):
    if not os.path.exists(dir_path):
        msg = f"Directory is not existed! - {dir_path}"
        print(msg)
        return

    img_ls = list(list_images(dir_path))
    rename_dict = _gen_rename_dict(img_ls, mode, rt_len, char_type)
    # print(rename_dict)
    _rename(rename_dict)
    print('done.')


if __name__ == '__main__':
    d_path = '../TEST-IMG/jet'
    rename_all_images(d_path)

    d_path = '../TEST-IMG/lotus'
    rename_all_images(d_path)
