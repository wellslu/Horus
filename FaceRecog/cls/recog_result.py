"""
author: Jet Chien
GitHub: https://github.com/jet-chien
Create Date: 2021/1/13
"""
# coding: utf-8
from pprint import pformat
from typing import Union, Any


class RecogResult:
    def __init__(self, status: bool, has_member: bool, hl_member: Union[str, Any], member_cand: list,
                 tag=None, error_code=None, error_msg=None, event_flag=None, exe=None):
        self.status = status
        self.has_member = has_member
        self.ml_member = hl_member
        self.member_cand = member_cand

        # optional
        self.tag = tag
        self.error_code = error_code
        self.error_msg = error_msg
        self.event_flag = event_flag
        self.exe = exe

    def __str__(self):
        if self.status:
            s = f"     Status : {self.status}\n" \
                f" Has Member : {self.has_member}\n" \
                f"  HL Member : {self.ml_member}\n" \
                f"Member Cand : \n\t{pformat(self.member_cand, indent=4)}\n"
        else:
            s = f"    Status : {self.status}\n" \
                f"Error Code : {self.error_code}\n" \
                f"Error Code : {self.error_code}\n" \
                f"Error MSG  : {self.error_msg}\n" \
                f"Event Flag : {self.event_flag}\n" \
                f"Exception  : {self.exe}\n"

        return s

