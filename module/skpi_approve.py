import openpyxl
from module import kelas
from lib import wa, reply, numbers
import os

import pandas as pd

def auth(data):
    if kelas.getKodeDosen(data[0]) != '':
        ret = True
    else:
        ret = False
    return ret

def replymsg(driver, data):
    # wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    # wa.typeAndSendMessage(driver, wmsg)
    num = numbers.normalize(data[0])
    
    kodeDosen = kelas.getKodeDosen(num)
    print(kodeDosen)
    msgreply = ""
    try:
        npm = [npm for npm in data[3].split(' ') if npm.isdigit() and len(npm) == 7][0]
        prodiMhs, namaMhs = getMahasiswa(npm)
        nipyKaprodi, namaDosen= getKaprodi(prodiMhs)
        kodeKaprodi = getKodeDosen(nipyKaprodi)
        nipyWadirI, namaWadirI = getWadirI()
        kodeWadirI = getKodeDosen(nipyWadirI)
        if(kodeDosen == kodeWadirI):
            approveSKL(npm, "wadirI", kodeDosen)
            msgreply = f"{namaWadirI} sebagai wadir I telah mengapprove SKL milik {npm} - {namaMhs}"
        elif(kodeDosen == kodeKaprodi):
            approveSKL(npm, "kaprodi", kodeDosen)
            msgreply = f"{namaDosen} sebagai kaprodinya telah mengapprove SKL {npm}-{namaMhs}"
        else:
            msgreply = "Anda bukan siapa-siapa untuknya.."
    except IndexError:
        msgreply = "NPMnya mana sahabat.... atau salah NPM nih Anda... atau NPM gak terdaftar sebagai wisudawan tahun ini..."
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def getMahasiswa(npm):
    db = kelas.dbConnectSiap()
    sql = "select ProdiID, Nama from simak_mst_mahasiswa where MhswID = '{0}'".format(npm)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1]]
        else:
            return False

def getKaprodi(prodi):
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY, Nama FROM simak_mst_pejabat WHERE ProdiID='{prodi}' AND JenisJabatanID=5"
    # print(sql)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1]]
        else:
            return None
    
def getWadirI():
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY, Nama FROM simpati.simak_mst_pejabat WHERE JenisJabatanID='2'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1]]
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


def approveSKL(npm, role, kodeDosen):
    file = f"./skpi/list-skpi/list-wisudawan.xlsx"
    
    dfStatus = pd.read_excel(file)
    noUrut = int(dfStatus.loc[dfStatus["NPM"] == int(npm)].values.tolist()[0][0])
    print(noUrut)
    book = openpyxl.load_workbook(file)
    sheet = book.active
    
    if role == 'wadirI':
        print('C'+str(noUrut-3))
        D = sheet['D'+str(noUrut-3)] 
        D.value = kodeDosen
    elif role == 'kaprodi':
        C = sheet['C'+str(noUrut-3)] 
        C.value = kodeDosen
    
    book.save(file) 
    book.close()

