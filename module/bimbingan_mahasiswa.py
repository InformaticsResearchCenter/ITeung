from lib import wa, reply, message
from module import kelas
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
    tipe_bimbingan=msg.split('bimbingan ')[1].split(' topik')[0]
    studentid=kelas.getNpmandNameMahasiswa(data[0])[0]
    topik=msg.split('topik ')[1].split(' nilai')[0].replace(' ', '%20')
    # pertemuan=msg.split('pertemuan ')[1].split(' nilai')[0]
    nilai=msg.split('nilai ')[1]
    msgreply='https://api.whatsapp.com/send?phone={nomoriteung}&text=iteung%20input%20bimbingan%20{tipebimbingan}%20{npm}%0Atopik%20{topikbimbingan}%0Anilai%20{nilai}'.format(
        nomoriteung=config.nomor_iteung,
        tipebimbingan=tipe_bimbingan,
        npm=studentid,
        topikbimbingan=topik,
        nilai=nilai
    )
    return msgreply