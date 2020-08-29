from module import kelas, bkd, cek_tanda_tangan_bap
from zipfile import ZipFile
from lib import numbers

import os, subprocess, config

def auth(data):
    if cek_tanda_tangan_bap.isDeputiAkademik(cek_tanda_tangan_bap.getNIPYfromHandphone(data[0])):
        ret=True
    else:
        ret=False
    return ret

def getJadwalIDFullApproval(prodiid):
    db = kelas.dbConnectSiap()
    sql = f'select JadwalID from simak_trn_jadwal where TahunID=20192 and BKD_Prodi="true" and BKD_Deputi="true" and ProdiID=".{prodiid}."'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        return cur.fetchall()


def getMkKodeFromJadwalID(jadwalid):
    db = kelas.dbConnectSiap()
    sql = f'select MKKode from simak_trn_jadwal where JadwalID={jadwalid}'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]


def getProdiIDAndSingkatan():
    db = kelas.dbConnectSiap()
    sql = f'select ProdiID, Singkatan from simak_mst_prodi'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        return cur.fetchall()


def replymsg(driver, data):
    kodedosen = kelas.getKodeDosen(data[0])
    num = numbers.normalize(data[0])
    msgreply = f'okeeeeeee tunggu yaaa sekitaran 15-20 menit, dan akan {config.bot_name} kirim ke email yang {kelas.getEmailDosen(kodedosen)} yaaa....'
    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0], num], cwd=config.cwd)
    return msgreply


def run(num):
    prodiidandsingkatan = getProdiIDAndSingkatan()
    zippath = []
    for prodiID, singkatan in prodiidandsingkatan:
        mkkodelist = []
        for i in getJadwalIDFullApproval(prodiID):
            mkkode = getMkKodeFromJadwalID(i[0])
            if mkkode not in mkkodelist:
                mkkodelist.append(mkkode)
            else:
                continue
        foldername = 'bkd'
        pathperprodi = []
        for i in mkkodelist:
            abc = bkd.getFilePath(i, foldername)
            for i in abc:
                pathperprodi.append(i)
        with ZipFile(f'{singkatan}.zip', 'w') as zip:
            for file in pathperprodi:
                try:
                    zip.write(file)
                except:
                    print(f'file: {file}, ngga ada')
                    continue
        zippath.append(f'{os.getcwd()}\\{singkatan}.zip')
    bkd.mail(
        kelas.getEmailDosen(kelas.getKodeDosen(num)),
        f'yowwwwwww {config.bot_name} kirim file .zip semua berkas yang udah lengkap approvalnya eheee',
        f'coba dicek dulu yaaaa kalo ada yang kurang bisa di kontak ke admin {config.bot_name} maaciwww..... :9',
        zippath
    )