import config
import pandas as pd
import pymysql
import openpyxl
import string
from datetime import datetime
from lib import reply
import os
from lib import wa
from module import kelas
from lib import wa, numbers


def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret


def replymsg(driver, data):
    if kelas.cekSiap():
        wmsg = reply.getWaitingMessage(
            os.path.basename(__file__).split('.')[0])
        wa.typeAndSendMessage(driver, wmsg)
        num = data[0]
        num = numbers.normalize(num)
        msg = data[3]
        data = msg.split(' ')
        # error ketika uas
        try:
            if 'matkul' in data and 'jadwal' not in data:
                matkul = data[data.index('matkul')+1] if any(char.isdigit()
                                                             for char in data[data.index('matkul')+1]) else False
                kelass = data[data.index(
                    'kelas')+1].upper() if len(data[data.index('kelas')+1]) < 2 else False

                if matkul and kelass:
                    datas = {
                        'tahun': kelas.getTahunID(),
                        'kode_matkul': matkul,
                        'kelas': convertKelas(kelass),
                        'jadwal': 0
                    }

                    msgreply = mainCekNilai(num, datas)

                    msgreply = "Ini nilai ujian yang Bapak/Ibu minta\n\n"+msgreply
                else:
                    msgreply = 'Salah keyword beb...................'
            elif 'jadwal' in data and 'matkul' not in data:
                jadwal = data[data.index('jadwal')+1] if all(char.isdigit()
                                                             for char in data[data.index('jadwal')+1]) else False
                if jadwal:
                    datas = {
                        'tahun': kelas.getTahunID(),
                        'kode_matkul': 0,
                        'kelas': 0,
                        'jadwal': jadwal
                    }

                    msgreply = mainCekNilai(num, datas)

                    msgreply = "Ini nilai ujian yang Bapak/Ibu minta\n\n"+msgreply
                else:
                    msgreply = 'Salah keyword beb...............................'
            else:
                msgreply = 'Salah keyword beb......'
        except:
            msgreply = 'Salah keyword beb....., atau salah masukin jadwal uas atau uts'
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply


def dbConnectSiap():
    db = pymysql.connect(config.db_host_siap,
                         config.db_username_siap,
                         config.db_password_siap,
                         config.db_name_siap)
    return db


def checkDosen(nomor, tahun, matkul=0, jadwal=0):
    db = dbConnectSiap()
    if matkul != 0 and jadwal == 0:
        query = """
            select distinct(Nama) from simak_trn_jadwal where DosenID = (select Login from simak_mst_dosen where Handphone = '"""+nomor+"""') and TahunID = '"""+tahun+"""' and MKKode = '"""+matkul.upper()+"""'
        """
    elif jadwal != 0 and matkul == 0:
        query = """
            select distinct(Nama) from simak_trn_jadwal where DosenID = (select Login from simak_mst_dosen where Handphone = '""" + nomor + """') and TahunID = '""" + tahun + """' and JadwalID = '""" + jadwal + """'
        """
    with db:
        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            for row in rows:
                return row[0]
        else:
            return False


def checkNilaiTugas(tahun, matkul, kode_matkul=0, jadwal=0, kelas=0):
    db = dbConnectSiap()
    if kode_matkul != 0:
        query = """
            select krs.MhswID, mhs.Nama, krs.Tugas1, krs.Tugas2, krs.Tugas3, krs.Tugas4, krs.Tugas5 from simak_trn_krs krs, simak_mst_mahasiswa mhs, simak_trn_jadwal j where krs.StatusKRSID='A' and krs.MKKode='"""+kode_matkul+"""' and krs.TahunID='"""+tahun+"""' and krs.Kelas='"""+kelas+"""' and krs.JadwalID=j.JadwalID and krs.NA='N' and krs.MhswID=mhs.MhswID group by krs.MhswID order by krs.MhswID ASC
        """
    elif jadwal != 0:
        query = """
            select krs.MhswID, mhs.Nama, krs.Tugas1, krs.Tugas2, krs.Tugas3, krs.Tugas4, krs.Tugas5 from simak_trn_krs krs, simak_mst_mahasiswa mhs, simak_trn_jadwal j where krs.StatusKRSID='A' and krs.JadwalID='"""+jadwal+"""' and krs.TahunID='"""+tahun+"""' and krs.NA='N' and krs.MhswID=mhs.MhswID group by krs.MhswID order by krs.MhswID ASC
        """
    with db:
        nilais = '*Nilai Tugas '.upper()+matkul+'*' + \
            '\n*NPM | Nama | Tugas 1 | Tugas 2 | Tugas 3 | Tugas 4 | Tugas 5*\n'

        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if rows is not None:
            for row in rows:
                nama = cutNama(row[1])
                nilais += '*%s* | %s | %s | %s | %s | %s | %s\n' % (row[0], nama, int(
                    row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]))

    return nilais


def convertKelas(kelas):
    kelas = kelas.lower()
    list_kelas = list(string.ascii_lowercase)
    list_nomor = list(range(1, 27))
    dict_kelas = dict(zip(list_nomor, list_kelas))
    for k, v in dict_kelas.items():
        if v == kelas:
            return str(k).zfill(2)
            break
    return '00'


def cutNama(nama):
    nama = ' '.join(map(str, nama.split(" ", 2)[:2])) if len(
        nama.split(" ")) > 1 else nama
    return nama


def mainCekNilai(nomor, data):
    if data['kode_matkul'] != 0:
        matkul = checkDosen(nomor, data['tahun'], matkul=data["kode_matkul"])
        if matkul:
            msg = checkNilaiTugas(
                data['tahun'], matkul, kode_matkul=data['kode_matkul'], kelas=data['kelas'])
        else:
            msg = 'ohh tidak bisa, gak punya akses anda, atau salah matkul'
        return msg
    elif data['jadwal'] != 0:
        matkul = checkDosen(nomor, data['tahun'], jadwal=data["jadwal"])
        if matkul:
            msg = checkNilaiTugas(
                data['tahun'], matkul, jadwal=data['jadwal'])

        else:
            msg = 'ohh tidak bisa, gak punya akses anda, atau salah jadwal'
        return msg
