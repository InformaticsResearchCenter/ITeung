from module import kelas, cek_mp
from lib import wa, reply
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
    msg=data[3]
    dosenID=kelas.getKodeDosen(num)
    try:
        datasplit=msg.split(' materi perkuliahan ')[1]
        jadwalid=int(datasplit.split(' ')[0])
        jadwalidDosen=cek_mp.getJadwalIDfromDosenID(dosenID)
        for i in jadwalidDosen:
            if jadwalid in i:
                isAdaJadwal=True
                break
            else:
                isAdaJadwal=False
        if isAdaJadwal:
            pertemuan=datasplit.split(' ')[2]
            if len(pertemuan) > 1:
                materi=datasplit.split(' pertemuan ')[1][3:]
            else:
                materi=datasplit.split(' pertemuan ')[1][2:]
            updateMateriPerkuliahan(jadwalid, pertemuan, materi)
            msgreply='okeee bosqqq sudah di update'
        else:
            msgreply='Jadwal ID yang dimasukkan salah atau tidak ditemukan!'
    except Exception as e:
        print(str(e))
        msgreply='format katanya salah nichhhh bosqueeee'
    return msgreply

def updateMateriPerkuliahan(jadwalid, pertemuan, materi):
    db=kelas.dbConnectSiap()
    sql=f"UPDATE `simpati`.`simak_trn_presensi_dosen` SET `MP` = '{materi}' WHERE `JadwalID` = {jadwalid} AND `Pertemuan` = {pertemuan} AND `TahunID` = {kelas.getTahunID()}"
    with db:
        cur=db.cursor()
        cur.execute(sql)