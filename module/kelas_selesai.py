from module import kelas
from lib import wa,reply,numbers
import os, config

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    if kelas.cekSiap():
        grp = data[1]
        num = data[0]
        msg = data[3]
        try:
            kehadiran = kelas.getKehadiran(grp.split('-')[0])
            if (kehadiran != config.kehadiran and kehadiran < config.kehadiran) or (kelas.isSudahKelas(jadwalid=grp.split('-')[0], lecturercode=kelas.getKodeDosen(num=num))):
                wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                wa.typeAndSendMessage(driver, wmsg)
                materi = msg.lower()
                materi = materi.split('materi')[-1]
                msgreply = kelas.siapabsensiwithsql(grp=grp, num=numbers.normalize(num), materi=materi)
                if msgreply != '':
                    if msgreply != []:
                        # msgreply=kelas.siapabsensiwithweb(driver=driver, num=num,namagroup=grp)
                        try:
                            msgreply = kelas.beritaAcara(driver=driver, num=num, groupname=grp, data=msgreply, msg=msg)
                        except:
                            msgreply = 'aduh materinya ga ada nich, \ncontoh format yang bener gini ya: \niteung kelas daring selesai materi chapter 04'
                    else:
                        msgreply = 'aduh mahasiswanya belum ada yang update nomer hp SIAP nich, \nKalo mau ke absen cocokin dulu dong nomer hp yang ada di SIAP dengan yang kamu pakai di WhatsApp \nIngat ya gunakan format international, contoh: 6282217401448 '
                else:
                    msgreply = "adohhhh wadohdoh peserta absensinya kosong nih, coba ganti ke jadwal id yang satunya lagi eheeeee.... :-3"
            elif kehadiran == '':
                msgreply = 'yahhhhh kehadirannya ngga #BOTNAME# temuin coba di cek lagi jadwal idnya yaaa....'
            else:
                msgreply = 'Mohon maaf Untuk kuliah daring ini sudah memenuhi kuota pertemuan pada jadwal kali ini...'
        except:
            listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
            guide = 'yahh....nama groupnya jangan diubah dong. hihihi ganti lagi ya.jadi JADWALID-KELAS-NAMAMK,contoh : 17312-A-KECERDASAN BUATAN : \n'
            msgreply = guide+listMK
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply