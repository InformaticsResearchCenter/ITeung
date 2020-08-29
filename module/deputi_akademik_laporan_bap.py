from module import kelas, bkd, cek_tanda_tangan_bap
from zipfile import ZipFile
from lib import numbers, wa
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime

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
    num = numbers.normalize(data[0])
    msgreply = f'okeeeeeee tunggu yaaa sekitaran 15-20 menit, dan akan {config.bot_name} kirim ke linknya nanti ke nomor {num} yaaa....'
    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0], num], cwd=config.cwd)
    return msgreply


def run(num):
    link={}
    dmy=datetime.now().strftime("%d-%m-%Y")
    hms=datetime.now().strftime("%H:%M:%S")
    prodiidandsingkatan = getProdiIDAndSingkatan()
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
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()
        gauth.SaveCredentialsFile("mycreds.txt")
        drive=GoogleDrive(gauth)
        file1=drive.CreateFile({'title': f'{singkatan} {dmy} {hms}.zip'})
        file1.SetContentFile(f'{os.getcwd()}\\{singkatan}.zip')
        file1.Upload()
        file1.InsertPermission({
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader'})
        link[f'{singkatan}']=file1['alternateLink']
    msgreply=f'ini yaaa link berdasarkan prodinyaa....{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}'
    for data in link.items():
        msgreply+=f'{data[0]}: {data[1]}{config.whatsapp_api_lineBreak}'
    wa.setOutbox(num, msgreply)