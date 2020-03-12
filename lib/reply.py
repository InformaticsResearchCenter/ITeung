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
    replymsg = getNotFoundMessage()
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

def getNotFoundMessage():
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM notfound_message ORDER BY RAND() LIMIT 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content

def getErrorMessage():
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM error_message ORDER BY RAND() LIMIT 1"
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

def getNumberGroup(num):
    db = dbConnect()
    sql = "SELECT group_id from group_auth where number = '%s'"%(num)
    group_id = ''
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            group_id = rows[0]
        else:
            group_id=None
    return group_id


def getAuth(group, module):
    db = dbConnect()
    sql = "SELECT * from number_auth where group_id = %s AND modul = '%s'"%(group, module)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.rowcount
    if rows:
        return True
    else:
        return False

def getReplyAuth():
    db = dbConnect()
    sql = "SELECT reply_message FROM reply_auth ORDER BY RAND() LIMIT 1"
    content = ''
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            content=rows[0]
    return content