from module import kelas
from lib import wa, reply, message, numbers
import os, config
import pandas as pd

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    num = numbers.normalize(data[0])
    kodeDosen = kelas.getKodeDosen(num)
    # tahun_id = '20192'
    tahun_id = kelas.getTahunID()
    try:
        npm = [npm for npm in data[3].split(' ') if npm.isdigit() and len(npm) == 7][0]
        if checkMhs(npm, kodeDosen):
            approveRevisiSidang(npm, kodeDosen, tahun_id)        
            msgreply = f"Dah diapprove ya {npm} oleh {kodeDosen}"
            if checkRevisiStatus(npm, tahun_id):
                kategori = getKategoriSidang(npm, tahun_id)
                makeBeritaAcara(npm, tahun_id, kategori)
            else:
                pass
                print("Belum boleh boy")
        else:
            msgreply = f"Anda bukan penguji {npm}"
            
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def checkStatusSidang(npm, tahunID, kategori):
    db=kelas.dbConnect()
    sql=f"SELECT npm FROM sidang_data WHERE npm = '{npm}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}'"
    print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False

def makeBeritaAcara(npm, tahunID, kategori):
    db=kelas.dbConnect()
    if not checkStatusSidang(npm, tahunID, kategori):
        sql = f"INSERT INTO sidang_data (npm, tahun_id, kategori) VALUE ('{npm}', '{tahunID}', '{kategori}')"
        with db:
            cur=db.cursor()
            cur.execute(sql)
    else:
        pass
        print("Lewat aja ya")

def getKategoriSidang(npm, tahunID):
    db = kelas.dbConnectSiap()
    sql = f"SELECT distinct(Tipe) FROM simpati.simak_croot_bimbingan WHERE MhswID = '{npm}' AND TahunID = '{tahunID}' order by TahunID DESC"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

def checkRevisiStatus(npm, tahunID):
    db=kelas.dbConnect()
    sql=f"SELECT COUNT(DISTINCT(penguji)) as total FROM revisi_data WHERE npm ='{npm}' AND tahun_id = '{tahunID}' AND status = 'True'"
    print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            print(row[0])
            if int(row[0]) == 2:
                return True
            else:
                return False
        else:
            return False

def approveRevisiSidang(npm, penguji, tahun_id):
    db=kelas.dbConnect()
    sql=f'UPDATE revisi_data SET status="True" WHERE npm="{npm}" and penguji="{penguji}" and tahun_id="{tahun_id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        
def checkMhs(npm, kodeDosen):
    df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')
    df.set_index('npm', inplace=True)
    listPem = ['pem3', 'pem4', ]
    pem = df.loc[int(npm), listPem].values.tolist()
    
    if kodeDosen in pem:
        return True
    else:
        return False
    