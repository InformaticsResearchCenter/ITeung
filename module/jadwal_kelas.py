from module import kelas
import config
from lib import reply
import os
from lib import wa

def kodeHari(kode):
    switcher = {
        'senin' : '1',
        'selasa': '2',
        'rabu'  : '3',
        'kamis' : '4',
        'jumat' : '5',
        'sabtu' : '6',
        'minggu': '7',
    }
    return switcher.get(kode, "Not Found!")


def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret

def dataHari(msg):
    datahari = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu']
    msgs = msg.split(' ')
    for message in msgs:
        if message in datahari:
            hari = message
            break
        else:
            hari = ''
    return hari

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

def replymsg(driver, data):
    if kelas.cekSiap():
        wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
        wa.typeAndSendMessage(driver, wmsg)
        msg = data[3]
        msg = normalizeday(msg)
        num = data[0]
        day = dataHari(msg)
        hariId = kodeHari(day)
        msgreply = jadwalKuliah(hariId, num)
        msgreply = "Ini ya jadwal kuliah yang bapak/ibu minta \n"+msgreply
    else:
        msgreply='Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply

def jadwalKuliah(hari, num):
    kelas.dbConnect()
    db = kelas.dbConnectSiap()
    listMK = 'Kode Dosen | Jadwal ID | Mata Kuliah | Kelas | Hari | Jam Mulai | Jam Selesai | Ruangan\n '
    sql = "select DosenID, JadwalID, Nama, NamaKelas, HariID, JamMulai, JamSelesai, RuangID from simak_trn_jadwal where DosenID = '{0}' and TahunID = '".format(kelas.getKodeDosen(num)) + config.siap_tahun_id + "' and HariID = '{0}'".format(hari)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            listMK = listMK + str(row[0]) + ' | ' + str(row[1]) + ' | ' +str(row[2])+ ' | ' + kelas.toKelas(str(row[3])) + ' | ' + kelas.toHari(str(row[4])) + ' | ' + str(row[5]) + ' | ' + str(row[6]) +' | '+str(row[7])+' \n '
    return listMK