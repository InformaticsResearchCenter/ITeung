from lib import message
from lib import reply
from lib import log
from lib import numbers

from importlib import import_module

import config

def cekAndSendMessage(message_flask, number):
    try:
        driver=''
        isgrp = 'website'
        msg = message_flask
        als = 'website'
        grp = 'website'
        num = numbers.normalize(number)
        log.save(num=num, msg=msg, als=als, grp=grp, isgrp=isgrp, tipe='website')
        data=[]
        data.append(num)
        data.append(grp)
        data.append(als)
        data.append(msg)
        data.append(isgrp)
        msg = message.normalize(msg)
        msgs = list(msg.split(" "))
        if msg.find(config.bot_name) >= 0:
            if len(msgs) == 1:
                msgreply = reply.getOpeningMessage()
            else:
                msgreply = reply.message(msg)
                if msgreply[:2] == 'm:':
                    modulename = msgreply.split(':')[1]
                    mod = import_module('module.' + modulename)
                    if mod.auth(data):
                        msgreply = mod.replymsg(driver, data)
                    else:
                        msgreply = reply.getReplyAuth(modulename)
    except Exception as e:
        msgreply = reply.getErrorMessage()
        msgreply = msgreply.replace("#ERROR#", str(e))

    if 'msgreply' in locals():
        msgreply = msgreply.replace("#BOTNAME#", config.bot_name)
        msgreply = message.newlineNormalize(msgreply)
        return msgreply
    # if 'msgreply' in locals():
    #     if msgreply[:2] != 'm:':
    #         msgreply = msgreply.replace("#BOTNAME#", config.bot_name)
    #         try:
    #             msgreply = message.newlineNormalize(msgreply)
    #             log.save(num=num, msg=msg, als=als, grp=grp, isgrp=isgrp, tipe='daring')
    #             del msgreply
    #         except:
    #             print("field reply not found!!")