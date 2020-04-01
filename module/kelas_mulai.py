from lib import wa
from module import kelas

import config



def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret
    
#close commit #2
def replymsg(driver, data):
    grp = data[1]
    num = data[0]
    if kelas.sudahinput(wa.getGroupName(driver)) == True:
        msgreply = "yuhuuuu..... semangat banget sih, kan minggu ini udah kuliah. tunggu minggu depan ya... terima kasih"
    else:
        try:
            if kelas.isMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num):
                mkkode = grp.split('-')[0]
                kodekelas = kelas.kodeKelas(grp.split('-')[1])
                JadwalID = kelas.getJadwalId(kelas=kodekelas, mkkode=mkkode)
                abc = 1
                listStudent='\n\nBerikut Peserta Absensinya:\n'
                for i in kelas.pesertaAbsensi(JadwalID):
                    npm=i[-1]
                    nama=kelas.getStudentNameOnly(npm)
                    listStudent=listStudent+str(abc)+'. '+npm+' '+nama+'\n'
                    abc+=1
                coursename = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), kelas.getKodeDosen(num))[1]
                messages = kelas.getAwaitingMessageKelasStart('kelas_mulai')
                messages = messages.replace('#MATKUL#', coursename)
                messages = messages.replace('#BOTNAME#', config.bot_name)
                msgreply = messages + listStudent
            else:
                listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
                guide = 'Yahh... Nama grupnya belum KODEMK-KELAS-NAMA. yuk ubah #BOTNAME# kasih contoh TI3466-A-KECERDASAN BUAT klo lupa kode mata kuliah #BOTNAME# kasih ya ini daftarnya : \n'
                msgreply = guide+listMK
        except:
            listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
            guide = 'Di setting dulu ya nama groupnya jadi KODEMK-KELAS-NAMA contoh : TI3466-A-KECERDASAN BUAT, ini daftarnya : \n'
            msgreply = guide+listMK
    return msgreply