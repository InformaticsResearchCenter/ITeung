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
    kelas_number=f'{kelas.kodeKelas(data[1].split("-")[2])}'
    for data in getPesertaPerwalian(kode_dosen, tahun_angkatan, kelas_number):
        msgreply+=f'{nomor_urut}. *{data["MhswID"]}* - *{data["Nama"]}*\n'
        nomor_urut+=1
    return msgreply

def getPesertaPerwalian(kode_dosen, tahun_angkatan, kelas_number):
    db=kelas.dbConnectSiap()
    sql=f'select mst.MhswID,mst.Nama,mst.PenasehatAkademik,mst.TahunID,krs.Kelas ' \
        f'from ' \
        f'simak_mst_mahasiswa as mst ' \
        f'join ' \
        f'simak_trn_krs as krs ' \
        f'where mst.MhswID=krs.MhswID ' \
        f'and ' \
        f'mst.TahunID={tahun_angkatan} ' \
        f'and ' \
        f'krs.kelas="{kelas_number}" ' \
        f'and ' \
        f'mst.PenasehatAkademik="{kode_dosen}" ' \
        f'and ' \
        f'mst.StatusMhswID = "A" ' \
        f'group by ' \
        f'mst.MhswID;'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        datas=cur.fetchall()
        return sql_to_dictionary.fetchAllMode(datas, cur)
