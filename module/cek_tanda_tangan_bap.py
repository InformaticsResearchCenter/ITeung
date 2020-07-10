from module import kelas
from lib import numbers, wa, reply

import subprocess, config, os

def confirmBKD(jadwalid):
    db=kelas.dbConnectSiap()
    sql=f"UPDATE `simpati`.`simak_trn_jadwal` SET `BKD_Prodi` = 'true' WHERE `JadwalID` = {jadwalid}"
    with db:
        cur=db.cursor()
        cur.execute(sql)


def getMateriFromJadwalID(jadwalid):
    db = kelas.dbConnectSiap()
    sql = f"select MP from simak_trn_presensi_dosen WHERE `JadwalID` = {jadwalid}"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            return rows
        else:
            return None


def materiToList(materiTuple):
    materiData=[]
    for i in materiTuple:
        materiData.append(i[0])
    return materiData


def getListJadwalIDfromKaprodi(prodiID):
    db=kelas.dbConnectSiap()
    sql=f"select JadwalID from simak_trn_jadwal where TahunID={kelas.getTahunID()} and ProdiID='{prodiID}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            return rows
        else:
            return None


def getListJadwalIDfromDeputi():
    db=kelas.dbConnectSiap()
    sql=f"select JadwalID from simak_trn_jadwal where TahunID={kelas.getTahunID()}"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            return rows
        else:
            return None


def cekMateriPerkuliahan(jadwalid):
    MateriTuple = getMateriFromJadwalID(jadwalid)
    MateriToList = materiToList(MateriTuple)
    if None in MateriToList:
        ret = False
    else:
        ret = True
    return ret


def cekStatusBKDKaprodi(jadwalid):
    db=kelas.dbConnectSiap()
    sql=f'select BKD_Prodi from simak_trn_jadwal where JadwalID={jadwalid}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row[0] == None or row[0] == 'false':
            return False
        else:
            return True


def infoBAPKaprodi(prodiid):
    JadwalIDDataProdi=getListJadwalIDfromKaprodi(prodiid)
    sudah=[]
    siap=[]
    belum=[]
    for jadwalid in JadwalIDDataProdi:
        statusmateri=cekMateriPerkuliahan(jadwalid[0])
        statusttd=cekStatusBKDKaprodi(jadwalid[0])
        if statusmateri == False and statusttd == False:
            belum.append(jadwalid[0])
        elif statusmateri == True and statusttd == False:
            siap.append(jadwalid[0])
        else:
            sudah.append(jadwalid[0])
    msgreply=f"BAP yang sudah ditandatangani ada: {len(sudah)} berkas%0ABAP yang siap ditandatangani ada: {len(siap)} berkas%0ABAP yang belum siap ditandatangani ada: {len(belum)} berkas"
    return msgreply

def infoBAPDeputi():
    JadwalIDDataDeputi=getListJadwalIDfromDeputi()
    sudah=[]
    siap=[]
    belum=[]
    for jadwalid in JadwalIDDataDeputi:
        statusmateri=cekMateriPerkuliahan(jadwalid[0])
        statusttd=cekStatusBKDKaprodi(jadwalid[0])
        if statusmateri == False and statusttd == False:
            belum.append(jadwalid[0])
        elif statusmateri == True and statusttd == False:
            siap.append(jadwalid[0])
        else:
            sudah.append(jadwalid[0])
    msgreply=f"BAP yang sudah ditandatangani ada: {len(sudah)} berkas%0ABAP yang siap ditandatangani ada: {len(siap)} berkas%0ABAP yang belum siap ditandatangani ada: {len(belum)} berkas"
    return msgreply


def getNIPYfromHandphone(num):
    num=numbers.normalize(num)
    db=kelas.dbConnectSiap()
    sql=f'select NIPY from simak_mst_dosen where Handphone="{num}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def isDeputiAkademik(NIPY):
    db=kelas.dbConnectSiap()
    sql=f'select * from simak_mst_pejabat where NIPY="{NIPY}" and JenisJabatanID=9'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return True
        else:
            return False


def isKaprodi(NIPY):
    db = kelas.dbConnectSiap()
    sql = f'select * from simak_mst_pejabat where NIPY="{NIPY}" and JenisJabatanID=5'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return True
        else:
            return False


def auth(data):
    if isKaprodi(getNIPYfromHandphone(data[0])) or isDeputiAkademik(getNIPYfromHandphone(data[0])):
        return True
    else:
        return False


def replymsg(driver, data):
    num=numbers.normalize(data[0])
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0], num], cwd=config.cwd)
    return wmsg


def run(num):
    if isKaprodi(getNIPYfromHandphone(num)):
        status='kaprodi'
    else:
        status='deputi'
    if status == 'kaprodi':
        msgreply=infoBAPKaprodi(kelas.getAllDataDosens(kelas.getKodeDosen(num))[21])
    else:
        msgreply=infoBAPDeputi()
    wa.setOutbox(numbers.normalize(num), msgreply)