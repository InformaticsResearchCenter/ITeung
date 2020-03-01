# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:44:01 2020

@author: rolly
"""
import pymysql
import config



def dbConnect():
    db=pymysql.connect(config.db_host,config.db_username,config.db_password,config.db_name)
    return db

def message(msg):
    keygroup = getKeywordGroup(msg)
    replymsg = 'duh maap... '+config.bot_name+' ga ngerti bahasanya.... huhuhu...'
    if keygroup != '':
        if keygroup[:2] != 'm:':
            replymsg = getContentWithKeyword(keygroup)
        else:
            replymsg=keygroup
    return replymsg

def normalizeKeywords(msg):
    db = dbConnect()
    sql = "SELECT multiple_keywords FROM multi_key"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows = [item[0] for item in cur.fetchall()]
        for mkey in rows:
            keys=list(mkey.split('-'))
            if all(x in msg for x in keys):
                msg=msg+' '+mkey
    return msg
    
    
def getKeywordGroup(msg):
    msg=normalizeKeywords(msg)
    msgs = list(msg.split(" "))
    db = dbConnect()
    keygroup = ''
    for key in msgs:
        keyword=key.replace(" ", "")
        sql = "SELECT keyword_group FROM keyword WHERE keyword = '%s'"%(keyword)
        with db:
            cur=db.cursor()
            cur.execute(sql)
            rows = cur.fetchone()
            if rows is not None:
                keygroup = rows[0]
    return keygroup
    
    
def getContentWithKeyword(keyword):
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM reply WHERE keyword_group = '%s' ORDER BY RAND() LIMIT 1"%(keyword)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content

def getOpeningMessage():
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM opening_message ORDER BY RAND() LIMIT 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content

def getWaitingMessage(module):
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM waiting_message WHERE module_name = '%s' ORDER BY RAND() LIMIT 1"%(module)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content