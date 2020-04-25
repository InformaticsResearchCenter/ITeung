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
        
        try:
            matkul = data[data.index('matkul')+1] if any(char.isdigit() for char in data[data.index('matkul')+1]) else False
            kelass = data[data.index('kelas')+1].upper() if len(data[data.index('kelas')+1]) < 2 else False
            jenis = data[3].lower() if data[3].lower() == 'uts' or data[3].lower() == 'uas' else False
            if matkul and kelass and jenis:
                datas = {
                    'tahun': config.siap_tahun_id,
                    'kode_matkul': matkul,
                    'kelas': convertKelas(kelass),
                    'jenis': jenis
                }
                
                msgreply = mainCekNilai(num, datas)
                
                msgreply = "Ini nilai ujian yang Bapak/Ibu minta\n\n"+msgreply
            else:
                msgreply = 'Salah keyword beb......'
        except:
            msgreply = 'Salah keyword beb.....'
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply

def dbConnectSiap():
    db = pymysql.connect(config.db_host_siap,
                         config.db_username_siap,
                         config.db_password_siap,
                         config.db_name_siap)
    return db


def checkDosen(nomor, tahun, matkul):
    db = dbConnectSiap()
    query = """
        select distinct(Nama) from simak_trn_jadwal where DosenID = (select Login from simak_mst_dosen where Handphone = '"""+nomor+"""') and TahunID = '"""+tahun+"""' and MKKode = '"""+matkul+"""'
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


def checkNilaiUTS(kode_matkul, tahun, kelas, matkul):
    db = dbConnectSiap()
    query = """
        select krs.MhswID, mhs.Nama, krs.UTS from simak_trn_krs krs, simak_mst_mahasiswa mhs, simak_trn_jadwal j where krs.StatusKRSID='A' and krs.MKKode='"""+kode_matkul+"""' and krs.TahunID='"""+tahun+"""' and krs.Kelas='"""+kelas+"""' and krs.JadwalID=j.JadwalID and krs.NA='N' and krs.MhswID=mhs.MhswID group by krs.MhswID order by krs.MhswID ASC
    """
    with db:
        nilais = '*Nilai UTS '.upper()+matkul+'*' + '\nNPM | Nama | UTS\n'

        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if rows is not None:
            for row in rows:
                nilais += '* % s * | % s | %s\n' % (row[0], row[1], row[2])

    return nilais


def checkNilaiUAS(kode_matkul, tahun, kelas, matkul):
    db = dbConnectSiap()
    query = """
        select krs.MhswID, mhs.Nama, krs.UAS from simak_trn_krs krs, simak_mst_mahasiswa mhs, simak_trn_jadwal j where krs.StatusKRSID='A' and krs.MKKode='"""+kode_matkul+"""' and krs.TahunID='"""+tahun+"""' and krs.Kelas='"""+kelas+"""' and krs.JadwalID=j.JadwalID and krs.NA='N' and krs.MhswID=mhs.MhswID group by krs.MhswID order by krs.MhswID ASC
    """
    with db:
        nilais = '*Nilai UAS '.upper()+matkul+'*' + '\nNPM | Nama | UAS\n'

        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if rows is not None:
            for row in rows:
                nilais += '* % s * | % s | %s\n' % (row[0], row[1], row[2])

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


def mainCekNilai(nomor, data):
    matkul = checkDosen(nomor, data['tahun'], data["kode_matkul"])
    if matkul:
        if data['jenis'] == 'uts':
            msg = checkNilaiUTS(data['kode_matkul'],
                                data['tahun'], data['kelas'], matkul)
        elif data['jenis'] == 'uas':
            msg = checkNilaiUAS(data['kode_matkul'],
                                data['tahun'], data['kelas'], matkul)
        else:
            msg = 'Ujian apa nih beb...'
    else:
        msg = 'Ohh tidak bisa..'
    return msg


