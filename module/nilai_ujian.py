import config
import pandas as pd
import pymysql
import openpyxl
import string
import os
import shutil
from module import kelas, cek_nilai
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
        msg = data[3].lower()
        num = data[0]
        nomor = numbers.normalize(num)
        data = msg.split(' ')

        if len(data) == 4:
            try:
                if 'uas' in msg:
                    filename = downloadFile(driver)
                    sleep(2)
                    moveFiles(filename)
                    msgreply = inputNilaiByExcel(
                        filename, 'uas', kelas.getTahunID(), nomor)
                    removeFile(filename)
                elif 'uts' in msg:
                    filename = downloadFile(driver)
                    sleep(2)
                    moveFiles(filename)
                    msgreply = inputNilaiByExcel(
                        filename, 'uts', kelas.getTahunID(), nomor)
                    removeFile(filename)
                else:
                    msgreply = 'Salah keyword bosque..'
            except FileNotFoundError:
                msgreply = 'Gak ada filenya....'
            except Exception as e:
                msgreply = 'Ada masalah di kodingannya... '+str(e)
        else:
            try:
                jenis = data[3].lower() if data[3].lower(
                ) == 'uts' or data[3].lower() == 'uas' else False
                if jenis.lower() == 'uts':
                    nilai = data[data.index('uts')+1] if all(char.isdigit() for char in data[data.index('uts')+1]) and (
                        int(data[data.index('uts')+1]) <= 100 and int(data[data.index('uts')+1]) >= 0) else False
                elif jenis.lower() == 'uas':
                    nilai = data[data.index('uas')+1] if all(char.isdigit() for char in data[data.index('uas')+1]) and (
                        int(data[data.index('uas')+1]) <= 100 and int(data[data.index('uas')+1]) >= 0) else False

                npm = data[data.index('npm')+1] if all(char.isdigit()
                                                       for char in data[data.index('npm')+1]) else False
                if 'matkul' in data and 'jadwal' not in data:
                    matkul = data[data.index('matkul')+1] if any(char.isdigit()
                                                                 for char in data[data.index('matkul')+1]) else False
                    if jenis and nilai and npm and matkul:
                        data = {
                            'tahun': kelas.getTahunID(),
                            'kode_matkul': matkul,
                            'npm': npm,
                            'nilai': nilai,
                            'jadwal': 0
                        }
                        msgreply = inputNilaiByMesssage(data, jenis, nomor)
                    else:
                        msgreply = 'Salah keyword bosque...'
                elif 'jadwal' in data and 'matkul' not in data:
                    jadwal = data[data.index('jadwal')+1] if any(char.isdigit()
                                                                 for char in data[data.index('jadwal')+1]) else False
                    if jenis and nilai and npm and jadwal:
                        data = {
                            'tahun': kelas.getTahunID(),
                            'kode_matkul': 0,
                            'npm': npm,
                            'nilai': nilai,
                            'jadwal': jadwal
                        }
                        msgreply = inputNilaiByMesssage(data, jenis, nomor)
                    else:
                        msgreply = 'Salah keyword bosque.............'
                else:
                    msgreply = 'Salah keyword bosque................'
            except:
                msgreply = 'Salah keyword bosque....'
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply


def downloadFile(driver):
    filecheck = driver.find_elements_by_class_name('_23z4j')[-1]
    filename = driver.find_elements_by_class_name('_1VzZY')[-1].text
    driver.find_elements_by_class_name('WtawS')[-1].click()
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


def checkDosen(nomor, tahun, matkul=0, jadwal=0):
    db = dbConnectSiap()
    if matkul != 0:
        query = """
            select distinct(Nama) from simak_trn_jadwal where DosenID = (select Login from simak_mst_dosen where Handphone = '"""+nomor+"""') and TahunID = '"""+tahun+"""' and MKKode = '"""+matkul+"""'
        """
    elif jadwal != 0:
        query = """
            select distinct(Nama) from simak_trn_jadwal where DosenID = (select Login from simak_mst_dosen where Handphone = '""" + nomor + """') and TahunID = '""" + tahun + """' and JadwalID = '""" + jadwal + """'
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
    if data['kode_matkul'] != 0:
        query = """
            update simak_trn_krs set uts='"""+str(data['nilai'])+"""' where MhswID='"""+str(data['npm'])+"""' 
            and MKKode='"""+str(data['kode_matkul'])+"""' and TahunID='"""+str(data['tahun'])+"""';
        """
    elif data['jadwal'] != 0:
        query = """
            update simak_trn_krs set uts='"""+str(data['nilai'])+"""' where MhswID='"""+str(data['npm'])+"""' 
            and JadwalID='"""+str(data['jadwal'])+"""' and TahunID='"""+str(data['tahun'])+"""';
        """

    with db:
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        if cur.rowcount > 0:
            return 'Berhasil input bosque'
        else:
            return 'Blm berhasil bosque, mungkin npm ato matkul salah ato nilai yg diinput sama kyk sebelumnya'


def inputNilaiUAS(data):
    db = dbConnectSiap()
    if data['kode_matkul'] != 0:
        query = """
            update simak_trn_krs set uas='"""+str(data['nilai'])+"""' where MhswID='"""+str(data['npm'])+"""' 
            and MKKode='"""+str(data['kode_matkul'])+"""' and TahunID='"""+str(data['tahun'])+"""';
        """
    elif data['jadwal'] != 0:
        query = """
            update simak_trn_krs set uas='"""+data['nilai']+"""' where MhswID='"""+data['npm']+"""' 
            and JadwalID='"""+str(data['jadwal'])+"""' and TahunID='"""+str(data['tahun'])+"""';
        """
    with db:
        cur = db.cursor()
        cur.execute(query)
        db.commit()
        if cur.rowcount > 0:
            return 'Berhasil input bosque'
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
            return datetime.strptime("0000-00-00", '%Y-%m-%d').date()


def getProdi(matkul):
    db = dbConnectSiap()
    query = """
        SELECT ProdiID FROM simpati.simak_trn_jadwal where MKKode='"""+matkul+"""' order by TahunID DESC limit 1
    """

    with db:
        cur = db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        if row is not None:
            return row[0].replace(".", "")
        else:
            return False


def inputByExcel(file, jenis, tahun, func, nomor):
    book = openpyxl.load_workbook(file,data_only=True)
    sheet = book.active
    kode_matkul = sheet["C5"].value.replace(
        ":", "").replace("/", "").split()[0]
    
    prodi = getProdi(kode_matkul)
    tgl = getTanggalNilai(tahun, prodi)
    today = datetime.today().date()
    
    print(tgl, today)
    if tgl >= today:
        if checkDosen(nomor, tahun, matkul=kode_matkul):
            kelas = convertKelas(sheet["C6"].value.replace(":", "").strip())
            mahasiswas = getMahasiswa(kode_matkul, tahun, kelas)
            if mahasiswas:
                length = len(mahasiswas)
                npms = sheet['B10': 'B'+str(9+length)]
                nilais = sheet['E10': 'E'+str(9+length)]
                cells = dict(zip(npms, nilais))
                for k, v in cells.items():
                    if k[0].value is not None:
                        npm = k[0].value
                    else:
                        break
                    data = {
                        'tahun': tahun,
                        'kode_matkul': kode_matkul,
                        'npm':  npm,
                        'nilai': str(v[0].value) if v[0].value is not None else '0',
                    }
                    
                    # print(jenis, func, npm, str(v[0].value) if v[0].value is not None else '0')
                    if jenis.lower() == 'uts':
                        func(data)
                    elif jenis.lower() == 'uas':
                        func(data)
                    else:
                        continue
                try:
                    if jenis.lower() == 'uts':
                        msg = cek_nilai.checkNilaiUTS(tahun, "yang dimasukan tadi", kode_matkul=kode_matkul, jadwal=0, kelas=kelas)
                    elif jenis.lower() == 'uas':
                        msg = cek_nilai.checkNilaiUAS(tahun, "yang dimasukan tadi", kode_matkul=kode_matkul, jadwal=0, kelas=kelas)
                    else:
                        pass
                except:
                    msg = 'Udh masuk bosque'
            else:
                msg = 'Kesalahan pada file bosque'
        else:
            msg = 'Ohh tidak bisa bosque, Anda tidak berhak'
    else:
        msg = "Mana sempat, sudah telat"

    return msg


def inputNilaiByExcel(file, jenis, tahun, nomor):

    today = datetime.today().date()
    book = openpyxl.load_workbook(file,data_only=True)
    sheet = book.active
    cek_ujian = sheet["E9"].value
    # print(cek_ujian)
    if jenis.lower() == 'uts' and 'uts' in str(cek_ujian).lower():
        # uts = getTanggalUTS(tahun)

        # if uts[0] <= today and uts[1] >= today and uts:
        #     msg = inputByExcel(file, jenis, tahun, inputNilaiUTS, nomor)
        # else:
        #     msg = 'Gak bisa lagi bosque'
        msg = inputByExcel(file, jenis, tahun, inputNilaiUTS, nomor)

    elif jenis.lower() == 'uas' and 'uas' in str(cek_ujian).lower():
        # uas = getTanggalUAS(tahun)
        # if uas[0] <= today and uas[1] >= today and uas:
        #     msg = inputByExcel(file, jenis, tahun, inputNilaiUAS, nomor)
        # else:
        #     msg = 'Gak bisa lagi bosque'
        msg = inputByExcel(file, jenis, tahun, inputNilaiUAS, nomor)
    else:
        msg = 'Ujian apa nih bosque, salah file mereun.. ato udh diubah format filenya ya..., hayoo lo...'

    return msg


def inputNilaiByMesssage(data, jenis, nomor):

    if checkDosen(nomor, data['tahun'], matkul=data['kode_matkul'], jadwal=data['jadwal']):

        prodi = getProdi(data['kode_matkul'])
        tgl = getTanggalNilai(data['tahun'], prodi)
        today = datetime.today().date()

        if jenis.lower() == 'uts':
            uts = getTanggalUTS(data['tahun'])
            if tgl >= today:
                # if uts[0] <= today and uts[1] >= today and uts:
                msg = inputNilaiUTS(data)
            else:
                msg = 'Gak bisa lagi bosque'

        elif jenis.lower() == 'uas':
            uas = getTanggalUAS(data['tahun'])
            if tgl >= today:
                # if uas[0] <= today and uas[1] >= today and uas:
                msg = inputNilaiUAS(data)
            else:
                msg = 'Gak bisa lagi bosque'
        else:
            msg = 'Ujian apa nih bosque'
    else:
        msg = 'ohh tidak bisa'
    return msg
