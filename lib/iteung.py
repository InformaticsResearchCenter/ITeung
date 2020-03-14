# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:36:17 2020

@author: rolly
"""
from lib import reply,message
import config
from importlib import import_module

def get(num,msg):
    try:
        msg  = message.normalize(msg)
        msgs = list(msg.split(" "))

        if msg.find(config.bot_name) >= 0 and len(msgs) == 1:
            msgreply = reply.getOpeningMessage()
        else:
            msgreply=reply.message(msg)
            if msgreply[:2] == 'm:':
                group_id = reply.getNumberGroup(num)
                if group_id is not None:
                    status = reply.getAuth(group_id, msgreply)
                else:
                    status=False
                if status == True:
                    modulename = msgreply.split(':')[1]
                    mod=import_module('module.'+modulename)
                    wmsg=reply.getWaitingMessage(modulename)
                    #wa.typeAndSendMessage(driver,wmsg)
                    msgreply=mod.reply(msg)
                else:
                    msgreply=reply.getReplyAuth()
    except Exception as e:
        print(e)
        msgreply=reply.getErrorMessage()
        msgreply=msgreply.replace("#ERROR#", str(e))

    print(locals())

    if 'msgreply' in locals():
        if msgreply[:2] != 'm:':
            try:
                msgreply=msgreply.replace("#BOTNAME#", config.bot_name)
            except:
                msgreply="field reply not found!!"
    return msgreply