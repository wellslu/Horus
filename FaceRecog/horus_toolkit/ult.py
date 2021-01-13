"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8
from typing import Union

from .tk_gen import gen_random_token


def gen_member_id(rt_len=4) -> Union[str, None]:
    if rt_len < 4:
        msg = '[WARN] - The length of random token must be greater or equal to 4!'
        print(msg)
        return

    return f"M-{gen_random_token(rt_len)}"
