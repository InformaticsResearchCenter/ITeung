from module import kelas, bimbingan_dosen
from lib import reply, wa
import os
def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    startdate=bimbingan_dosen.getStartDate(data[0])
    pertemuan=bimbingan_dosen.countPertemuan(startdate)
    msgreply='ini yaa info pertemuannya:\n\nJadwal Mulai Pertemuan: {startdate}\nPertemuan: {pertemuanke}'.format(startdate=startdate, pertemuanke=pertemuan)
    return msgreply