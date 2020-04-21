import config
import pymysql
from module import kelas
from lib import reply
import os
from lib import wa
from datetime import datetime

def normalizeday(msg):
    msg = msg.lower()
    msg = msg.replace(',', ' ')
    msg = msg.replace('.', ' ')
    msg = msg.replace("'", '')
    msg = msg.replace('?', ' ')
    msg = msg.replace('!', ' ')
    msg = msg.replace('(', ' ')
    msg = msg.replace(')', ' ')
    msg = msg.replace(':', ' ')
    msg = msg.replace(';', ' ')
    msg = msg.replace('*', ' ')
    msg = msg.replace('&', ' ')
    msg = msg.replace('^', ' ')
    msg = msg.replace('%', ' ')
    msg = msg.replace('/', ' ')
    msg = msg.replace('[', ' ')
    msg = msg.replace(']', ' ')
    msg = msg.replace(config.bot_shortname, config.bot_name)
    msg = msg.strip()
    return msg

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    if kelas.cekSiap():
        wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
        wa.typeAndSendMessage(driver, wmsg)
        num = data[0]
        msgreply = getJadwalData(num)
        msgreply = "Ini jadwal ujian yang Bapak/Ibu minta\n"+msgreply
    else:
        msgreply='Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply

def getJadwalData(nohp):
    kelas.dbConnect()
    db = kelas.dbConnectSiap()

    sql = """
        select j.Nama, CASE
        WHEN j.ProdiID ='.13.' THEN 'D3 Teknik Informatika'
        WHEN j.ProdiID ='.14.' THEN 'D4 Teknik Informatika'
        WHEN j.ProdiID ='.23.' THEN 'D3 Manajemen Informatika'
        WHEN j.ProdiID ='.33.' THEN 'D3 Akuntansi'
        WHEN j.ProdiID ='.34.' THEN 'D4 Akuntansi Keuangan'
        WHEN j.ProdiID ='.43.' THEN 'D3 Manajemen Pemasaran'
        WHEN j.ProdiID ='.44.' THEN 'D4 Manajemen Perusahaan'
        WHEN j.ProdiID ='.53.' THEN 'D3 Logistik Bisnis'
        WHEN j.ProdiID ='.54.' THEN 'D4 Logistik Bisnis'
        END AS namaprodi, CASE
        WHEN j.NamaKelas =1 THEN 'A'
        WHEN j.NamaKelas =2 THEN 'B'
        WHEN j.NamaKelas =3 THEN 'C'
        WHEN j.NamaKelas =4 THEN 'D'
        WHEN j.NamaKelas =5 THEN 'E'
        WHEN j.NamaKelas =6 THEN 'F'
        WHEN j.NamaKelas =7 THEN 'G'
        WHEN j.NamaKelas =8 THEN 'H'
        WHEN j.NamaKelas =9 THEN 'I'
        END AS namakelas, j.JumlahMhsw, date_format(j.UTSTanggal,'%d-%m-%Y') as Tanggal, 
        time_format(j.UTSJamMulai,'%H:%i') as JamMulai, 
        time_format(j.UTSJamSelesai,'%H:%i') as JamSelesai,  r.Nama as Ruang, j.JadwalID
        from simak_trn_jadwal j, simak_mst_ruangan r, simak_mst_dosen d, 
        simak_mst_matakuliah m,  simak_mst_tahun t, simak_mst_prodi pr
        where j.MKID=m.MKID and j.DosenID=d.Login and j.DosenID='"""+kelas.getKodeDosen(nohp)+"""' 
        and j.TahunID='"""+config.siap_tahun_id+"""' and t.ProgramID='"""+config.jalur_program+"""' 
        and m.ProdiID = pr.ProdiID and j.RuangID=r.RuangID group by j.JadwalID;
    """
    jadwal = ''
    jadwalToday = '*Jadwal Ujian Hari Ini*'.upper() + \
        '\nTanggal | Mata Kuliah | Prodi | Kelas | Jumlah | Jam Ujian | Ruangan\n'
    jadwalPrevDay = '*Jadwal Ujian Yang Telah Dilaksanakan*'.upper() + \
        '\nTanggal | Mata Kuliah | Prodi | Kelas | Jumlah | Jam Ujian | Ruangan\n'
    jadwalNextDay = '*Jadwal Ujian Yang Akan Datang*'.upper() + \
        '\nTanggal | Mata Kuliah | Prodi | Kelas | Jumlah | Jam Ujian | Ruangan\n'

    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        for row in rows:
            if row[3] != 0:
                date = datetime.strptime(row[4], '%d-%m-%Y').date()
                today = datetime.today().date()
                if date == today:
                    jadwalToday += '*%s* | %s | %s | %s | %s | %s | %s \n' % (
                        row[4], row[0].title(), row[1], row[2], row[3], row[5]+'-'+row[6], row[7])
                elif date > today:
                    jadwalNextDay += '*%s* | %s | %s | %s | %s | %s | %s \n' % (
                        row[4], row[0].title(), row[1], row[2], row[3], row[5]+'-'+row[6], row[7])
                elif date < today:
                    jadwalPrevDay += '*%s* | %s | %s | %s | %s | %s | %s \n' % (
                        row[4], row[0].title(), row[1], row[2], row[3], row[5]+'-'+row[6], row[7])

        if len(jadwalToday) == 93:
            jadwalToday += '_Tidak ada jadwal ujian hari ini_'
        if len(jadwalPrevDay) == 108:
            jadwalPrevDay += '_Tidak ada jadwal ujian yang telah dilaksanakan_'
        if len(jadwalNextDay) == 101:
            jadwalNextDay += '_Tidak ada jadwal ujian yang akan datang_'

    return jadwal + jadwalToday+'\n\n' + jadwalNextDay+'\n' + jadwalPrevDay
