from module import kelas
from lib import numbers, reply, wa

import config, os

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    data=getDataDosen(data[0])
    msgreply='Ini data yang Bapak/Ibu dosen minta ya:\n\nKode Dosen: {dosenid}\nNama: {namadosen}\nHandphone: {nohp}\nE-Mail: {email}'.format(dosenid=data[0], namadosen=data[1], nohp=data[2], email=data[3])
    return msgreply

def getDataDosen(num):
    db=kelas.dbConnectSiap()
    num=numbers.normalize(num)
    sql="select Login, Nama, Handphone, Email form simak_mst_dosen where Handphone='{num}'".format(num=num)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row
        else:
            return None