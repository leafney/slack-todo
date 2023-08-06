#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
-------------------------------
@File    : main.py
@Author  : leafney
@Github  : https://github.com/leafney
@Time    : 2023-08-03 15:34:59
@Version : v0.1.0
@Desc    : 
-------------------------------
'''


import src.todo as todo
import src.config as vars

if __name__ =='__main__':
    td= todo.SlackTodo(debug=True)
    c = vars.SLACK_CHANNEL

    # td.get_channel_history_messages(channel=c)

    # td.post_message(channel=c,msg='今天天气不错')

    # td.msg_add_emoji(channel=c,ts='1691052332.745439',emoji='thumbsup')

    td.get_message_item_replies(channel=c,ts='1684467528.726679')


    