from lib import wa
from lib import reply
from lib import message
from lib import log
from lib import redis_set_get

from importlib import import_module

import config


class Chatbot(object):
    def __init__(self):
        driver = wa.setProfile(config.profile_folder)
        wa.loginWA(driver)
        self.msgcheck=''
        self.alscheck=''
        self.numcheck=''
        while True:
            self.cekAndSendMessage(driver)

    def cekAndSendMessage(self, driver):
        if config.useemulator:
            wa.restartMemu(wa.detectphoneNotConnected(driver))
        # wa.sendOutbox(driver) is optional for bot management
        messageindex = config.message_wa_index
        alsandnumindex = config.default_alias_number_index
        try:
            wa.openMessage(driver)
            data = wa.getData(driver, message_wa_index=messageindex, default_alias_number_index=alsandnumindex)
            messageindex-=11
            alsandnumindex-=1
            isgrp= data[4]
            msg = data[3]
            als = data[2]
            grp = data[1]
            num = data[0]
            messageindex-=10
            alsandnumindex-=1
            msg=message.normalize(msg)
            msgs = list(msg.split(" "))
            if msg.find(config.bot_name) >= 0:
                if len(msgs) == 1:
                    msgreply = reply.getOpeningMessage()
                else:
                    msgreply = reply.message(msg)
                    if msgreply[:2] == 'm:':
                        modulename = msgreply.split(':')[1]
                        mod=import_module('module.' + modulename)
                        if mod.auth(data):
                            msgreply=mod.replymsg(driver, data)
                        else:
                            msgreply=reply.getReplyAuth(modulename)
        except Exception as e:
            msgreply = reply.getErrorMessage()
            msgreply = msgreply.replace("#ERROR#", str(e))

        if 'msgreply' in locals():
            if msgreply[:2] != 'm:':
                msgreply = msgreply.replace("#BOTNAME#", config.bot_name)
                try:
                    msgreply = message.newlineNormalize(msgreply)
                    redis_set_get.set(config.BOT_MANAGEMENT_NAME, msgreply, None)
                    msgreply = redis_set_get.get(config.BOT_MANAGEMENT_NAME)
                    # wa.copyToClipboard(msgreply)
                    wa.clickChatBox(driver)
                    # wa.pasteMessage(driver)
                    wa.typeMessage(driver, msgreply)
                    wa.sendMessage(driver)
                    del msgreply
                except:
                    pass

        try:
            if self.msgcheck != msg or (self.numcheck != num and self.alscheck != als):
                log.save(num=num, msg=msg, als=als, grp=grp, isgrp=isgrp, tipe='daring')
                self.msgcheck = msg
                self.numcheck = num
                self.alscheck = als
        except Exception as e:
            msgreply = reply.getErrorMessage()
            msgreply = msgreply.replace("#ERROR#", str(e))