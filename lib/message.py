# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:32:40 2020

@author: rolly
"""
import config

def normalize(message):
    msg = message.lower()
    msg=msg.replace(',',' ')
    msg=msg.replace('.',' ')
    msg=msg.replace("'",' ')
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
    msg=msg.replace(config.bot_shortname,config.bot_name)
    msg=msg.strip()
    #message = self.splitString(tolowercase)
    return msg