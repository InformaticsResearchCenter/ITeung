from module import kelas
from lib import reply
import pymysql, config

def auth(data):
    groupid = reply.getNumberGroup(data[0]).split('-')
    if '4' in groupid:
        ret = True
    else:
        ret = False
    return ret

def replymsg(driver, data):
    insertData(getDataMahasiswaAktif())
    msgreply='okeee sudah masukkkk choyyyyyy'
    return msgreply

def dbConnectVA():
    db = pymysql.connect(config.db_host_va, config.db_username_va, config.db_password_va, config.db_name_va)
    return db

def getDataMahasiswaAktif():
    db=kelas.dbConnectSiap()
    sql="select MhswID, Nama, EmailOrtu, HandphoneOrtu, ProdiID from simak_mst_mahasiswa where StatusMhswID='A' AND MhswID between 1133001 and 6194500"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        return rows

def insertData(datamahasiswa):
    MAHASISWAAKTIF=datamahasiswa
    for i in MAHASISWAAKTIF:
        npm=i[0]
        nama=i[1]
        prodiid=i[4]
        angkatan=angkatanSwitcher(npm[1:3])
        if i[2] == None or i[2] == '' or i[2] == ' ' or i[2] == 'NULL':
            email='NULL'
        else:
            email=i[2]
        if i[3] == None or i[3] == '' or i[3] == ' ' or i[3] == 'NULL':
            hp='NULL'
        else:
            hp=i[3]
        try:
            setData(npm, nama, email, hp, prodiid, switcherJurusan(prodiid), angkatan)
        except:
            print('data sudah ada')

def setData(npm, nama, email, handphone, prodiid, namaprodi, angkatan):
    db=dbConnectVA()
    sql='INSERT INTO `db_ypbpi`.`VAMAHASISWA`(`MhswID`, `Nama`, `EmailOrtu`, `HandphoneOrtu`, `ProdiID`, `NamaProdi`, `Angkatan`) VALUES ("{npm}", "{nama}", "{email}", "{handphone}", "{prodiid}", "{namaprodi}", "{angkatan}")'.format(
        npm=npm,
        nama=nama,
        email=email,
        handphone=handphone,
        prodiid=prodiid,
        namaprodi=namaprodi,
        angkatan=angkatan
    )
    with db:
        cur=db.cursor()
        cur.execute(sql)

def angkatanSwitcher(npm):
    switcher = {
        '10': '2010',
        '11': '2011',
        '12': '2012',
        '13': '2013',
        '14': '2014',
        '15': '2015',
        '16': '2016',
        '17': '2017',
        '18': '2018',
        '19': '2019',
        '20': '2020',
    }
    return switcher.get(npm, 'notfound')

def switcherJurusan(kode):
    switcher = {
        '13': 'D3 Teknik Informatika',
        '14': 'D4 Teknik Informatika',
        '23': 'D3 Manajemen Informatika',
        '33': 'D3 Akuntansi',
        '34': 'D4 Akuntansi',
        '43': 'D3 Manajemen Bisnis',
        '44': 'D4 Manajemen Bisnis',
        '53': 'D3 Logistik Bisnis',
        '54': 'D4 Logistik Bisnis',
    }
    return switcher.get(kode, "Not Found!")