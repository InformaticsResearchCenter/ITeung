from module import kelas

from lib import numbers
from lib import message


def auth(data):
    if numbers.normalize(data[0]) == '6285155494985':
        return True
    else:
        return False


def replymsg(driver, data):
    tahun = valid_year_uda(message.normalize(data[3]).split(' '))
    if tahun:
        msgreply = 'ini yaa datanyaa...\n\n'
        for i in getData(f'{tahun}1'):
            print(i)
            msgreply += f'NPM Mahasiswa: {i["MhswID"]}\n' \
                        f'Nama Mahasiswa: {i["nama"]}\n' \
                        f'Tanggal Lahir: {i["TanggalLahir"]}\n' \
                        f'NIK KTP: {i["nik"]}\n' \
                        f'Judul: {i["Judul"]}\n' \
                        f'SKS Semester: {i["SKS_SMT"]}\n' \
                        f'IPK Transkrip: {i["IPK_Trans"]}\n' \
                        f'Prodi: {i["Nama"]}\n\n'
    else:
        msgreply = 'tahun tidak valid'
    return msgreply


def valid_year_uda(message):
    for i in message:
        if i and i.isdigit():
            i = int(i)
            if i >= 1900 and i <= 2020:
                return i


def getData(tahun):
    db = kelas.dbConnectSiap()
    sql = f"SELECT simpati.simak_mst_mahasiswa.MhswID, simpati.simak_mst_mahasiswa.nama, simpati.simak_mst_mahasiswa.TanggalLahir, simpati.simak_mst_mahasiswa.nik, simak_trn_ta.Judul, " \
          f"sum(simpati.simak_trn_transkrip.sks) as SKS_SMT, " \
          f"sum(simpati.simak_trn_transkrip.BobotNilai * simpati.simak_trn_transkrip.sks) as T_bobot," \
          f"round (sum(simpati.simak_trn_transkrip.BobotNilai * simpati.simak_trn_transkrip.sks) / sum(simpati.simak_trn_transkrip.sks),2) as IPK_Trans, " \
          f"simpati.simak_mst_mahasiswa.StatusMhswID, simak_mst_prodi.Nama, simpati.simak_mst_mahasiswa.TanggalEdit " \
          f"FROM simpati.simak_mst_mahasiswa " \
          f"inner join simak_mst_prodi on simak_mst_prodi.ProdiID=simak_mst_mahasiswa.ProdiID " \
          f"INNER JOIN simak_trn_ta ON simpati.simak_mst_mahasiswa.MhswID=simak_trn_ta.MhswID " \
          f"left join simpati.simak_trn_transkrip on simak_mst_mahasiswa.MhswID=simpati.simak_trn_transkrip.MhswID " \
          f"where simpati.simak_mst_mahasiswa.TahunID in ('{tahun}') " \
          f"group by simak_mst_mahasiswa.MhswID, simak_mst_mahasiswa.Nama, simak_mst_prodi.Nama;"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        desc = cur.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))
                for row in cur.fetchall()]
        return data