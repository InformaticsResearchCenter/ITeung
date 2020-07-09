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
        tglttd = resultpasscode.split(';')[1]
        blnttd = resultpasscode.split(';')[2]
        thnttd = resultpasscode.split(';')[3]
        jamttd = resultpasscode.split(';')[4]
        mntttd = resultpasscode.split(';')[5]
        dtkttd = resultpasscode.split(';')[6]
        datadosen=kelas.getAllDataDosens(kodedosen)
        penerbitantandatangan = f'{jamttd}:{mntttd}:{dtkttd} {tglttd} {calendar.month_name[int(blnttd)]} {thnttd}'
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