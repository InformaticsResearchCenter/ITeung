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
            msg = wa.getMessage(driver)
            num = self.getSenderNumber(driver)
            #alname = self.getSenderName(driver)
            #print(num+' - '+alname)
            print(num)
			
            msg  = wa.normalize(msg)
            msgs = list(msg.split(" "))
            
            if msg.find(config.bot_name) >= 0:
                if len(msgs) == 1:
                    msgreply = reply.getOpeningMessage()
                else:
                    msgreply=reply.message(msg)
                    if msgreply[:2] == 'm:':
                        modulename = msgreply.split(':')[1]
                        mod=import_module('module.'+modulename)
                        wmsg=reply.getWaitingMessage(modulename)
                        wa.typeAndSendMessage(driver,wmsg)
                        msgreply=mod.reply(driver,msg)
        except Exception as e:
            print(e)
            msgreply=reply.getErrorMessage()
            msgreply=msgreply.replace("#ERROR#", str(e))
                                      
        if 'msgreply' in locals():
            msgreply=msgreply.replace("#BOTNAME#", config.bot_name)
            wa.typeAndSendMessage(driver,msgreply)



