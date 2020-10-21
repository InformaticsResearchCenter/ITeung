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
        nipyKaBaak = getKaBaak()
        kodeKaBaak = getKodeDosen(nipyKaBaak)
        
        if(kodeDosen == kodeKaBaak):
            datas = dataSumbitSKMK()
            msgreply = "*Data yang minta SKMK:*\n\n"
            if datas:
                for i, data in enumerate(datas):
                    msgreply += f"{int(i)+1}. {data[0]}\n"
            else:
                msgreply += "Tidak ada yg minta.."
        else:
            msgreply = "Haha.. lucu ya, ternyata anda bukan siapa-siapa..."
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def getKaBaak():
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY FROM simpati.simak_mst_pejabat WHERE JenisJabatanID='11'"
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
        
def dataSumbitSKMK():
    db = kelas.dbConnect()
    sql="select npm from skmk_data where approve is null"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows:
            return rows
    return False