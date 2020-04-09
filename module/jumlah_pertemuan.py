from module import kelas
from lib import wa, reply
import os

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    #fix commit #27
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    num=data[0]
    lecturercode=kelas.getKodeDosen(num)
    msgreply=kelas.getListMK(lecturercode)
    return msgreply