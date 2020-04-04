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
        wmsg=reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        wa.typeAndSendMessage(driver,wmsg)
        msgreply=kelas.siapabsensiwithsql(grp=grp, num=numbers.normalize(num))
        # msgreply=kelas.siapabsensiwithweb(driver=driver, num=num,namagroup=grp)
        try:
            msgreply=kelas.beritaAcara(driver=driver, num=num, groupname=grp, data=msgreply, msg=msg)
        except:
            msgreply='aduh materinya ga ada nich, contoh format yang bener gini ya: iteung kelas daring selesai materi chapter 04'
    except:
        listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
        guide = 'yahh....nama groupnya jangan diubah dong. hihihi ganti lagi ya.jadi JADWALID-KELAS-NAMAMK,contoh : 17312-A-KECERDASAN BUATAN : \n'
        msgreply = guide+listMK
    return msgreply