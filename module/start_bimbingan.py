from lib import numbers
from module import kelas
from datetime import datetime
from lib import wa, reply
import os, config

def auth(data):
    prodiid=getHomeBase(data[0])
    if prodiid is not None:
        if isKaprodi(prodiid):
            ret = True
        else:
            ret = False
    else:
        ret = False
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    prodiid=getHomeBase(data[0])
    datestring=data[3].split(' ')[-1]
    day=int(datestring.split('-')[0])
    month=int(datestring.split('-')[1])
    year=int(datestring.split('-')[2])
    date=datetime.date(datetime(year, month, day))
    updateDateBimbingan(prodiid, date)
    msgreply='sudah di update cuyyyyy'
    return msgreply

def getHomeBase(num):
    num=numbers.normalize(num)
    db=kelas.dbConnectSiap()
    sql="select Homebase from simak_mst_dosen where Handphone='{phonenumber}'".format(phonenumber=num)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
    return row[0]

def isKaprodi(prodiid):
    db=kelas.dbConnectSiap()
    sql = "select * from simak_mst_pejabat where ProdiID={prodiid} and JenisJabatanID=5".format(prodiid=prodiid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    if row is not None:
        ret = True
    else:
        ret = False
    return ret

def updateDateBimbingan(prodiid, dateupdate):
    db=kelas.dbConnectSiap()
    sql="UPDATE simak_mst_prodi SET `Start` = '{dateupdate}' WHERE `ProdiID` = '{prodiid}'".format(dateupdate=dateupdate, prodiid=prodiid)
    with db:
        cur=db.cursor()
        cur.execute(sql)