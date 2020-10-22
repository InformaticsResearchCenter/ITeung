from lib import wa, reply, message
from module import kelas

import config
import os

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    msgreply=kelasMulai(data)
    return msgreply

def isJadwalID(kode_dosen, jadwal_id):
    db=kelas.dbConnectSiap()
    sql=f'select * from simak_trn_jadwal where DosenID="{kode_dosen}" and JadwalID = "{jadwal_id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        if cur.fetchone():
            return True
        else:
            return False

def kelasMulai(data):
    msg = data[3]
    msg = message.normalize(msg)
    if kelas.cekSiap():
        grp=data[1]
        num=data[0]
        if isJadwalID(kelas.getKodeDosen(num), grp.split('-')[0]):
            try:
                kehadiran = kelas.getKehadiran(grp.split('-')[0])
                if (kehadiran != config.kehadiran and kehadiran < config.kehadiran) or (kelas.isSudahKelas(jadwalid=grp.split('-')[0], lecturercode=kelas.getKodeDosen(num=num))):
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
                        if 'luring' in msg:
                            link = '\n\nLink Kelas Luring (offline):\n'+config.link_kelas_luring+grp.replace(' ', '%20')
                            msgreply = messages + link + listStudent
                        else:
                            msgreply = messages + listStudent
                    else:
                        listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
                        guide = 'Yahh... Nama grupnya belum JADWALID-KELAS-NAMA. yuk ubah #BOTNAME# kasih contoh 17312-A-KECERDASAN BUAT klo lupa kode mata kuliah #BOTNAME# kasih ya ini daftarnya : \n'
                        msgreply = guide+listMK
                elif kehadiran == '':
                    msgreply = 'yahhhhh kehadirannya ngga #BOTNAME# temuin coba di cek lagi jadwal idnya yaaa....'
                else:
                    jadwalid = grp.split('-')[0]
                    datamatkul = kelas.getMatakuliahInfowithJadwalID(jadwalid)
                    if datamatkul == None:
                        msgreply="mohon maaf JadwalID salah bisa untuk dicek kembali...."
                    else:
                        datamatkul = kelas.getMatakuliahInfowithJadwalID(jadwalid)
                        prodi = kelas.switcherJurusan(datamatkul[5])
                        mkkode = datamatkul[11]
                        namamatkul = datamatkul[12]
                        hari = kelas.toHari(str(datamatkul[13]))
                        jammulai = datamatkul[14]
                        jamselesai = datamatkul[15]
                        dosen = kelas.getNamaDosen(datamatkul[21])
                        rencanakehadiran = datamatkul[22]
                        kehadiran = datamatkul[23]
                        msgreply = 'Mohon maaf Untuk kuliah daring ini sudah memenuhi kuota pertemuan pada jadwal kali ini...\n\n'
                        msgreply += f"Jadwal ID: {jadwalid}\nProgram Studi: {prodi}\nKode Matakuliah: {mkkode}\nNama Matakuliah: {namamatkul}\nHari: {hari}\nJam Mulai: {jammulai}\nJam Selesai: {jamselesai}\nDosen/Kode Dosen: {dosen}/{datamatkul[21]}\nRencana Kehadiran: {rencanakehadiran}\nKehadiran: {kehadiran}"
            except Exception as e:
                print(str(e))
                listMK=kelas.getListMK(kelas.getKodeDosen(data[0]))
                guide = 'Di setting dulu ya nama groupnya jadi JADWALID-KELAS-NAMA contoh : 17312-A-KECERDASAN BUAT, ini daftarnya : \n'
                msgreply = guide+listMK
        else:
            listMK = kelas.getListMK(kelas.getKodeDosen(data[0]))
            guide = 'aduwww waduwduwwww ini bukan Jadwal ID Bapak/Ibu dosen nihhhh, yang bener yang dibawah ini yaaa.... : \n'
            msgreply = guide + listMK
    else:
        msgreply = 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....'
    return msgreply