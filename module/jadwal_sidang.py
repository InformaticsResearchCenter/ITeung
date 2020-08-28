import pandas
from lib import message
from module import kelas

def auth(data):
    if kelas.getKodeDosen(data[0]) or kelas.getNpmandNameMahasiswa(data[0]):
        return True
    else:
        return False


def replymsg(driver, data):
    if kelas.getKodeDosen(data[0]):
        kode_dosen = kelas.getKodeDosen(data[0])
        dosen_homebase = getHomebaseDosen(kode_dosen)
        nama_file = f'jadwal_sidang_ta_{dosen_homebase}.xlsx'
        status, df = openJadwalExcel(nama_file)
        if status == False:
            msgreply='mohon untuk memberikan jadwal sidang dalam bentuk excel ke admin'
        else:
            if 'penguji pendamping' in message.normalize(data[3]):
                msgreply = 'ini dia jadwal sidangnya yaaa....\n\n'
                for i, j in df.iterrows():
                    if j[3] == kode_dosen:
                        msgreply += f'PENGUJI UTAMA: {kelas.getNamaDosen(j[2])}\n' \
                                    f'PENGUJI PENDAMPING: {kelas.getNamaDosen(j[3])}\n' \
                                    f'NPM MAHASISWA: {j[4]}\n' \
                                    f'NAMA MAHASISWA: {kelas.getStudentNameOnly(j[4])}\n' \
                                    f'JADWAL SIDANG: {j[5]}\n' \
                                    f'JAM SIDANG: {j[6]}\n\n'
            elif 'penguji utama' in message.normalize(data[3]):
                msgreply = 'ini dia jadwal sidangnya yaaa....\n\n'
                for i, j in df.iterrows():
                    if j[2] == kode_dosen :
                        msgreply += f'PENGUJI UTAMA: {kelas.getNamaDosen(j[2])}\n' \
                                    f'PENGUJI PENDAMPING: {kelas.getNamaDosen(j[3])}\n' \
                                    f'NPM MAHASISWA: {j[4]}\n' \
                                    f'NAMA MAHASISWA: {kelas.getStudentNameOnly(j[4])}\n' \
                                    f'JADWAL SIDANG: {j[5]}\n' \
                                    f'JAM SIDANG: {j[6]}\n\n'
            else:
                msgreply='ini dia jadwal sidangnya yaaa....\n\n'
                for i, j in df.iterrows():
                    if j[2] == kode_dosen or j[3] == kode_dosen:
                        msgreply+=f'PENGUJI UTAMA: {kelas.getNamaDosen(j[2])}\n' \
                                  f'PENGUJI PENDAMPING: {kelas.getNamaDosen(j[3])}\n' \
                                  f'NPM MAHASISWA: {j[4]}\n' \
                                  f'NAMA MAHASISWA: {kelas.getStudentNameOnly(j[4])}\n' \
                                  f'JADWAL SIDANG: {j[5]}\n' \
                                  f'JAM SIDANG: {j[6]}\n\n'
    else:
        mahasiswa_homebase=kelas.getProdiIDwithStudentID(kelas.getNpmandNameMahasiswa(data[0])[0])
        nama_file = f'jadwal_sidang_ta_{mahasiswa_homebase}.xlsx'
        status, df = openJadwalExcel(nama_file)
        if status == False:
            msgreply='mohon untuk memberikan jadwal sidang dalam bentuk excel ke admin'
        else:
            msgreply = 'ini dia jadwal sidangnya yaaa....\n\n'
            for i, j in df.iterrows():
                if str(j[4]) == str(kelas.getNpmandNameMahasiswa(data[0])[0]):
                    msgreply += f'PENGUJI UTAMA: {kelas.getNamaDosen(j[2])}\n' \
                                f'PENGUJI PENDAMPING: {kelas.getNamaDosen(j[3])}\n' \
                                f'NPM MAHASISWA: {j[4]}\n' \
                                f'NAMA MAHASISWA: {kelas.getStudentNameOnly(j[4])}\n' \
                                f'JADWAL SIDANG: {j[5]}\n' \
                                f'JAM SIDANG: {j[6]}\n\n'
    return msgreply


def getHomebaseDosen(dosenid):
    db=kelas.dbConnectSiap()
    sql=f'select Homebase from simak_mst_dosen where Login="{dosenid}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def openJadwalExcel(namaFile):
    try:
        df=True, pandas.read_excel(f'{namaFile}')
    except:
        df=False, ''
    return df