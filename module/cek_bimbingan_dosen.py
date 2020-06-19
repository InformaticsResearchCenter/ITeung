from module import kelas, bimbingan_dosen, pertemuan_bimbingan
from lib import reply, wa
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
    num=data[0]
    npm=[]
    kodedosen=kelas.getKodeDosen(num)
    for i in getMahasiswaBimbingan(kelas.getTahunID()):
        if i[1]==kodedosen or i[2]==kodedosen:
            npm.append(i[0])
    datefromdatabasehomebase=bimbingan_dosen.getStartDate(num)
    startdate = datetime.date(datefromdatabasehomebase)
    pertemuan, datemulai, dateakhir=bimbingan_dosen.countPertemuan(startdate)
    msgreply='Nama Dosen: {lecturername}\nProdi: {prodi}\nPertemuan: {pertemuan}'.format(lecturername=kelas.getNamaDosen(kodedosen), prodi=pertemuan_bimbingan.getHomebase(num), pertemuan=str(pertemuan))+'\n\nNPM | Nama | Status Bimbingan\n\n'
    for i in npm:
        cek=cek_bimbingan(i, kodedosen, pertemuan)
        namamahasiswa=kelas.getStudentNameOnly(i)
        if cek == None:
            msgreply+='*'+i+'*'+' | '+namamahasiswa+' | '+'*_BELUM BIMBINGAN_*'+'\n'
        else:
            msgreply+='*'+i+'*'+' | '+namamahasiswa+' | '+'*_SUDAH BIMBINGAN_*'+'\n'
    return msgreply

def cek_bimbingan(npm, kodedosen, pertemuan):
    db=kelas.dbConnectSiap()
    sql='select * from simak_croot_bimbingan where MhswID={npm} and DosenID="{dosenid} and Pertemuan_={pertemuanke}"'.format(dosenid=kodedosen, npm=npm, pertemuanke=pertemuan)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row
        else:
            return None

def getMahasiswaBimbingan(tahunid):
    db=kelas.dbConnect()
    sql="select * from bimbingan_data where tahun_id={tahunid}".format(tahunid=tahunid)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        return rows