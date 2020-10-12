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
    # print(kodeDosen)
    # tahunID = '20192'
    tahun_id = kelas.getTahunID()
    try:
        npm = [npm for npm in data[3].split(' ') if npm.isdigit() and len(npm) == 7][0]
        if checkMhs(npm, kodeDosen): 
            if checkRevisiStatus(npm, tahunID):
                df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')    
                listPem = ['pem1', 'pem2', 'pem3', 'pem4', 'koor']
                pem = df.loc[(df["npm"] == int(npm)) & (df["tahun"] == int(tahunID)), listPem].values.tolist()[0]
                
                peran = f"{kodeDosen} sebagai "
                nip = getKaProdi('14')
                kaprodiID = getDosenIDfromNIPY(nip)
                
                kategori = getKategoriSidang(npm, tahunID)
                kategori = "ta"
                
                if pem[0] == kodeDosen:
                    role = "pembimbing_utama"
                    approveBASidang(kodeDosen, role, tahunID, kategori, npm)
                    peran += 'Pembimbing Utama '
                
                if pem[1] == kodeDosen:
                    role = "pembimbing_pendamping"
                    approveBASidang(kodeDosen, role, tahunID, kategori, npm)
                    peran += 'Pembimbing Pendamping '
                
                if pem[2] == kodeDosen:
                    role = "penguji_utama"
                    approveBASidang(kodeDosen, role, tahunID, kategori, npm)
                    peran += 'Penguji Utama '
                
                if pem[3] == kodeDosen:
                    role = "penguji_pendamping"
                    approveBASidang(kodeDosen, role, tahunID, kategori, npm)
                    peran += 'Penguji Pendamping '
                    
                if pem[4] == kodeDosen:
                    if checkKoor(npm, tahunID, kategori):
                        role = "koordinator"
                        approveBASidang(kodeDosen, role, tahunID, kategori, npm)
                        peran += 'Koordinator '
                    else:
                        pass

                if kaprodiID == kodeDosen:
                    if checkKaprodi(npm, tahunID, kategori):
                        role = "kaprodi"
                        approveBASidang(kodeDosen, role, tahunID, kategori, npm)
                        peran = 'Kepala Prodi '
                    else:
                        pass
                
                msgreply = f"Dah diapprove ya {npm} oleh {peran}"
            else:
                msgreply = f"Blm acc revisi {npm} dari kedua penguji nih......"
        else:
            msgreply = f"Anda bukan siapa-siapa untuk {npm}"
            
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def checkKoor(npm, tahunID, kategori):
    db=kelas.dbConnect()
    sql=f"SELECT npm FROM sidang_data WHERE npm='{npm}' and tahun_id='{tahunID}' and kategori = '{kategori}' and (penguji_utama is not null and penguji_utama <> '') and (penguji_pendamping is not null and penguji_pendamping <> '') and (pembimbing_utama is not null and pembimbing_utama <> '') and (pembimbing_pendamping is not null and pembimbing_pendamping <> '')"
    
    # print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False

def checkKaprodi(npm, tahunID, kategori):
    db=kelas.dbConnect()
    sql=f"SELECT npm FROM sidang_data WHERE npm='{npm}' and tahun_id='{tahunID}' and kategori = '{kategori}' and (penguji_utama is not null and penguji_utama <> '') and (penguji_pendamping is not null and penguji_pendamping <> '') and (pembimbing_utama is not null and pembimbing_utama <> '') and (pembimbing_pendamping is not null and pembimbing_pendamping <> '') and (koordinator is not null and koordinator <> '')"
    
    # print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False

def approveBASidang(kodeDosen, role, tahunID, kategori, npm):
    db=kelas.dbConnect()
    sql=f'UPDATE sidang_data SET {role}="{kodeDosen}" WHERE npm="{npm}" and tahun_id="{tahunID}" and kategori = "{kategori}"'
    # print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)

def getKaProdi(prodiid):
    db = kelas.dbConnectSiap()
    sql = f"select NIPY from simak_mst_pejabat where ProdiID={prodiid} and JenisJabatanID=5"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None
        
def getDosenIDfromNIPY(nipy):
    db = kelas.dbConnectSiap()
    sql = f'select Login from simak_mst_dosen where NIPY="{nipy}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

def getKategoriSidang(npm, tahunID):
    db = kelas.dbConnectSiap()
    sql = f"SELECT distinct(Tipe) FROM simpati.simak_croot_bimbingan WHERE MhswID = '{npm}' AND TahunID = '{tahunID}'"
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
    # print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            # print(row[0])
            if int(row[0]) == 2:
                return True
            else:
                return False
        else:
            return False
        
def checkMhs(npm, kodeDosen):
    df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')
    df.set_index('npm', inplace=True)
    listPem = ['pem1','pem2','pem3', 'pem4', 'koor']
    pem = df.loc[int(npm), listPem].values.tolist()
    nip = getKaProdi('14')
    kaprodiID = getDosenIDfromNIPY(nip)
    pem.append(kaprodiID)
    print(pem)
    if kodeDosen in pem:
        return True
    else:
        return False
    