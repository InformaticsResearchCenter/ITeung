from lib import wa, reply, message, log
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
        wa.restartMemu(wa.detectphoneNotConnected(driver))
        messageindex = config.message_wa_index
        alsandnumindex = config.default_alias_number_index
        for loop in range(wa.messageunread(driver)):
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
                print(msg)
                if self.msgcheck != msg or (self.numcheck != num and self.alscheck != als):
                    log.save(num=num, msg=msg, als=als, grp=grp, isgrp=isgrp)
                    self.msgcheck=msg
                    self.numcheck=num
                    self.alscheck=als
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
                        wa.typeAndSendMessage(driver, msgreply)
                        del msgreply
                    except:
                        print("field reply not found!!")
