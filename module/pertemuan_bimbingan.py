from module import kelas, bimbingan_dosen, cek_bimbingan_dosen
from lib import reply, wa, numbers, message
from datetime import datetime
import os
def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    msg=message.normalize(data[3])
    tipe_bimbingan = cek_bimbingan_dosen.cekTipeBimbingan(msg)
    if tipe_bimbingan:
        startdate=datetime.date(bimbingan_dosen.getStartDate(data[0], tipe_bimbingan))
        pertemuan=bimbingan_dosen.countPertemuan(startdate)
        prodi=getHomebase(data[0])
        return 'ini yaa info pertemuannya:\n\nProdi: {prodi}\nJadwal Mulai Pertemuan: {startdate}\nPertemuan: {pertemuanke}'.format(prodi=prodi, startdate=startdate, pertemuanke=pertemuan[0])
    else:
        return 'aduhhh mana nihhh kok ngilang tipe bimbingannya ....'

def getHomebase(num):
    num=numbers.normalize(num)
    db=kelas.dbConnectSiap()
    sql="select `Nama` from simak_mst_prodi WHERE ProdiID=(select Homebase from simak_mst_dosen WHERE Handphone='{phonenumber}')".format(phonenumber=num)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        return row[0]