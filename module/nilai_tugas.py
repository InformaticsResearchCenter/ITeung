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
from time import sleep


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

        try:
            filename = downloadFile(driver)
            sleep(2)
            moveFiles(filename)
            msgreply = inputByExcel(filename, kelas.getTahunID(), nomor)
            removeFile(filename)
        except FileNotFoundError:
            msgreply = 'Gak ada filenya....'
        except:
            msgreply = 'Ada masalah di kodingannya...'
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply


def downloadFile(driver):
    filecheck = driver.find_elements_by_class_name('r9_f4')[-1]
    filename = driver.find_elements_by_class_name('_3Whw5')[-1].text
    driver.find_elements_by_class_name('_1-9IA')[-1].click()
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


def checkDosen(nomor, tahun, jadwal_id):
    db = dbConnectSiap()
    query = """
            select distinct(Nama) from simak_trn_jadwal where DosenID = (select Login from simak_mst_dosen where Handphone = '""" + nomor + """') and TahunID = '""" + tahun + """' and JadwalID = '""" + jadwal_id + """'
        """
    with db:
        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        if cur.rowcount > 0:
            return True
        else:
            return False


def getMahasiswa(jadwal_id):
    db = dbConnectSiap()
    query = """
        select krs.MhswID from simak_trn_krs krs, simak_mst_mahasiswa mhs, simak_trn_jadwal j where krs.StatusKRSID='A' and krs.JadwalID='"""+jadwal_id+"""' and krs.TahunID=j.TahunID and krs.NA='N' and krs.MhswID=mhs.MhswID group by krs.MhswID order by krs.MhswID ASC
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


def inputNilaiTugas(data):
    # print(data)
    db = dbConnectSiap()
    query = """
        update simak_trn_krs set Tugas1='"""+str(data['nilais'][0])+"""', Tugas2='"""+str(data['nilais'][1])+"""', Tugas3='"""+str(data['nilais'][2])+"""', Tugas4='"""+str(data['nilais'][3])+"""', Tugas5='"""+str(data['nilais'][4])+"""' where MhswID='"""+str(data['npm'])+"""' and JadwalID='"""+str(data['jadwal_id'])+"""' and TahunID='"""+str(data['tahun'])+"""';
        """

    # print(query)

    with db:
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        if cur.rowcount > 0:
            return str(data['npm'])+' berhasil diinput bos'
        else:
            return str(data['npm'])+' blm berhasil bos, mungkin npm ato matkul salah ato nilai yg diinput sama kyk sebelumnya'


def getTanggalNilai(tahun, prodi):
    db = dbConnectSiap()
    query = """
        SELECT TglNilai, TahunID, ProdiID FROM simpati.simak_mst_tahun where NA = 'N' and ProgramID = 'REG' and TahunID = '"""+tahun+"""' and ProdiID = '"""+prodi+"""' order by TglNilai ASC limit 1
    """

    with db:
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return False


def getProdi(jadwal_id):
    db = dbConnectSiap()
    query = """
        SELECT ProdiID FROM simpati.simak_trn_jadwal where JadwalID='"""+jadwal_id+"""' order by TahunID DESC limit 1
    """

    with db:
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            return row[0].replace(".", "")
        else:
            return False


def inputByExcel(file, tahun, nomor):
    book = openpyxl.load_workbook(file)
    sheet = book.active
    jadwal_id = sheet["F5"].value.replace(":", "")
    prodi = getProdi(jadwal_id)
    tgl = getTanggalNilai(tahun, prodi)
    today = datetime.today().date()
    # print(tgl, today)
    if tgl >= today:
        if checkDosen(nomor, tahun, jadwal_id):
            mahasiswas = getMahasiswa(jadwal_id)
            if mahasiswas:
                length = len(mahasiswas)
                # print(length)
                npms = [x[0].value for x in sheet['B10': 'B'+str(9+length)]]
                nilais = [
                    [x[0].value for x in sheet['D10': 'D'+str(9+length)]], [x[0].value for x in sheet['E10': 'E'+str(9+length)]], [x[0].value for x in sheet['F10': 'F'+str(9+length)]], [x[0].value for x in sheet['G10': 'G'+str(9+length)]], [x[0].value for x in sheet['H10': 'H'+str(9+length)]]]

                if len(npms) == len(nilais[0]):

                    dict_nilai = {}

                    for i, v in enumerate(npms):
                        tugas = []
                        for x in nilais:
                            tugas.append(x[i])
                        dict_nilai[v] = tugas

                    for k, v in dict_nilai.items():

                        data = {
                            'tahun': tahun,
                            'jadwal_id': jadwal_id,
                            'npm':  k,
                            'nilais': v
                        }
                        print(inputNilaiTugas(data))

                    msg = 'Udh masuk bos'
                else:
                    msg = 'Gak sama bos, takutnya salah letak'
            else:
                msg = 'Kesalahan pada file bos'
        else:
            msg = 'Ohh tidak bisa bos'
    else:
        msg = "Mana sempat, sudah telat"

    return msg
