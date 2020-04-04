from module import kelas
from lib import wa,reply,numbers
import os

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    grp = data[1]
    num = data[0]
    msg = data[3]
    try:
        coursename = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), kelas.getKodeDosen(num))[1]
        starttimeclass = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), kelas.getKodeDosen(num))[3]
        endtimeclass = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), kelas.getKodeDosen(num))[4]
        wmsg=reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        wa.typeAndSendMessage(driver,wmsg)
        msgreply=kelas.siapabsensiwithsql(grp=grp, num=numbers.normalize(num))
        # msgreply=kelas.siapabsensiwithweb(driver=driver, num=num,namagroup=grp)
        msgreply=kelas.beritaAcara(driver=driver, num=num, coursename=coursename, starttimeclass=starttimeclass, endtimeclass=endtimeclass, groupname=grp, data=msgreply, msg=msg)
    except:
        listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
        guide = 'yahh....nama groupnya jangan diubah dong. hihihi ganti lagi ya.jadi KodeMK-KELAS-NAMAMK,contoh : TI3466-A-KECERDASAN BUATAN : \n'
        msgreply = guide+listMK
    return msgreply