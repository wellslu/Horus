"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8
import random
import string

DIGIT_LOWER = list(string.digits + string.ascii_lowercase)
DIGIT_UPPER = list(string.digits + string.ascii_uppercase)
DIGIT_ALL = list(string.digits + string.ascii_letters)


def gen_random_token(rt_len: int, char_type='DL') -> str:
    """
    optional arguments - char_type:
        -   DL  : Digital String with Lowercase Letters
        -   DU  : Digital String with Uppercase Letters
        -   ALL : Digital String with All Cases of Letters

    :param rt_len: int
    :param char_type: str
    :return:
    """
    if char_type == 'DL':
        char_pool = DIGIT_LOWER
    elif char_type == 'DU':
        char_pool = DIGIT_UPPER
    else:
        char_pool = DIGIT_ALL

    result = ''
    for _ in range(rt_len):
        char = random.choice(char_pool)
        result += char

    return result
