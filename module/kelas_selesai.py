from module import kelas, kelas_mulai
from lib import wa, reply, numbers, message
import os, config

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    msgreply=kelasSelesai(driver,  data)
    return msgreply

def kelasSelesai(driver, data):
    if kelas.cekSiap():
        grp = data[1]
        num = data[0]
        if kelas_mulai.isJadwalID(kelas.getKodeDosen(num), grp.split('-')[0]):
            msg = data[3]
            msg = message.normalize(msg)
            if 'luring' in msg:
                tipe = 'luring'
            else:
                tipe = 'daring'
            try:
                kehadiran = kelas.getKehadiran(grp.split('-')[0])
                rencana_kehadiran = kelas.rencana_kehadiran(grp.split('-')[0])
                if (kehadiran != rencana_kehadiran and kehadiran < rencana_kehadiran) or (kelas.isSudahKelas(jadwalid=grp.split('-')[0], lecturercode=kelas.getKodeDosen(num=num))):
                    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                    wa.typeAndSendMessage(driver, wmsg)
                    materi = msg.lower()
                    try:
                        materi = materi.split(' materi ')[1]
                    except:
                        return f'yahhh materinya ngga ada nih tambahin dong materinyaaa.....,\ncontoh: iteung kelas daring selesai materi chapter 1'
                    msgreply = kelas.siapabsensiwithsql(grp=grp, num=numbers.normalize(num), materi=materi, tipe=tipe)
                    if msgreply != '':
                        if msgreply != []:
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
            listMK = kelas.getListMK(kelas.getKodeDosen(data[0]))
            guide = 'aduwww waduwduwwww ini bukan Jadwal ID Bapak/Ibu dosen nihhhh, yang bener yang dibawah ini yaaa.... : \n'
            msgreply = guide + listMK
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply