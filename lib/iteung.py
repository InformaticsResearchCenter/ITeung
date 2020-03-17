# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:36:17 2020

@author: rolly
"""
from lib import reply,message,twl
import config
from importlib import import_module

def get(num,msg):
    try:
        msg  = message.normalize(msg)
        msgs = list(msg.split(" "))

        if len(msgs) == 1:
            msgreply = reply.getOpeningMessage()
        else:
            msgreply=reply.message(msg)
            if msgreply[:2] == 'm:':
                modulename = msgreply.split(':')[1]
                mod=import_module('module.'+modulename)
                msgreply=mod.replymsg(num)
    except Exception as e:
        print(e)
        msgreply=reply.getErrorMessage()
        msgreply=msgreply.replace("#ERROR#", str(e))

    if 'msgreply' in locals():
        if msgreply[:2] != 'm:':
            try:
                msgreply=msgreply.replace("#BOTNAME#", config.bot_name)
            except:
                msgreply="field reply not found!!"
    return msgreply