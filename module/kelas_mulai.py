from lib import wa
from module import kelas

import config

#close commit #2
def replymsg(driver, data):
    grp = data[1]
    num = data[0]
    if kelas.sudahinput(wa.getGroupName(driver)) == True:
        msgreply = "mohon maaf matakuliah ini tidak bisa dimulai, mohon menunggu hingga minggu depan... terima kasih"
    else:
        if kelas.isMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num):
            coursename = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[1]
            messages = kelas.getAwaitingMessageKelasStart('kelas')
            messages = messages.replace('#MATKUL#', coursename)
            messages = messages.replace('#BOTNAME#', config.bot_name)
            msgreply = messages
        else:
            msgreply = 'mohon maaf kode dosen bapak/ibu dengan kode matkul yang berada digroup ini tidak ditemukan, mohon untuk cek kembali, terima kasih :-)'
    return msgreply