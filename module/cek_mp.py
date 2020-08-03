from module import kelas
from lib import message, reply, wa
import os

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    num=data[0]
    jadwal_id_msg=message.normalize(data[3]).split(' ')[-1]
    dosenid=kelas.getKodeDosen(num=num)
    jadwalID=getJadwalIDfromDosenID(dosenid=dosenid)
    if jadwal_id_msg == 'all':
        msg=allJadwalIDDosen(jadwalID)
        msgreply = msg
    else:
        data=[]
        datafix=[]
        data.append(jadwal_id_msg)
        datafix.append(data)
        msg=allJadwalIDDosen(datafix)
        msgreply = msg
    return msgreply

def getJadwalIDfromDosenID(dosenid):
    db = kelas.dbConnectSiap()
    sql=f'select JadwalID, Nama from simak_trn_jadwal where DosenID="{dosenid}" and TahunID={kelas.getTahunID()}'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

def getPresensiFromJadwalID(presensiID):
    db = kelas.dbConnectSiap()
    sql=f'select * from simak_trn_presensi_dosen where JadwalID={presensiID} ORDER BY Pertemuan ASC'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
    return rows

def allJadwalIDDosen(jadwalID):
    msg='ini yaaa datanya...'
    for i in jadwalID:
        msg += f"Jadwal ID: {i[0]}\nNama Matakuliah: {i[1]}\n"
        msg += "Pertemuan | Materi Perkuliahan\n"
        presensi=getPresensiFromJadwalID(i[0])
        if presensi != ():
            for j in presensi:
                pertemuan = j[4]
                if j[-2] != None:
                    materiPerkuliahan = message.normalize(j[-2])
                    msgs = f"{pertemuan} | {materiPerkuliahan}\n"
                else:
                    msgs = f"{pertemuan} | _(belum diisi)_\n"
                msg += msgs
        else:
            msg+='mohon maaf jadwalid tidak dapat ditemukan'
        msg += '\n'
    return msg