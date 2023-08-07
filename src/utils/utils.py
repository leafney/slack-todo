#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
-------------------------------
@File    : utils.py
@Author  : leafney
@Github  : https://github.com/leafney
@Time    : 2023-08-07 00:00:55
@Version : v0.1.0
@Desc    : 
-------------------------------
'''

import time
from datetime import datetime
import random
import json
import os


def slp(sec=3):
    """sleep秒"""
    time.sleep(sec)


def rand_int(min: int, max: int) -> int:
    """随机返回一个数字"""
    return random.randint(min, max)

def rand_float(min:float,max:float)->float:
    """随机返回一个浮点数，保留2位小数"""
    res = random.uniform(min,max)
    return round(res,2)

def slp_rand(min:int=2,max:int=10)->None:
    """随机sleep秒"""
    sec = rand_int(min,max)
    slp(sec)

def slp_rand_float(min:float=2,max:float=10)->None:
    """随机sleep秒"""
    sec = rand_float(min,max)
    slp(sec)