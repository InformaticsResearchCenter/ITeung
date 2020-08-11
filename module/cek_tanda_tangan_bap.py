from module import kelas
from lib import numbers, wa, reply, message

import subprocess, config, os

def getMateriFromJadwalID(jadwalid):
    db = kelas.dbConnectSiap()
    sql = f"select MP from simak_trn_presensi_dosen WHERE `JadwalID` = {jadwalid} ORDER BY Pertemuan ASC"
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


def getListJadwalIDfromDeputi(status, prodiid):
    db=kelas.dbConnectSiap()
    if status:
        sql=f"select JadwalID from simak_trn_jadwal where TahunID={kelas.getTahunID()} and ProdiID='{prodiid}'"
    else:
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
    if None in MateriToList or '' in MateriToList:
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
        if row[0] == 'true':
            return True
        else:
            return False


def cekStatusBKDDeputi(jadwalid):
    db=kelas.dbConnectSiap()
    sql=f'select BKD_Deputi from simak_trn_jadwal where JadwalID={jadwalid}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row[0] == 'true':
            return True
        else:
            return False


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
    msgsudah = ''
    for i in sudah:
        kelas_info = kelas.getMatakuliahInfowithJadwalID(i)
        msgsudah += f'{config.whatsapp_api_lineBreak}{kelas_info[0]} | {getNamaProdiFromProdiID(kelas_info[5].split(".")[1])} | {kelas_info[12]} | {kelas.getNamaDosen(kelas_info[21])}'
    msgsudah += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}'
    msgsiap = ''
    for i in siap:
        kelas_info = kelas.getMatakuliahInfowithJadwalID(i)
        msgsiap += f'{config.whatsapp_api_lineBreak}{kelas_info[0]} | {getNamaProdiFromProdiID(kelas_info[5].split(".")[1])} | {kelas_info[12]} | {kelas.getNamaDosen(kelas_info[21])}'
    msgsiap += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}'
    msgbelum = ''
    for i in belum:
        kelas_info = kelas.getMatakuliahInfowithJadwalID(i)
        msgbelum += f'{config.whatsapp_api_lineBreak}{kelas_info[0]} | {getNamaProdiFromProdiID(kelas_info[5].split(".")[1])} | {kelas_info[12]} | {kelas.getNamaDosen(kelas_info[21])}'
    msgbelum += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}'
    msgreply = f"BAP yang sudah ditandatangani ada: {len(sudah)} berkas{msgsudah}BAP yang siap ditandatangani ada: {len(siap)} berkas{msgsiap}BAP yang belum siap ditandatangani ada: {len(belum)} berkas{msgbelum}"
    return msgreply, sudah, siap, belum

def infoBAPDeputi(msg):
    msgs=msg.split(' ')[-1]
    if msgs == 'all':
        JadwalIDDataDeputi=getListJadwalIDfromDeputi(False, '')
    else:
        JadwalIDDataDeputi=getListJadwalIDfromDeputi(True, getProdiIDfromSingkatan(msgs))
    sudah=[]
    siap=[]
    belum=[]
    for jadwalid in JadwalIDDataDeputi:
        statusmateri=cekMateriPerkuliahan(jadwalid[0])
        statusttd=cekStatusBKDDeputi(jadwalid[0])
        if statusmateri == False and statusttd == False:
            belum.append(jadwalid[0])
        elif statusmateri == True and statusttd == False:
            siap.append(jadwalid[0])
        else:
            sudah.append(jadwalid[0])
    msgsudah=''
    for i in sudah:
        kelas_info=kelas.getMatakuliahInfowithJadwalID(i)
        msgsudah+=f'{config.whatsapp_api_lineBreak}{kelas_info[0]} | {getNamaProdiFromProdiID(kelas_info[5].split(".")[1])} | {kelas_info[12]} | {kelas.getNamaDosen(kelas_info[21])}'
    msgsudah+=f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}'
    msgsiap=''
    for i in siap:
        kelas_info=kelas.getMatakuliahInfowithJadwalID(i)
        msgsiap+=f'{config.whatsapp_api_lineBreak}{kelas_info[0]} | {getNamaProdiFromProdiID(kelas_info[5].split(".")[1])} | {kelas_info[12]} | {kelas.getNamaDosen(kelas_info[21])}'
    msgsiap += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}'
    msgbelum=''
    for i in belum:
        kelas_info=kelas.getMatakuliahInfowithJadwalID(i)
        msgbelum+=f'{config.whatsapp_api_lineBreak}{kelas_info[0]} | {getNamaProdiFromProdiID(kelas_info[5].split(".")[1])} | {kelas_info[12]} | {kelas.getNamaDosen(kelas_info[21])}'
    msgbelum += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}'
    msgreply=f"BAP yang sudah ditandatangani ada: {len(sudah)} berkas{msgsudah}BAP yang siap ditandatangani ada: {len(siap)} berkas{msgsiap}BAP yang belum siap ditandatangani ada: {len(belum)} berkas{msgbelum}"
    return msgreply, sudah, siap, belum


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


def getNamaProdiFromProdiID(prodiid):
    db=kelas.dbConnectSiap()
    sql=f'select Nama from simak_mst_prodi where ProdiID={prodiid}'
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
    msg=message.normalize(data[3])
    data=f'{num};{msg}'
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0], data], cwd=config.cwd)
    return wmsg


def run(data):
    num=data.split(';')[0]
    msg=data.split(';')[1]
    if isKaprodi(getNIPYfromHandphone(num)):
        status='kaprodi'
    else:
        status='deputi'
    if status == 'kaprodi':
        msgreply=infoBAPKaprodi(f'.{kelas.getAllDataDosens(kelas.getKodeDosen(num))[20]}.')
    else:
        msgreply=infoBAPDeputi(msg)
    wa.setOutbox(numbers.normalize(num), msgreply[0])


def getProdiIDfromSingkatan(singkatan):
    db=kelas.dbConnectSiap()
    sql=f"select ProdiID from simak_mst_prodi where Singkatan = '{singkatan}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return f".{row[0]}."
        else:
            return None