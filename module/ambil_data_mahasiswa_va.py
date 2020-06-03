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
    sql="select MhswID, Nama, EmailOrtu, HandphoneOrtu from simak_mst_mahasiswa where StatusMhswID='A' AND MhswID between 1133001 and 6194500"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        return rows

def insertData(datamahasiswa):
    MAHASISWAAKTIF=datamahasiswa()
    for i in MAHASISWAAKTIF:
        npm=i[0]
        nama=i[1]
        if i[2] == None or i[2] == '' or i[2] == ' ' or i[2] == 'NULL':
            email='NULL'
        else:
            email=i[2]
        if i[3] == None or i[3] == '' or i[3] == ' ' or i[3] == 'NULL':
            hp='NULL'
        else:
            hp=i[3]
        try:
            setData(npm, nama, email, hp)
        except:
            print('data sudah ada')

def setData(npm, nama, email, handphone):
    db=dbConnectVA()
    sql="INSERT INTO `db_ypbpi`.`VAMAHASISWA`(`MhswID`, `Nama`, `EmailOrtu`, `HandphoneOrtu`) VALUES ('{npm}', '{nama}', '{email}', '{handphone}')".format(
        npm=npm,
        nama=nama,
        email=email,
        handphone=handphone
    )
    with db:
        cur=db.cursor()
        cur.execute(sql)