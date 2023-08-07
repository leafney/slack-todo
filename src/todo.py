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

from .utils import utils as tools

from loguru import logger
import config as vars
from model import TODO,Files 

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

    def get_channel_history_messages(self,channel,isAll:bool=True,onlyReply=True):
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
            res = self._parse_channel_history_messages(data=result.data,channel=channel,isAll=isAll,onlyReply=onlyReply)
            # data= json.dumps(res)
            # with open('tmp5.json','w') as f:
            #     f.write(data)
            
            # 保存为markdown
            # self.save_history_markdown(res)

            return res

        except SlackApiError as e:
            logger.error(e)


    def _parse_channel_history_messages(self,channel,data,isAll:bool=True,onlyReply:bool=False):
        """
        解析频道历史消息
        """
        result = []

        ok=data.get('ok')
        if ok:
            msg_list = data.get('messages',[])
            i = 0
            for m in msg_list:
                # 用于测试
                # i+=1
                # if i>10:
                #     break

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
                
                logger.info(f'解析到内容 【{m_text}】')

                item['is_bot']=is_bot
                item['msg_id']=m_msg_id
                item['type']=m_type
                item['text'] =m_text
                item['user']=m.get('user','')
                m_ts=m.get('ts','')
                m_reply_count=m.get('reply_count',0)
                item['ts']=m_ts
                item['reply_count']=m_reply_count
                item['reactions']=list(map(lambda x:x.get('name',''),m.get('reactions',[])))
                item['files']=list(map(lambda f:{"id":f['id'],"title":f['title'],"size":f['size'],"url_download":f['url_private_download'],"url_preview":f['permalink']},m.get('files',[])))
                item['team']=m.get('team','')
                
                # 获取包含的评论列表
                m_reply_list=[]
                if m_reply_count>0:
                    logger.debug(f'包含 【{m_reply_count}】条回复，开始获取')
                    m_reply_list= self.get_message_item_replies(channel=channel,ts=m_ts,onlyReply=onlyReply)
                
                item['reply_list']=m_reply_list
                result.append(item)
                tools.slp_rand_float(min=0.6,max=2.0)

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

        result = self._parse_messge_item_replies(data=resp.data,onlyReply=onlyReply)
        # self._show_json(result)
        return result

    def _parse_messge_item_replies(self,data,onlyReply:bool=False):
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
                if onlyReply:
                    if not m_parent:
                        continue
                    else:
                        is_reply=True

                m_text=m.get('text','')
                logger.info(f'包含的回复内容 【{m_text}】')

                item['is_reply']=is_reply
                item['msg_id']=m.get('client_msg_id','')
                item['type']=m.get('type','')
                item['text']=m_text
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

    def save_history_markdown(self,data):
        """
        将历史消息数据保存为markdown
        """

        result = []
        for x in data:
            x_text = x.get('text')
            x_files=x.get('files')
            info = f'- {x_text}'
            for m in x_files:
                m_title = m.get('title')
                m_url = m.get('url_download')
                info+=f" [{m_title}]({m_url})"
            result.append(info)
            for y in x.get('reply_list',[]):
                y_text=y.get('text','')
                result.append(f'  - {y_text}')
        
        logger.info('保存到markdown文件中')
        # data= json.dumps(result)
        with open('tmp9.md','w') as f:
            for line in result:
                f.write(f"{line}\n")

    def init_database(self):
        """
        初始化数据库
        """
        TODO.create_table()
        Files.create_table()
        logger.info(f'数据库初始化完成')


    def save_history_database(self,channel,isAll:bool=True,onlyReply=True):
        """
        将将历史消息数据保存到数据库
        """

        data = self.get_channel_history_messages(channel=channel,isAll=isAll,onlyReply=onlyReply)

        for x in data:
            # logger.debug(f'数据 {json.dumps(x)}')

            x_ts= x.get('ts')
            x_text = x.get('text')
            x_files=x.get('files')

            # 判断当前项是否已经处理过
            ext_count = TODO.select().where(TODO.ts==x_ts).count()
            if ext_count > 0:
                logger.info(f'数据 【{x_text}】 已被记录')
                continue

            x_unix=int(x_ts.split('.',1)[0])
            
            new_id= TODO.insert(
                        parent_id=0,
                        ts=x.get('ts',''),
                        msg_id=x.get('msg_id',''),
                        user=x.get('user',''),
                        team=x.get('team',''),
                        text=x.get('text',''),
                        reply_count=x.get('reply_count',0),
                        reactions=','.join(x.get('reactions',[])),
                        has_file = len(x.get('files',[]))>0,
                        create_unix=x_unix,
                        ).execute()

            if new_id<=0:
                logger.error(f'数据 【{x_text}】保存失败')
                continue

            # 判断是否包含文件
            for m in x_files:
                m_title=m.get('title')
                Files.create(
                    td_id=new_id,
                    file_id=m.get('id'),
                    title=m_title,
                    size=m.get('size'),
                    url_download=m.get('url_download'),
                    url_preview=m.get('url_preview'),
                )
                logger.info(f'文件 【{m_title}】记录成功')

            # 判断是否包含子项
            for y in x.get('reply_list',[]):
                # logger.debug(f'子项 {json.dumps(x)}')

                y_ts=y.get('ts')
                y_text=y.get('text')

                y_unix=int(y_ts.split('.',1)[0])

                child_id= TODO.insert(
                    parent_id=new_id,
                    ts=y_ts,
                    msg_id=y.get('msg_id',''),
                    user=y.get('user',''),
                    team=y.get('team',''),
                    text=y_text,
                    reactions=','.join(y.get('reactions',[])),
                    has_file = len(y.get('files'))>0,
                    create_unix=y_unix,
                ).execute()

                if child_id>0:
                    logger.info(f'子项 【{y_text}】记录成功')

                    y_files = y.get('files',[])
                    for z in y_files:
                        z_title=z.get('title','')
                        Files.create(
                            td_id=child_id,
                            file_id=z.get('id',''),
                            title=z_title,
                            size=z.get('size'),
                            url_download=z.get('url_download'),
                            url_preview=z.get('url_preview'),
                        )
                        logger.info(f'文件信息 【{z_title}】记录成功')
                else:
                    logger.error(f'子项 【{y_text}】记录失败')
                
                


            

            

