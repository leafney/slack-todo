#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
-------------------------------
@File    : config.py
@Author  : leafney
@Github  : https://github.com/leafney
@Time    : 2023-08-03 15:42:52
@Version : v0.1.0
@Desc    : 配置
-------------------------------
'''

from environs import Env

env = Env()
env.read_env()

# debug mode
DEBUG=env.bool('DEBUG',True)

SLACK_BOT_TOKEN=env.str("SLACK_BOT_TOKEN")
SLACK_CHANNEL=env.str("SLACK_CHANNEL",'')

PROXY=env.str("PROXY",'')