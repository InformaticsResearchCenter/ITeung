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
        msgreply = "mohon maaf matakuliah ini tidak bisa dimulai, mohon menunggu hingga minggu depan... terima kasih"
    else:
        try:
            if kelas.isMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num):
                coursename = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[1]
                messages = kelas.getAwaitingMessageKelasStart('kelas_mulai')
                messages = messages.replace('#MATKUL#', coursename)
                messages = messages.replace('#BOTNAME#', config.bot_name)
                msgreply = messages
            else:
                listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
                guide = 'Yahh... kayaknya kode mata kuliah atau kelasnya masih salah deh coba cek yahh : \n'
                msgreply = guide+listMK
        except:
            listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
            guide = 'Di setting dulu ya nama groupnya jadi KODEMK-KELAS-NAMA contoh : TI3466-A-KECERDASAN BUAT, ini daftarnya : \n'
            msgreply = guide+listMK
    return msgreply