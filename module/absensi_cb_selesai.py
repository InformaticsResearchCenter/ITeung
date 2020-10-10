from module import kelas
from module import absensi_cb_mulai

from lib import numbers

from datetime import datetime

import config

def auth(data):
    if numbers.normalize(data[0]) in config.nomor_koor_pleton_cb:
        return True
    else:
        return False

def replymsg(driver, data):
    grp=data[1]
    msg=data[3]
    try:
        materi=msg.split(' materi ')[1]
    except:
        return 'duhh materinya mana nihhh'
    absensi_from_log=kelas.getnumonly(groupname=grp, tipe='daring')
    npm_and_nama=[]
    for phone_number in absensi_from_log:
        peserta_cb_phone_number=numbers.normalize(phone_number[0])
        npm_nama=kelas.getNpmandNameMahasiswa(peserta_cb_phone_number)
        npm_and_nama.append(npm_nama)
    msgreply=f'Kode Pleton: {grp.split("-")[1]}\n' \
             f'Nama Pleton: {absensi_cb_mulai.pletonSwitcher(grp.split("-")[1])}\n' \
             f'Materi: {materi}\n' \
             f'Koordinator Pleton: {kelas.getNpmandNameMahasiswa(data[0])[1]}\n' \
             f'Tanggal dan Waktu: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}\n' \
             f'Absensi Peserta CB:\n'
    number=1
    for npm, nama in npm_and_nama:
        msgreply+=f'{number}. {npm} - {nama}\n'
        number+=1
    return msgreply