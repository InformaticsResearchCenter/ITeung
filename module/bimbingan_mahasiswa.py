from lib import wa, reply, message
from module import kelas
from Crypto.Cipher import AES
from datetime import datetime
import os, config

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
    successsplit=''
    try:
        tipe_bimbingan=msg.split('bimbingan ')[1].split(' target selesai')[0]
        studentid=kelas.getNpmandNameMahasiswa(data[0])[0]
        # topik=msg.split('topik ')[1].split(' nilai')[0].replace(' ', '%20')
        # pertemuan=msg.split('pertemuan ')[1].split(' nilai')[0]
        target_selesai = msg.split('sudah dikerjakan ')[1].split(' pekerjaan selanjutnya')[0].replace(' ', '%20')
        terget_selanjutnya = msg.split('pekerjaan selanjutnya ')[1].split(' nilai')[0].replace(' ', '%20')
        nilai=msg.split('nilai ')[1]
    except:
        successsplit='error'
    if successsplit == 'error':
        msgreply='wahh salah keyword bosqqq'
    else:
        if tipeSwitcher(tipe_bimbingan) == True:
            datenow = datetime.date(datetime.now()).strftime('%d%m%Y')
            hari = datetime.now().strftime('%A')
            hari = hariSwitcher(hari)
            obj = AES.new(config.key, AES.MODE_CBC, config.iv)
            cp = obj.encrypt(studentid+datenow+hari)
            passcode=cp.hex()
            msgreply='https://api.whatsapp.com/send?phone={nomoriteung}&text=iteung%20input%20bimbingan%20{tipebimbingan}%20{npm}%0Asudah%20dikerjakan%20{targetselesai}%0Apekerjaan%20selanjutnya%20{targetselanjutnya}%0Anilai%20{nilai}%0Apasscode%20{passcode}'.format(
                nomoriteung=config.nomor_iteung,
                tipebimbingan=tipe_bimbingan,
                npm=studentid,
                nilai=nilai,
                passcode=passcode,
                targetselesai=target_selesai,
                targetselanjutnya=terget_selanjutnya
            )
        else:
            msgreply='tuh salah nih tipe bimbingannya coba di cek lagi yaa qaqa ehee.....'
    return msgreply

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