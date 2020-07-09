from lib import wa, reply
from module import kelas
from Crypto.Cipher import AES
import os, config, calendar

def auth(data):
    # if kelas.getKodeDosen(data[0]) == '':
    #     ret=False
    # else:
    #     ret=True
    return True

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace("#BOTNAME#", config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    msg=data[3]
    passcode=msg.split(' ')[-1]
    try:
        obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode("utf8"))
        dec = bytes.fromhex(passcode)
        resultpasscode, status = obj.decrypt(dec).decode('utf-8'), True
    except:
        resultpasscode, status = '', False
    if status:
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
    else:
        msgreply=f'waduh akang/teteh kayaknya #BOTNAME# ga bisa mengenali passcode yang {passcode} deh, coba di periksa lagi yaa, dan jangan diubah passcodenya'
    return msgreply