from module import approve_kambing, kelas
from lib import numbers


def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    num=numbers.normalize(data[0])
    kodedosen=kelas.getKodeDosen(num)
    sudah, siap, belum = approve_kambing.bimbinganCekApprovalBimbingan(kodedosen)
    msgreply='ini datanya....'
    msgreply += f"\n\nSudah ditandatangani:\n*NPM* | *Nama*"
    for i in sudah:
        msgreply+=f'\n*{i}* | *{kelas.getStudentNameOnly(i)}*'
    msgreply += f"\n\nSiap ditandatangani:\n*NPM* | *Nama*"
    for i in siap:
        msgreply += f'\n*{i}* | *{kelas.getStudentNameOnly(i)}*'
    msgreply += f"\n\nBelum siap ditandatangani:\n*NPM* | *Nama*"
    for i in belum:
        msgreply += f'\n*{i}* | *{kelas.getStudentNameOnly(i)}*'
    return msgreply