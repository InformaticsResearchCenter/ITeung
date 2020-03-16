from lib import wa,reply,message
import config
from importlib import import_module
from datetime import datetime



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

            if len(data) == 3:
                msg = data[2]
                als = data[1]
                num = data[0]
            else:
                msg = data[1]
                num = data[0]

            msg  = message.normalize(msg)
            msgs = list(msg.split(" "))

            if msg.find(config.bot_name) >= 0:
                if len(msgs) == 1:
                    msgreply = reply.getOpeningMessage()
                else:
                    msgreply=reply.message(msg)
                    if msgreply[:2] == 'm:':
                        if msgreply[2:] == 'prodi':
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
                        if msgreply[2:] == 'kelas':
                            modulename = msgreply.split(':')[1]
                            mod= import_module('module.'+modulename)
                            if mod.numberAuth(num):
                                wmsg=reply.getContentWithKeyword(modulename)
                                msgreply=wmsg.replace("#MATKUL#", mod.mulaiMatkul(msg))
                                wa.typeAndSendMessage(driver, msgreply)
                                kelas = True
                                msgcek=''
                            else:
                                msgreply="Enak aja main mulai kelas tunggu dosennya dulu dong :-)"

                            while kelas:
                                data=wa.getData(driver)

                                getDateTimeNow=datetime.now()

                                datetimenow=getDateTimeNow.strftime("%d/%m/%Y %H:%M:%S")

                                msg = data[2]
                                als = data[1]
                                num = data[0]

                                msg = message.normalize(msg)
                                msgs = msg.split(" ")

                                if msgcek != msg:
                                    
                                    msgcek = msg

                                if msg.find(config.bot_name) >= 0:
                                    if len(msgs) == 1:
                                        msgreply = reply.getOpeningMessage()
                                    else:
                                        msgreply = reply.message(msg)
                                        if msgreply[:2] == 'm:':
                                            if msgreply[2:] == 'kelas':
                                                if msgs[-1] == "selesai":
                                                    modulename = msgreply.split(":")[1]
                                                    mod=import_module('module.'+modulename)
                                                    namamatkul=mod.selesaiMatkul(msg)
                                                    msgreply="oke, matkul "+namamatkul+" selesai"
                                                    kelas=False


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



