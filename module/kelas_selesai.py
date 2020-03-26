from module import kelas
from lib import wa
import config

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    grp = data[1]
    num = data[0]
    messages = kelas.getAwaitingMessageKelasStart('kelas_selesai')
    messages = messages.replace('#BOTNAME#', config.bot_name)
    wa.typeMessage(driver, messages)
    coursename = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[1]
    starttimeclass = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[3]
    endtimeclass = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[4]
    msgreply=kelas.siapAbsensi(driver=driver, namagroup=grp, num=num,)
    msgreply=kelas.beritaAcara(driver=driver, num=num, coursename=coursename, starttimeclass=starttimeclass, endtimeclass=endtimeclass, groupname=grp, data=msgreply)
    return msgreply