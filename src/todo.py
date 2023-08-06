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

    def _show_json(self,res):
        """
        打印json信息
        """
        data= json.dumps(res)
        logger.debug(data)

    def post_message(self,channel:str,msg:str):
        """
        向指定频道发送消息
        """
        try:
            resp= self.client.chat_postMessage(
                                        channel=channel,
                                        text=msg,
                                        username='U0563221SBY',
                                               )
            
            print(resp)

        except SlackApiError as e:
            ok= e.response['ok']
            print(ok)
            print(e)

    def del_message(self,channel:str,ts:str):
        """
        删除指定频道中的指定消息
        """

        resp = self.client.chat_delete(
            channel=channel,
            ts=ts,
            as_user=True,
        )
        res = resp.data
        self._show_json(res)

    def get_channel_history_messages(self,channel,isAll:bool=True):
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
            # with open('tmp4.json','w') as f:
            #     f.write(data)
            
            # # 解析历史消息
            res= self.parse_channel_history_messages(data=result.data,isAll=isAll)
            data= json.dumps(res)
            with open('tmp5.json','w') as f:
                f.write(data)
            


        except SlackApiError as e:
            logger.error(e)


    def parse_channel_history_messages(self,data,isAll:bool=True):
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
                m_bot_id=m.get('bot_id')
                is_bot=False
                if not m_msg_id and m_bot_id:
                    # 不是用户发布的正常消息
                    logger.info(f"消息【{m_text}】不是由用户发布的")
                    if not isAll:
                        continue
                    else:
                        is_bot=True
                        m_msg_id=''
                
                item['is_bot']=is_bot
                item['msg_id']=m_msg_id
                item['type']=m_type
                item['text'] =m_text
                item['user']=m.get('user','')
                item['ts']=m.get('ts','')
                item['reply_count']=m.get('reply_count',0)
                item['reactions']=list(map(lambda x:x.get('name',''),m.get('reactions',[])))
                item['files']=list(map(lambda f:{"id":f['id'],"title":f['title'],"size":f['size'],"url_download":f['url_private_download'],"url_preview":f['permalink']},m.get('files',[])))
                item['team']=m.get('team','')
                result.append(item)

                # 获取包含的评论列表

        return result

    def get_message_item_replies(self,channel,ts:str,onlyReply:bool=False):
        """
        获取消息项的回复列表
        """

        resp=self.client.conversations_replies(
            channel=channel,
            ts=ts,
            include_all_metadata=True,
        )
        res = resp.data
        self._show_json(res)

        result = self.parse_messge_item_replies(data=resp.data,onlyReply=onlyReply)
        self._show_json(result)

    def parse_messge_item_replies(self,data,onlyReply:bool=False):
        """
        解析消息项的回复列表
        """
        result = []

        ok=data.get('ok')
        if ok:
            msg_list = data.get('messages',[])
            for m in msg_list:
                item={}
                is_reply=False
                m_parent = m.get('parent_user_id')
                if m_parent:
                    if onlyReply:
                        continue
                    else:
                        is_reply=True

                item['is_reply']=is_reply
                item['msg_id']=m.get('client_msg_id','')
                item['type']=m.get('type','')
                item['text']=m.get('text','')
                item['user']=m.get('user','')
                item['ts']=m.get('ts','')
                item['team']=m.get('team','')
                item['reactions']=list(map(lambda x:x.get('name',''),m.get('reactions',[])))
                item['files']=list(map(lambda f:{"id":f['id'],"title":f['title'],"size":f['size'],"url_download":f['url_private_download'],"url_preview":f['permalink']},m.get('files',[])))
                result.append(item)

        return result

    def msg_add_emoji(self,channel,ts:str,emoji:str):
        """
        添加emoji表情
        """

        resp = self.client.reactions_add(
            channel=channel,
            name=emoji,
            timestamp=ts,
        )
        res = resp.data
        self._show_json(res)

    def msg_get_emoji_list(self,channel,ts:str):
        """
        获取指定消息包含的所有emoji表情列表
        """

        resp = self.client.reactions_get(
            channel=channel,
            timestamp=ts,
        )
        res = resp.data
        self._show_json(res)

    def msg_rmv_emoji(self,channel,ts:str,emoji:str):
        """
        移除指定消息包含的指定emoji表情
        """

        resp = self.client.reactions_remove(
            channel=channel,
            name=emoji,
            timestamp=ts,
        )
        res = resp.data
        self._show_json(res)

    