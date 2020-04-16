from lib import wa, reply
from module import kelas

import config
import os



def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret
    
#close commit #2
def replymsg(driver, data):
    if kelas.cekSiap():
        grp = data[1]
        try:
            kehadiran = kelas.getKehadiran(grp.split('-')[0])
            if kehadiran != config.kehadiran and kehadiran < config.kehadiran:
                if kelas.isMatkul(grp.split('-')[0]):
                    jadwalid = grp.split('-')[0]
                    jadwalserial = kelas.getJadwalSerial(jadwalid=jadwalid)
                    if jadwalserial == '0':
                        jadwalid = jadwalid
                    else:
                        jadwalid = jadwalserial
                    abc = 1
                    listStudent='\n\nBerikut Peserta Absensinya:\n'
                    for i in kelas.pesertaAbsensi(jadwalid=jadwalid):
                        npm=i[-1]
                        nama=kelas.getStudentNameOnly(npm)
                        listStudent=listStudent+str(abc)+'. '+npm+' '+nama+'\n'
                        abc+=1
                    coursename = kelas.getDataMatkul(grp.split('-')[0])[1]
                    messages = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                    messages = messages.replace('#MATKUL#', coursename)
                    messages = messages.replace('#BOTNAME#', config.bot_name)
                    msgreply = messages + listStudent
                else:
                    listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
                    guide = 'Yahh... Nama grupnya belum JADWALID-KELAS-NAMA. yuk ubah #BOTNAME# kasih contoh 17312-A-KECERDASAN BUAT klo lupa kode mata kuliah #BOTNAME# kasih ya ini daftarnya : \n'
                    msgreply = guide+listMK
            elif kehadiran == '':
                msgreply = 'yahhhhh kehadirannya ngga #BOTNAME# temuin coba di cek lagi jadwal idnya yaaa....'
            else:
                msgreply = 'Mohon maaf Untuk kuliah daring ini sudah memenuhi kuota pertemuan pada jadwal kali ini...'
        except:
            listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
            guide = 'Di setting dulu ya nama groupnya jadi JADWALID-KELAS-NAMA contoh : 17312-A-KECERDASAN BUAT, ini daftarnya : \n'
            msgreply = guide+listMK
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply