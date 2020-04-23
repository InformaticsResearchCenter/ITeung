# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:32:40 2020

@author: rolly
"""
import config, re
from ftfy import fix_encoding
from lib import times

def normalize(message):
    # msg=message.encode('latin1').decode('utf8')
    msg=fix_encoding(message)
    msg=msg.lower()
    msg=msg.replace(',',' ')
    # msg=msg.replace('\n','')
    msg=msg.replace('.',' ')
    msg=msg.replace("'",'')
    msg=msg.replace('?',' ')
    msg=msg.replace('!',' ')
    msg=msg.replace('(',' ')
    msg=msg.replace(')',' ')
    msg=msg.replace(':',' ')
    msg=msg.replace(';',' ')
    msg=msg.replace('*',' ')
    msg=msg.replace('&',' ')
    msg=msg.replace('^',' ')
    msg=msg.replace('%',' ')
    msg=msg.replace('/',' ')
    msg=msg.replace('[',' ')
    msg=msg.replace(']',' ')
    msg=msg.replace('\\','')
    msg=msg.replace('hari ini','hari '+times.getCurrentDay())
    msg=msg.replace('sekarang','hari '+times.getCurrentDay())
    msg=msg.replace(config.bot_shortname,config.bot_name)
    msg=removeBackslash(msg)
    msg=msg.strip()
    return msg

def normalizeWithRegex(message):
    msg=message.split('\n')
    results=''
    for i in msg:
        result=re.sub(r"[^a-zA-Z0-9]+", ' ', i)
        results+=result
    return results

def newlineNormalize(msg):
    msg = msg.replace('\\n', '\n')
    return msg

def removeBackslash(message):
    try:
        msg=message
        backslash=True
        while backslash:
            if msg[-1] == '\\':
                msg=msg[:-1]
            if msg[-1] == '\\':
                backslash=True
            else:
                backslash=False
    except:
        msg=''
    return msg