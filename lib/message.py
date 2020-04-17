# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:32:40 2020

@author: rolly
"""
import config, re
from lib import times

def normalize(message):
    msg = message.lower()
    msg=msg.replace(',',' ')
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
    msg=msg.replace('\\',' ')
    msg=msg.replace('hari ini','hari '+times.getCurrentDay())
    msg=msg.replace('sekarang','hari '+times.getCurrentDay())
    msg=msg.replace(config.bot_shortname,config.bot_name)
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