from module import kelas
from lib import wa, reply, numbers

import os

def auth(data):
    if kelas.getKodeDosen(data[0]) != '':
        ret = True
    else:
        ret = False
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    num = numbers.normalize(data[0])
    kodeDosen = kelas.getKodeDosen(num)
    
    msgreply = ""
    try:
        nipyWadir1 = getWadir1()
        kodeWadir1 = getKodeDosen(nipyWadir1)
        
        nipyDirektur = getDirektur()
        kodeDirektur = getKodeDosen(nipyDirektur)
        
        if(kodeDosen == kodeWadir1):
            datas = dataPengajuSKPWadir1()
            msgreply = "*Data yang minta SKP:*\n\n"
            if datas:
                for i, data in enumerate(datas):
                    msgreply += f"{int(i)+1}. {data[0]}-{data[1]}\n"
            else:
                msgreply += "Tidak ada yg minta.."
        elif (kodeDosen == kodeDirektur):
            datas = dataPengajuSKPDirektur()
            msgreply = "*Data yang minta SKP:*\n\n"
            if datas:
                for i, data in enumerate(datas):
                    msgreply += f"{int(i)+1}. {data[0]}-{data[1]}\n"
            else:
                msgreply += "Tidak ada yg minta.."
        else:
            msgreply = "Ketika dia telah punya pasangan dan anda tidak punya hak untuk mengakses ini...."
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def getWadir1():
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY FROM simak_mst_pejabat WHERE JenisJabatanID='2'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

def getDirektur():
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY FROM simak_mst_pejabat WHERE JenisJabatanID='1'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None
    
def getKodeDosen(nik):
    db = kelas.dbConnectSiap()
    sql = f'select Login from simak_mst_dosen where NIPY="{nik}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None
        
def dataPengajuSKPWadir1():
    db = kelas.dbConnect()
    sql="select npm, nama from skp_data where (ajukan is not null and ajukan <> '-') and (wadir1 is null or wadir1 = '-')"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows:
            return rows
    return False

def dataPengajuSKPDirektur():
    db = kelas.dbConnect()
    sql="select npm, nama from skp_data where (ajukan is not null and ajukan <> '-') and (direktur is null or direktur = '-')"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows:
            return rows
    return False