"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8

import time


class UpdateTimer:
    def __init__(self):
        self.last_update = time.time()

    def no_update_duration(self) -> float:
        return time.time() - self.last_update

    def reset(self):
        self.last_update = time.time()
