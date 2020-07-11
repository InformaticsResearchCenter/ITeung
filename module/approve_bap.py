from module import cek_tanda_tangan_bap, kelas
from lib import numbers, wa, reply

import os, config

def auth(data):
    if cek_tanda_tangan_bap.isKaprodi(cek_tanda_tangan_bap.getNIPYfromHandphone(data[0])) or cek_tanda_tangan_bap.isDeputiAkademik(cek_tanda_tangan_bap.getNIPYfromHandphone(data[0])):
        return True
    else:
        return False

def cekStatus(num):
    if cek_tanda_tangan_bap.isKaprodi(cek_tanda_tangan_bap.getNIPYfromHandphone(num)):
        return 'kaprodi'
    else:
        return 'deputi'


def updateField(status):
    if status == 'kaprodi':
        return 'BKD_Prodi'
    else:
        return 'BKD_Deputi'


def cekProdiIDKaproditoJadwalID(prodiid, jadwalid):
    db=kelas.dbConnectSiap()
    sql=f'select * from simak_trn_jadwal where JadwalID={jadwalid} and ProdiID="{prodiid}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return True
        else:
            return False


def getKaprodiProdiID(num):
    db=kelas.dbConnectSiap()
    sql=f'select ProdiID from simak_mst_dosen where Handphone="{num}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def confirmBKD(jadwalid, updatefield):
    db=kelas.dbConnectSiap()
    sql=f"UPDATE `simpati`.`simak_trn_jadwal` SET `{updatefield}` = 'true' WHERE `JadwalID` = {jadwalid}"
    with db:
        cur=db.cursor()
        cur.execute(sql)


def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    num=numbers.normalize(data[0])
    jadwalid=data[3].split(' ')[-1]
    status=cekStatus(num)
    updatefield=updateField(status)
    if status == 'kaprodi':
        kaprodiprodiid=getKaprodiProdiID(num)
        if jadwalid == 'all':
            statusbap=cek_tanda_tangan_bap.infoBAPKaprodi(kaprodiprodiid)[1]
            if len(statusbap) > 0:
                for bapjadwalid in statusbap:
                    confirmBKD(bapjadwalid, updatefield)
                msgreply=f'okee sudah berhasil #BOTNAME# approve semua datanya yaaa ini data yang berhasil #BOTNAME# approve\n\n*Jadwal ID* :\n'
                for i in statusbap:
                    msgreply+=f'{i}\n'
            else:
                msgreply='aduh wadidiw, ga ada nih berkas yang bisa di approve hihihihi'
        else:
            if cekProdiIDKaproditoJadwalID(kaprodiprodiid, jadwalid):
                if cek_tanda_tangan_bap.cekMateriPerkuliahan(jadwalid):
                    confirmBKD(jadwalid, updatefield)
                    msgreply = f'okee sudah berhasil #BOTNAME# set approvalnya untuk JadwalID *{jadwalid}* yaa...'
                else:
                    msgreply = f'waduh mohon maaf sepertinya belum bisa approve JadwalID yang {jadwalid} deh soalnya materinya belum lengkap atau masih ada yang kosong'
            else:
                msgreply = f'hayooo Bapak/Ibu dari prodi mana hayooo kok mau set JadwalID yang lain hayoooo'
    else:
        if jadwalid == 'all':
            statusbap = cek_tanda_tangan_bap.infoBAPDeputi()[1]
            if len(statusbap) > 0:
                for bapjadwalid in statusbap:
                    confirmBKD(bapjadwalid, updatefield)
                msgreply = f'okee sudah berhasil #BOTNAME# approve semua datanya yaaa ini data yang berhasil #BOTNAME# approve\n\n*Jadwal ID* :\n'
                for i in statusbap:
                    msgreply += f'{i}\n'
            else:
                msgreply='yahhhh sayang sekali belum ada berkas yang siap untuk di approve nichhhhh'
        else:
            if cek_tanda_tangan_bap.cekMateriPerkuliahan(jadwalid):
                confirmBKD(jadwalid, updatefield)
                msgreply = f'okee sudah berhasil #BOTNAME# set approvalnya untuk JadwalID *{jadwalid}* yaa...'
            else:
                msgreply = f'waduh mohon maaf sepertinya belum bisa approce JadwalID yang {jadwalid} deh soalnya materinya belum lengkap atau masih ada yang kosong'
    return msgreply