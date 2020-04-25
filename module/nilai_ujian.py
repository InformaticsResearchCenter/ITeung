import config
import pandas as pd
import pymysql
import openpyxl
import string
import os
import shutil
from module import kelas
from lib import reply, wa
from datetime import datetime
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
        wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
        wa.typeAndSendMessage(driver, wmsg)
        msg = data[3]
        num = data[0]
        nomor = numbers.normalize(num)
        data = msg.split(' ')
        
        if len(data) == 4:
            try:
                jenis = data[3] if data[3].lower() == 'uts' or data[3].lower() == 'uas' else False
                if jenis:
                    filename = downloadFile(driver)
                    moveFiles(filename)
                    msgreply = inputNilaiByExcel(
                        filename, jenis, config.siap_tahun_id, nomor)
                    removeFile(filename)
                else:
                    msgreply = 'Salah keyword bosque..'
            except:
                msgreply = 'Gak ada filenya....'
        else:
            try:
                jenis = data[3].lower() if data[3].lower() == 'uts' or data[3].lower() == 'uas' else False
                nilai = data[data.index('uts')+1] if all(char.isdigit() for char in data[data.index('uts')+1]) and (
                    int(data[data.index('uts')+1]) <= 100 and int(data[data.index('uts')+1]) >= 0) else False
                npm = data[data.index('npm')+1] if all(char.isdigit() for char in data[data.index('npm')+1]) else False
                matkul = data[data.index('matkul')+1] if any(char.isdigit() for char in data[data.index('matkul')+1]) else False
                if jenis and nilai and npm and matkul:
                    data = {
                        'tahun': config.siap_tahun_id,
                        'kode_matkul': matkul,
                        'npm': npm,
                        'nilai': nilai
                    }
                    msgreply = inputNilaiByMesssage(data, jenis, nomor)
                else:
                    msgreply = 'Salah keyword bosque...'
                
            except:
                msgreply = 'Salah keyword bosque....'
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply


def downloadFile(driver):
    filecheck = driver.find_elements_by_class_name('_2RBFb')[-1]
    filename = driver.find_elements_by_class_name('_3UPcK')[-1].text
    driver.find_elements_by_class_name('_17viz')[-1].click()
    return filename

def moveFiles(filename):
    move = True
    while move:
        try:
            source = 'C:\\Users\\'+config.computeruser + \
                '\\Downloads\\' + str(filename)
            destination = os.getcwd()
            shutil.move(source, destination)
            move = False
        except Exception as e:
            if 'already exists' in str(e):
                move = False
            else:
                move = True


def removeFile(filename):
    os.remove(filename)


def dbConnectSiap():
    db = pymysql.connect(config.db_host_siap,
                         config.db_username_siap,
                         config.db_password_siap,
                         config.db_name_siap)
    return db


def checkDosen(nomor, tahun, matkul):
    db = dbConnectSiap()
    query = """
        select * from simak_trn_jadwal where DosenID = (select Login from simak_mst_dosen where Handphone = '"""+nomor+"""') and TahunID = '"""+tahun+"""' and MKKode = '"""+matkul+"""'
    """
    with db:
        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            return True
        else:
            return False


def getMahasiswa(kode_matkul, tahun, kelas):
    db = dbConnectSiap()
    query = """
        select krs.MhswID from simak_trn_krs krs, simak_mst_mahasiswa mhs, simak_trn_jadwal j
        where krs.StatusKRSID='A' and krs.MKKode='"""+kode_matkul+"""' and krs.TahunID='"""+tahun+"""' and krs.Kelas='"""+kelas+"""' and
        krs.JadwalID=j.JadwalID and krs.NA='N' and
        krs.MhswID=mhs.MhswID
        group by krs.MhswID
        order by krs.MhswID ASC
    """

    with db:
        mahasiswa = []

        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if rows is not None:
            for row in rows:
                mahasiswa.extend(row)

            return mahasiswa
        else:
            return False


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


def inputNilaiUTS(data):
    db = dbConnectSiap()
    query = """
        update simak_trn_krs set uts='"""+data['nilai']+"""' where MhswID='"""+data['npm']+"""' 
        and MKKode='"""+data['kode_matkul']+"""' and TahunID='"""+data['tahun']+"""';
    """
    with db:
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        if cur.rowcount > 0:
            return 'Berhasil input bosque...'
        else:
            return 'Blm berhasil bosque, mungkin npm ato matkul salah ato nilai yg diinput sama kyk sebelumnya'


def inputNilaiUAS(data):
    db = dbConnectSiap()
    query = """
        update simak_trn_krs set uas='"""+data['nilai']+"""' where MhswID='"""+data['npm']+"""' 
        and MKKode='"""+data['kode_matkul']+"""' and TahunID='"""+data['tahun']+"""';
    """
    with db:
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        if cur.rowcount > 0:
            return 'Berhasil input bosque.....'
        else:
            return 'Blm berhasil bosque, mungkin npm ato matkul salah ato nilai yg diinput sama kyk sebelumnya'


def getTanggalUTS(tahun):
    db = dbConnectSiap()
    query = """
        SELECT TglUTSMulai, TglUASMulai FROM simak_mst_tahun where TahunID = '"""+tahun+"""' and ProdiID = '14' order by TglUTSMulai ASC limit 1
    """

    with db:
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            return row
        else:
            return False


def getTanggalUAS(tahun):
    db = dbConnectSiap()
    query = """
        SELECT TglUASMulai, TglNilai FROM simak_mst_tahun where TahunID = '"""+tahun+"""' and ProdiID = '14' order by TglUTSMulai ASC limit 1
    """

    with db:
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            return row
        else:
            return False


def inputByExcel(file, jenis, tahun, func, nomor):
    book = openpyxl.load_workbook(file)
    sheet = book.active
    kode_matkul = sheet["C5"].value.replace(
        ":", "").replace("/", "").split()[0]

    if checkDosen(nomor, tahun, kode_matkul):
        kelas = convertKelas(sheet["C6"].value.replace(":", "").strip())
        mahasiswas = getMahasiswa(kode_matkul, tahun, kelas)
        if mahasiswas:
            length = len(mahasiswas)
            npms = sheet['B10': 'B'+str(9+length)]
            nilais = sheet['E10': 'E'+str(9+length)]
            cells = dict(zip(npms, nilais))
            for k, v in cells.items():
                data = {
                    'tahun': tahun,
                    'kode_matkul': kode_matkul,
                    'npm': k[0].value,
                    'nilai': str(v[0].value) if v[0].value is not None else '0',
                }
                if jenis == 'uts':
                    func(data)
                elif jenis == 'uas':
                    func(data)
                else:
                    continue
            msg = 'Udh masuk bosque.......'
        else:
            msg = 'Kesalahan pada file bosque..'
    else:
        msg = 'Ohh tidak bisa bosque........'

    return msg


def inputNilaiByExcel(file, jenis, tahun, nomor):

    today = datetime.today().date()
    if jenis == 'uts':
        uts = getTanggalUTS(tahun)
        if uts[0] <= today and uts[1] >= today and uts:
            msg = inputByExcel(file, jenis, tahun, inputNilaiUTS, nomor)
        else:
            msg = 'Gak bisa bosque...'

    elif jenis == 'uas':
        uas = getTanggalUAS(tahun)
        if uas[0] <= today and uas[1] >= today and uas:
            msg = inputByExcel(file, jenis, tahun, inputNilaiUAS, nomor)
        else:
            msg = 'Gak bisa lagi bosque.........'
    else:
        msg = 'Ujian apa nih bosque..'

    return msg


def inputNilaiByMesssage(data, jenis, nomor):
    print(checkDosen(nomor, data['tahun'], data['kode_matkul']))
    if checkDosen(nomor, data['tahun'], data['kode_matkul']):
        today = datetime.today().date()
        if jenis == 'uts':
            uts = getTanggalUTS(data['tahun'])
            if uts[0] <= today and uts[1] >= today and uts:
                msg = inputNilaiUTS(data)
            else:
                msg = 'Gak bisa bosque.........'

        elif jenis == 'uas':
            uas = getTanggalUAS(data['tahun'])
            if uas[0] <= today and uas[1] >= today and uas:
                msg = inputNilaiUAS(data)
            else:
                msg = 'Gak bisa bosque..........'
        else:
            msg = 'Ujian apa nih bosque......'
    else:
        msg = 'Ohh tidak bisa....'
    return msg
