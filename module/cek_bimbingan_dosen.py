from module import kelas, bimbingan_dosen, pertemuan_bimbingan
from lib import reply, wa, message
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
    msg=data[3]
    msg=message.normalize(msg)
    npm=[]
    kodedosen=kelas.getKodeDosen(num)
    for i in getMahasiswaBimbingan(kelas.getTahunID()):
        if i[1]==kodedosen or i[2]==kodedosen:
            npm.append(i[0])
    try:
        datefromdatabasehomebase=bimbingan_dosen.getStartDate(num)
        startdate = datetime.date(datefromdatabasehomebase)
        if 'pertemuan' in message:
            pertemuan=msg.split(' pertemuan ')[1]
        else:
            pertemuan, datemulai, dateakhir=bimbingan_dosen.countPertemuan(startdate)
        try:
            pertemuan=int(pertemuan)
            msgreply='Nama Dosen: {lecturername}\nProdi: {prodi}\nPertemuan: {pertemuan}'.format(lecturername=kelas.getNamaDosen(kodedosen), prodi=pertemuan_bimbingan.getHomebase(num), pertemuan=str(pertemuan))+'\n\nNPM | Nama | Status Bimbingan\n\n'
            for i in npm:
                cek=cek_bimbingan(i, kodedosen, pertemuan)
                namamahasiswa=kelas.getStudentNameOnly(i)
                if cek == None:
                    msgreply+='*'+i+'*'+' | '+namamahasiswa+' | '+'*_BELUM BIMBINGAN_*'+'\n'
                else:
                    msgreply+='*'+i+'*'+' | '+namamahasiswa+' | '+'*_SUDAH BIMBINGAN_*'+'\n'
        except:
            msgreply='wahhh salah di pertemuan nih bosqqqqqqqqqqqq coba pertemuannya make angka yak jangan make hurup....'
    except:
        msgreply='ihhhhh belum diset nih tanggal awal bimbingannya coba deh Bapak/Ibu dosen komunikasi ya sama KAPRODI untuk set tanggal mulai bimbingannnya, tutorial bisa dibaca di panduan iteung yaaa yang bagian *kaprodi* hatur tengkyuuu....'
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