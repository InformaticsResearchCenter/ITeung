from lib import wa, reply, message, auth
from importlib import import_module
import config


class Chatbot(object):
    def __init__(self):
        driver = wa.setProfile(config.profile_folder)
        wa.loginWA(driver)
        while True:
            self.cekAndSendMessage(driver)

    def cekAndSendMessage(self, driver):
        try:
            wa.openMessage(driver)
            data = wa.getData(driver)
            if len(data) == 3:
                msg = data[3]
                als = data[2]
                grp = data[1]
                num = data[0]
            else:
                msg = data[1]
                num = data[0]
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
                            msgreply=mod.replymsg(driver, msg)
                        else:
                            msgreply=reply.getReplyAuth(modulename)
        except Exception as e:
            print(e)
            msgreply = reply.getErrorMessage()
            msgreply = msgreply.replace("#ERROR#", str(e))

        if 'msgreply' in locals():
            if msgreply[:2] != 'm:':
                msgreply = msgreply.replace("#BOTNAME#", config.bot_name)
                print(msgreply)
                try:
                    wa.typeAndSendMessage(driver, msgreply)
                except:
                    print("field reply not found!!")