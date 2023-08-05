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

from loguru import logger
import config as vars
import sys
import json

class SlackTodo:

    def __init__(self,token='',debug:bool=False) -> None:
        # 调试模式
        if not debug:
            logger.remove()
            logger.add(sys.stderr, level="INFO",format='<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | - <level>{message}</level>')
        
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

        try:
            result = self.client.conversations_history(
                channel=channel,
                include_all_metadata=True, # 包含所有元数据
                # inclusive=True, # 包含最早或最新消息
                limit=1000, # 返回的最大消息条数
                )
            # history_list=result.get('messages',[])
            
            # 将历史消息保存到本地文件中
            # data= json.dumps(result.data)
            # print(data)
            # with open('tmp2.json','w') as f:
            #     f.write(data)
            
            # 解析历史消息
            res= self.parse_channel_history_messages(result.data)
            data= json.dumps(res)
            with open('tmp3.json','w') as f:
                f.write(data)
            
            # for x in res:
            #     logger.info(x)


        except SlackApiError as e:
            logger.error(e)


    def parse_channel_history_messages(self,data):
        """
        解析频道历史消息
        """
        result = []

        ok=data.get('ok')
        if ok:
            msg_list = data.get('messages',[])
            for m in msg_list:
                item = {}
                m_type = m.get('type','')
                m_text= m.get('text','')
                m_msg_id=m.get('client_msg_id')
                if not m_msg_id:
                    # 不是用户发布的正常消息
                    logger.info(f"消息【{m_text}】不是由用户发布的")
                    continue
                    
                item['id']=m_msg_id
                item['type']=m_type
                item['text'] =m_text
                item['user']=m.get('user','')
                item['ts']=m.get('ts','')
                item['reply_count']=m.get('reply_count',0)
                item['reactions']=list(map(lambda x:x.get('name',''),m.get('reactions',[])))
                m_files= list(map(lambda f:{"id":f['id'],"title":f['title'],"size":f['size'],"url_download":f['url_private_download'],"url_preview":f['permalink']},m.get('files',[])))
                item['files']=m_files
                result.append(item)

        return result

    