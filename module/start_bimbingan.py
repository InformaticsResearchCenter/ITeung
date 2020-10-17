from lib import numbers
from module import kelas, cek_bimbingan_dosen
from datetime import datetime
from lib import wa, reply, message
import os, config

def auth(data):
    datakaprodi=getDataForKaprodi(data[0])
    if datakaprodi is not None:
        if isKaprodi(datakaprodi):
            ret = True
        else:
            ret = False
    else:
        ret = False
    return ret

def replymsg(driver, data):
    # wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    # wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    # wa.typeAndSendMessage(driver, wmsg)
    tipe_bimbingan=cek_bimbingan_dosen.cekTipeBimbingan(data[3])
    if tipe_bimbingan:
        nipy, prodiid=getDataForKaprodi(data[0])
        datestring=data[3].split(' ')[-1]
        day=int(datestring.split('-')[0])
        month=int(datestring.split('-')[1])
        year=int(datestring.split('-')[2])
        date=datetime.date(datetime(year, month, day))
        updateDateBimbingan(prodiid, date, tipe_bimbingan)
        msgreply='sudah di update cuyyyyy'
    else:
        msgreply=f'mana niwhhhh tipe bimbingannya {config.bot_name} ga nemuin nih dimana tipe bimbingannya'
    return msgreply

def getDataForKaprodi(num):
    num=numbers.normalize(num)
    db=kelas.dbConnectSiap()
    sql="select NIPY, Homebase from simak_mst_dosen where Handphone='{phonenumber}'".format(phonenumber=num)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            ret=row
        else:
            ret=None
    return ret

def isKaprodi(data):
    db=kelas.dbConnectSiap()
    prodiid=data[1]
    nipy=data[0]
    sql = "select * from simak_mst_pejabat where ProdiID={prodiid} and JenisJabatanID=5 and NIPY='{nipy}'".format(prodiid=prodiid, nipy=nipy)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    if row is not None:
        ret = True
    else:
        ret = False
    return ret

def updateDateBimbingan(prodiid, dateupdate, tipe_bimbingan):
    db=kelas.dbConnectSiap()
    sql=f"UPDATE simak_mst_prodi SET `Start_{tipe_bimbingan}` = '{dateupdate}' WHERE `ProdiID` = '{prodiid}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)