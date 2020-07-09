from lib import wa, reply, message, numbers
from module import kelas, bimbingan_mahasiswa
from datetime import datetime, timedelta
from Crypto.Cipher import AES
import os, config, calendar

def auth(data):
    # if kelas.getKodeDosen(data[0]) == '':
    #     ret=False
    # else:
    #     ret=True
    return True

def replymsg(driver, data):
    # msg=data[3]
    msg='iteung tanda tangan 54fa6462007f2cec8d422cdf512ea6d7'
    passcode=msg.split(' ')[-1]
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode("utf8"))
    dec = bytes.fromhex(passcode)
    resultpasscode = obj.decrypt(dec).decode('utf-8')
    kodedosen = resultpasscode.split(';')[0]
    tglterbit = resultpasscode.split(';')[1][:-1]
    datadosen=kelas.getAllDataDosens(kodedosen)
    penerbitantandatangan = tglterbit[0:2] + ' ' + calendar.month_name[int(tglterbit[2:4])] + ' ' + tglterbit[4:]
    namadosen=kelas.getNamaDosen(kodedosen)
    datalahirdosen=datadosen[7].strftime('%d-%m-%Y')
    tahunlahirdosen=datalahirdosen.split('-')[2]
    bulanlahirdosen=calendar.month_name[int(datalahirdosen.split('-')[1])]
    tanggallahirdosen=datalahirdosen.split('-')[0]
    datalahirdosen=tanggallahirdosen+' '+bulanlahirdosen+' '+tahunlahirdosen
    msgreply=f'Ini yaaa data yang Akang/Teteh minta\n\nKode Dosen: {kodedosen}\nNama Dosen: {namadosen}\nNIDN: {datadosen[2]}\nTempat/Tgl Lahir: {datadosen[6]}/{datalahirdosen}\nHandphone: {datadosen[12]}\nE-mail: {datadosen[13]}\n\nPenerbitan Tanda Tangan: {penerbitantandatangan}'
    return msgreply