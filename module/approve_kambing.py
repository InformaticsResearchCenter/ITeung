from module import kelas, kambing
from lib import message, numbers, reply, wa

import os, config

def getDataPembimbing(npm, kode_dosen):
    db=kelas.dbConnect()
    sql=f"select * from bimbingan_data where npm={npm} and (pembimbing1='{kode_dosen}' or pembimbing2='{kode_dosen}')"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row
        else:
            return None


def getAllDataMahasiswaAndPembimbing(kode_dosen):
    db=kelas.dbConnect()
    sql=f"select * from bimbingan_data where pembimbing1='{kode_dosen}' or pembimbing2='{kode_dosen}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchall()
        if row is not None:
            return row
        else:
            return None


def setSingleApprovalBimbingan(npm, kode_dosen, pembimbing_ke, status):
    db = kelas.dbConnect()
    sql=f"UPDATE `wanda`.`bimbingan_data` SET `approval_{pembimbing_ke}` = '{status}' WHERE `npm` = {npm} and `{pembimbing_ke}` = '{kode_dosen}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)


def cekApprovalTrueorFalse(npm, pembimbingke):
    db = kelas.dbConnect()
    sql=f"select approval_{pembimbingke} from bimbingan_data where npm={npm}"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            if row[0] == 'true':
                return True
            else:
                return False
        else:
            return False

def bimbinganCekApprovalBimbingan(kodedosen):
    db=kelas.dbConnect()
    sql=f"select npm from bimbingan_data where pembimbing1='{kodedosen}' or pembimbing2='{kodedosen}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows != ():
            sudah=[]
            siap=[]
            belum=[]
            for npm in rows:
                npm=npm[0]
                if len(kambing.getAllDataBimbingan(npm)) < 16:
                    belum.append(npm)
                else:
                    data=getDataPembimbing(npm, kodedosen)
                    pembimbingke=pembimbingPositionAs(data, kodedosen)
                    if cekApprovalTrueorFalse(npm, pembimbingke):
                        sudah.append(npm)
                    else:
                        siap.append(npm)
            return sudah, siap, belum
        else:
            return None

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    num=numbers.normalize(data[0])
    msg=message.normalize(data[3])
    npm=msg.split(' ')[-1]
    kodedosen = kelas.getKodeDosen(num)
    if npm == "all":
        msgreply = 'ok sudah di approve semua berkas KAMBING-nya sama #BOTNAME# yyyyaaa'
        sudah, siap, belum=bimbinganCekApprovalBimbingan(kodedosen)
        if siap == []:
            msgreply='yah datanya belum ada lagi nih yang siap untuk di approve, coba deh cek dengan cara ketik #BOTNAME# cek approval kambing'
        else:
            for j in siap:
                pembimbing_ke = pembimbingPositionAs(getDataPembimbing(j, kodedosen), kodedosen)
                setSingleApprovalBimbingan(j, kodedosen, pembimbing_ke, 'true')
                nama_mahasiswa=kelas.getStudentNameOnly(j)
                msgreply+=f'\n\nNPM: {j}\nNama: {nama_mahasiswa}'
    else:
        data=getDataPembimbing(npm, kodedosen)
        if data == None:
            msgreply=f'npm {npm} tidak ditemukan didata bimbingan Bapak/Ibu dosen'
        else:
            pembimbing_ke=pembimbingPositionAs(data, kodedosen)
            setSingleApprovalBimbingan(npm, kodedosen, pembimbing_ke, 'true')
            nama_mahasiswa = kelas.getStudentNameOnly(npm)
            msgreply='oke sudah #BOTNAME# approve untuk KAMBING'
            msgreply+=f'\n\nNPM: {npm}\nNama: {nama_mahasiswa}'
    return msgreply


def pembimbingPositionAs(data, kodedosen):
    wekwek = data.index(kodedosen)
    if wekwek == 1:
        pembimbing_ke = 'pembimbing1'
    else:
        pembimbing_ke = 'pembimbing2'
    return pembimbing_ke