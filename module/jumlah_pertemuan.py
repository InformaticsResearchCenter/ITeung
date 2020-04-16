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
    if kelas.cekSiap():
        wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        wa.typeAndSendMessage(driver, wmsg)
        num=data[0]
        lecturercode=kelas.getKodeDosen(num)
        msgreply=kelas.getListMK(lecturercode)
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply