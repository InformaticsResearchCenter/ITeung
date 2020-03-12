from lib import wa,reply
import config
import random
from importlib import import_module



class Chatbot(object):
    def __init__(self):
        driver = wa.setProfile(config.profile_folder)
        wa.loginWA(driver)
        while True:
            self.cekAndSendMessage(driver)
        
       
    def cekAndSendMessage(self,driver):
        try:
            wa.openMessage(driver)
            data = wa.getData(driver)

            msg = data[1]
            num = data[0]

            msg  = wa.normalize(msg)
            msgs = list(msg.split(" "))

            if msg.find(config.bot_name) >= 0:
                if len(msgs) == 1:
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
                            wa.typeAndSendMessage(driver,wmsg)
                            msgreply=mod.reply(msg)
                        else:
                            msgreply=reply.getReplyAuth()
        except Exception as e:
            print(e)
            msgreply=reply.getErrorMessage()
            msgreply=msgreply.replace("#ERROR#", str(e))

        if 'msgreply' in locals():
            if msgreply[:2] != 'm:':
                msgreply=msgreply.replace("#BOTNAME#", config.bot_name)
                print(msgreply)
                try:
                    wa.typeAndSendMessage(driver,msgreply)
                except:
                    print("field reply not found!!")



