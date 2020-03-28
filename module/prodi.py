# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 06:29:37 2020

@author: rolly
"""
from dateutil.parser import parse
from lib import dawet, wa
from numba import jit
import datetime
import pymysql
import config

@jit(nopython=True)
def dbConnect():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

@jit(nopython=True)
def getWaitingMessage(module):
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM waiting_message WHERE module_name = '%s' ORDER BY RAND() LIMIT 1"%(module)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content

@jit(nopython=True)
def replymsg(driver, msg):
    wa.typeAndSendMessage(driver, getWaitingMessage('prodi'))

    msgs = list(msg.split(" "))
    getIndex = msgs.index("nilai")

    npm = msgs[getIndex+1]
    pertemuan = msgs[getIndex+2]
    hasil = getNilaiMahasiswa(npm, pertemuan)

    if hasil == "invalid":
        res="maaf npmnya ga #BOTNAME# temuin :'-(, mungkin npmnya salah, coba dicek lagi deh :-)"
    elif hasil == "pertemuan_invalid":
        res="format salah, contoh: pertemuan1"
    else:
        res="NPM: "+npm+", Nama: "+hasil[1]+", Nilai: "+hasil[0]+", Nilai rata-rata: "+hasil[2]
    return res

@jit(nopython=True)
def getNilaiMahasiswa(npm, pertemuan):
    if npm[:3] == "118":
        db = dawet.Dawet("BukuProyek2")
    elif npm[:3] == "117":
        db = dawet.Dawet("BukuProyek3")
    else:
        db = dawet.Dawet("BukuInternship1")

    nilai = db.getData(npm, pertemuan, 0)

    if nilai == "not_found":
        return "invalid"
    elif nilai == "pertemuan_not_found":
        return "pertemuan_invalid"
    else:
        nama_mahasiswa = db.getData(npm, "nama", 0)
        nilai_rata = db.getData(npm, "rata_rata", 0)

        hasil = []
        hasil.append(nilai)
        hasil.append(nama_mahasiswa)
        hasil.append(nilai_rata)

        return hasil

@jit(nopython=True)
def cekJadwalSidang(pilihan):
    db = dawet.Dawet("Jadwal_Sidang_Proyek_2")

    allData = db.getAllData(1)

    sekarang = datetime.datetime.now().date()
    besok = sekarang + datetime.timedelta(days=1)
    kemaren = sekarang - datetime.timedelta(days=1)
    lusa = sekarang + datetime.timedelta(days=2)

    if pilihan == "sekarang":
        pilihanTanggal = sekarang
        runnerVariable = 1
    if pilihan == "besok":
        pilihanTanggal = besok
        runnerVariable = 1
    if pilihan == "kemarin":
        pilihanTanggal = kemaren
        runnerVariable = 1
    if pilihan == "lusa":
        pilihanTanggal = lusa
        runnerVariable = 1

    if runnerVariable == 1:
        for data in allData:
            try:
                tanggal = parse(data[0]).date()
                print(pilihanTanggal)

                print(tanggal)

                if pilihanTanggal == tanggal:
                    getIndex = allData.index(data)

                    nextData = allData[getIndex:]

                    for nextdata in nextData:
                        if nextdata[0] == '':
                            getIndexNull = nextData.index(nextdata)

                    result = nextData[:getIndexNull]

                    return result

            except:
                print("beda")
    else:
        return "no_pilihan"
