from lib import wa, reply, message, auth, log
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
        try:
            wa.openMessage(driver)
            data = wa.getData(driver)
            isgrp= data[4]
            msg = data[3]
            als = data[2]
            grp = data[1]
            num = data[0]
            print(msg)
            if self.msgcheck != msg or (self.numcheck != num and self.alscheck != als):
                log.save(data)
                self.msgcheck=msg
                self.numcheck=num
                self.alscheck=als
            msg = message.normalize(msg)
            msgs = list(msg.split(" "))
            if msg.find(config.bot_name) >= 0:
                if len(msgs) == 1:
                    msgreply = reply.getOpeningMessage()
                else:
                    msgreply = reply.message(msg)
                    if msgreply[:2] == 'm:':
                        modulename = msgreply.split(':')[1]
                        if auth.valid(num, msgreply):
                            mod=import_module('module.' + modulename)
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
                    wa.typeAndSendMessage(driver, msgreply)
                except:
                    print("field reply not found!!")