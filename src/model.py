#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
-------------------------------
@File    : model.py
@Author  : leafney
@Github  : https://github.com/leafney
@Time    : 2023-08-07 10:11:10
@Version : v0.1.0
@Desc    : sqlite3操作
-------------------------------
'''

from peewee import *
import datetime

db = SqliteDatabase('slack.db')

class TODO(Model):
    id = PrimaryKeyField()
    parent_id = IntegerField(default=0)
    ts = CharField(index=True,max_length=64)
    msg_id = CharField(default='',max_length=64)
    user = CharField(default='',max_length=64)
    team = CharField(default='',max_length=64)
    text = TextField(default='')
    reply_count =IntegerField(default=0)
    reactions = TextField(default='')
    has_file=BooleanField(default=False)
    status =  IntegerField(default=0)
    create_unix = IntegerField(default=0)
    creat_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = db
        table_name = 'todo'

class Files(Model):
    id = PrimaryKeyField()
    td_id = IntegerField()
    file_id = CharField(default='',max_length=64)
    title = CharField(default='')
    size = IntegerField()
    url_download = TextField()
    url_preview = TextField()

    class Meta:
        database = db
        table_name = 'files'


if __name__ =='__main__':
    TODO.create_table()
    Files.create_table()

