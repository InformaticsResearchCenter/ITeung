from lib import wa, reply
from Crypto.Cipher import AES
from importlib import import_module
import os, config

def auth(data):
    # if kelas.getKodeDosen(data[0]) == '':
    #     ret=False
    # else:
    #     ret=True
    return True

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace("#BOTNAME#", config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    msg=data[3]
    passcode=msg.split(' ')[-1]
    try:
        obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode("utf8"))
        dec = bytes.fromhex(passcode)
        resultpasscode, status = obj.decrypt(dec).decode('utf-8'), True
    except:
        resultpasscode, status = '', False
    if status:
        modulename=resultpasscode.split(';')[0]
        mod = import_module('module.' + modulename)
        msgreply=mod.verifyDigitalSign(resultpasscode)
    else:
        msgreply=f'waduh akang/teteh kayaknya #BOTNAME# ga bisa mengenali passcode yang *{passcode}* deh, coba di periksa lagi yaa, dan jangan diubah passcodenya'
    return msgreply