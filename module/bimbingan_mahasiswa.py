from lib import wa
from lib import reply
from lib import message

from module import kelas

from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from base64 import b64encode

import os
import config
import json

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) == None:
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    msg=data[3]
    msg=message.normalize(msg)
    try:
        tipe_bimbingan=msg.split(' bimbingan ')[1].split(' sudah dikerjakan')[0]
        studentid=kelas.getNpmandNameMahasiswa(data[0])[0]
        target_selesai = msg.split('sudah dikerjakan ')[1].split(' pekerjaan selanjutnya')[0].replace(' ', '%20')
        terget_selanjutnya = msg.split('pekerjaan selanjutnya ')[1].split(' nilai')[0].replace(' ', '%20')
        nilai=msg.split('nilai ')[1]
    except:
        return 'duh salah keyword nih bosqqqq'
    if tipeSwitcher(tipe_bimbingan):
        datenow = datetime.date(datetime.now()).strftime('%d%m%Y')
        hari = datetime.now().strftime('%A')
        hari = hariSwitcher(hari)
        data=bytes(f'{studentid}{datenow}{hari}', 'utf-8')
        passcode = encryptData(data)
        return f'Mohon untuk klik link berikut untuk konfirmasi bimbingan:\n\nhttps://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung%20input%20bimbingan%20{tipe_bimbingan}%20{studentid}%0Asudah%20dikerjakan%20{target_selesai}%0Apekerjaan%20selanjutnya%20{terget_selanjutnya}%0Anilai%20{nilai}%0Apasscode%20{passcode["ciphertext"].replace("+", "plussign")}%0Aivcode%20{passcode["iv"].replace("+", "plussign")}'
    return 'duh salah nih tipe bimbingannya coba di cek lagi yaa qaqa ehee.....'

def encryptData(data):
    key = config.key_bimbingan
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv': iv, 'ciphertext': ct})
    result_json = json.loads(result)
    return result_json

def hariSwitcher(hari):
    switcher = {
        'Monday': '1',
        'Tuesday': '2',
        'Wednesday': '3',
        'Thursday': '4',
        'Friday': '5',
        'Saturday': '6',
        'Sunday': '7',
    }
    return switcher.get(hari, 'days not found!')

def tipeSwitcher(tipe):
    switcher= {
        'p1': True,
        'p2': True,
        'p3': True,
        'i1': True,
        'i2': True,
        'ta': True,
    }
    return switcher.get(tipe, False)