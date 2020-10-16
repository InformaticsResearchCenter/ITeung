from module import kelas

from lib import sql_to_dictionary

def auth(data):
    if kelas.getKodeDosen(data[0]):
        return True
    else:
        return False

def replymsg(driver, data):
    kode_dosen=kelas.getKodeDosen(data[0])
    tahun_angkatan=f'{data[1].split("-")[3]}1'
    msgreply=f'haiyooooo mari mari kita laksanakan perwalian bersama Bapak/Ibu dosen kita tercintaaa....\nBerikut ITeung berikan untuk peserta absensi Perwaliannya yaaa:\n\n'
    nomor_urut=1
    for data in getPesertaPerwalian(kode_dosen, tahun_angkatan):
        msgreply+=f'{nomor_urut}. *{data["MhswID"]}* - *{data["Nama"]}*\n'
        nomor_urut+=1
    return msgreply

def getPesertaPerwalian(kode_dosen, tahun_angkatan):
    db=kelas.dbConnectSiap()
    sql=f'select * from simak_mst_mahasiswa where PenasehatAkademik="{kode_dosen}" and TahunID={tahun_angkatan}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        datas=cur.fetchall()
        return sql_to_dictionary.fetchAllMode(datas, cur)
