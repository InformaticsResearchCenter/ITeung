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
            #num = self.getSenderNumber(driver)
            #alname = self.getSenderName(driver)
            #print(num+' - '+alname)
            
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
                msgreply=msgreply.replace("#BOTNAME#", config.bot_name)
                wa.typeAndSendMessage(driver,msgreply)
        except Exception as e:
            print(e)
            print("errorr..")
            wa.typeAndSendMessage(driver,"Duh maaf program yang diminta lagi rusak nih.. tulisannya : \n _"+str(e)+"_ \n minta tolong dong forwadin pesan diatas ke akang teteh mimin ya... Makasih :) ")




