from module import kelas, bimbingan_dosen, pertemuan_bimbingan, bimbingan_mahasiswa
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
    tipe_bimbingan=cekTipeBimbingan(msg)
    if tipe_bimbingan:
        for i in getMahasiswaBimbingan(kelas.getTahunID(), tipe_bimbingan):
            if i[1]==kodedosen or i[2]==kodedosen:
                npm.append(i[0])
        try:
            datefromdatabasehomebase=bimbingan_dosen.getStartDate(num, tipe_bimbingan)
            startdate = datetime.date(datefromdatabasehomebase)
            if 'pertemuan' in msg:
                pertemuan=msg.split(' pertemuan ')[1]
            else:
                pertemuan, datemulai, dateakhir=bimbingan_dosen.countPertemuan(startdate)
            try:
                pertemuan=int(pertemuan)
                msgreply=f'Nama Dosen: {kelas.getNamaDosen(kodedosen)}\n' \
                         f'Prodi: {pertemuan_bimbingan.getHomebase(num)}\n' \
                         f'Pertemuan: {pertemuan}\n\n' \
                         f'NPM | Nama | Status Bimbingan\n\n'
                for i in npm:
                    cek=cek_bimbingan(i, kodedosen, pertemuan, tipe_bimbingan)
                    namamahasiswa=kelas.getStudentNameOnly(i)
                    if cek == None:
                        msgreply+=f'*{i}* | {namamahasiswa} | *_BELUM BIMBINGAN_*\n'
                    else:
                        msgreply+=f'*{i}* | {namamahasiswa} | *_SUDAH BIMBINGAN_*\n'
            except Exception as e:
                msgreply=f'wahhh salah di pertemuan nih bosqqqqqqqqqqqq coba pertemuannya make angka yak jangan make hurup....'
        except:
            msgreply='ihhhhh belum diset nih tanggal awal bimbingannya coba deh Bapak/Ibu dosen komunikasi ya sama KAPRODI untuk set tanggal mulai bimbingannnya, tutorial bisa dibaca di panduan iteung yaaa yang bagian *kaprodi* hatur tengkyuuu....'
    else:
        msgreply='eh eh eh mana nihhh tipe bimbingannya harus dimasukin ke keyword yaaaa tipe bimbingannya cek di panduan mahasiswa bimbingan yaaa...'
    return msgreply

def cek_bimbingan(npm, kodedosen, pertemuan, tipe_bimbingan):
    db=kelas.dbConnectSiap()
    sql=f'select * from simak_croot_bimbingan where MhswID={npm} and DosenID="{kodedosen}" and Pertemuan_={pertemuan} and Tipe="{tipe_bimbingan}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row
        else:
            return None

def getMahasiswaBimbingan(tahunid, tipe_bimbingan):
    db=kelas.dbConnect()
    sql=f"select * from bimbingan_data where tahun_id={tahunid} and tipe_bimbingan='{tipe_bimbingan}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        return rows

def cekTipeBimbingan(message):
    for i in message.split(' '):
        if bimbingan_mahasiswa.tipeSwitcher(i):
            return i
        else:
            continue
    return False