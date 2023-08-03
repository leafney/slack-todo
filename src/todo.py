#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
-------------------------------
@File    : todo.py
@Author  : leafney
@Github  : https://github.com/leafney
@Time    : 2023-08-03 15:34:31
@Version : v0.1.0
@Desc    : 
-------------------------------
'''

import ssl

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import config as vars


class SlackTodo:

    def __init__(self,token='') -> None:
        if not token:
            token = vars.SLACK_BOT_TOKEN
        
        # unable to get local issuer certificate
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        proxy=None
        if vars.PROXY:
            proxy= vars.PROXY
        
        self.client=WebClient(token=token,
                              proxy=proxy,
                              ssl=ssl_context)
        
        pass

    def post_message(self,channel:str,msg:str):
        """
        向指定频道发送消息
        """
        try:
            resp= self.client.chat_postMessage(channel=channel,text=msg)
            print(resp)

        except SlackApiError as e:
            ok= e.response['ok']
            print(ok)
            print(e)


    def get_channel_history_messages(self,channel):
        """
        获取频道历史消息
        """

        result = self.client.conversations_history(channel=channel)
        history_list=result.get('messages',[])
        print(history_list)

        pass

    