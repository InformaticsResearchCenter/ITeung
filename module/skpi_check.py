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
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    num = numbers.normalize(data[0])
    print(num)
    kodeDosen = kelas.getKodeDosen(num)
    print(kodeDosen)
    msgreply = ""
    try:
        
        prodi = getProdiDosen(kodeDosen)
        nipyKaprodi, namaDosen = getKaprodi(prodi)
        kodeKaprodi = getKodeDosen(nipyKaprodi)
        nipyWadirI, namaWadirI = getWadirI()
        kodeWadirI = getKodeDosen(nipyWadirI)
        print()
        if(kodeDosen == kodeWadirI):
            datas = dataSumbitSKL()
            msgreply = "*Data yang minta SKL:*\n\n"
            if datas:
                for i, data in enumerate(datas):
                    msgreply += f"{int(i)+1}. {data[1]} - {data[5]}\n"
            else:
                msgreply += "Tidak ada"
        elif(kodeDosen == kodeKaprodi):
            datas = dataSumbitSKL(prodi)
            msgreply = "*Data yang minta SKL:*\n\n"
            if datas:
                for i, data in enumerate(datas):
                    msgreply += f"{int(i)+1}. {data[1]} - {data[5]}\n"
            else:
                msgreply += "Tidak ada"
        else:
            msgreply = "Anda bukan siapa-siapa untuknya.."
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def getProdiDosen(kodeDosen):
    db = kelas.dbConnectSiap()
    sql = f'SELECT Homebase FROM simak_mst_dosen WHERE Login = "{kodeDosen}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None
        
# def getKodeProdi(prodi):
#     prodis = {
#         'd3ti':'13',
#         'd4ti':'14',
#         'd3mi':'23',
#         'd3ak':'33',
#         'd4ak':'34',
#         'd3mb':'43',
#         'd4mb':'44',
#         'd3lb':'53',
#         'd4lb':'54'
#     }    
#     return prodis.get(prodi, 'XXX')

def getKodeProdi(prodi):
    prodis = {
        '13':'d3ti',
        '14':'d4ti',
        '23':'d3mi',
        '33':'d3ak',
        '34':'d4ak',
        '43':'d3mb',
        '44':'d4mb',
        '53':'d3lb',
        '54':'d4lb'
    }    
    return prodis.get(prodi, 'XXX')

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
        
def dataSumbitSKL(prodi=None):
    file = f"./skpi/list-skpi/list-wisudawan.xlsx"
    
    dfStatus = pd.read_excel(file)
    dfExcel = dfStatus.loc[dfStatus["AJUKAN"] != '-']
    print(prodi)
    
    if prodi != None:
        excel = dfExcel.loc[dfExcel["PRODI"] == getKodeProdi(str(prodi))].values.tolist()
        return excel
    else:
        excel = dfExcel.values.tolist()
        return excel