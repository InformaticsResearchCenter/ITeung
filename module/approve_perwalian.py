from module import kelas
from module import cek_tanda_tangan_bap
from module import approve_bap

import config

def auth(data):
    if cek_tanda_tangan_bap.isKaprodi(cek_tanda_tangan_bap.getNIPYfromHandphone(data[0])) or cek_tanda_tangan_bap.isDeputiAkademik(cek_tanda_tangan_bap.getNIPYfromHandphone(data[0])):
        return True
    else:
        return False

def replymsg(driver, data):
    kode_dosen=cekKodeDosen(data[3])
    if kode_dosen:
        status=approve_bap.cekStatus(data[0])
        update_field=updateField(status)
        if status == 'kaprodi':
            if cekKaprodiAndDosenProdiID(kelas.getKodeDosen(data[0]), kode_dosen):
                updateApproval(
                    kode_dosen,
                    getProdiIDfromDosenID(kode_dosen),
                    update_field
                )
                return f'sudah diapprove dengan kode koden {kode_dosen}'
            else:
                return 'eeehhhh kamu mau approve kode dosen dari prodi lain yaaa hihihiih....., harus sama atuh prodinya....'
        else:
            updateApproval(
                kode_dosen,
                getProdiIDfromDosenID(kode_dosen),
                update_field
            )
            return f'sudah diapprove dengan kode koden {kode_dosen}'
    else:
         return f'yahh kode dosennya mana nihhh, {config.bot_name} perlu kode dosennya nihhh....'

def updateField(status):
    if status == 'kaprodi':
        return 'ApproveKaprodi'
    else:
        return 'ApproveDeputi'

def cekKodeDosen(msg):
    msgs=msg.split(' ')
    for i in msgs:
        if kelas.getEmailDosen(i):
            return i
    return False

def getProdiIDfromDosenID(dosen_id):
    db=kelas.dbConnectSiap()
    sql=f'select Homebase from simak_mst_dosen where Login="{dosen_id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return row[0]
        return None

def cekKaprodiAndDosenProdiID(kaprodi_kode_dosen, dosen_kode_dosen):
    prodiid_dosen=getProdiIDfromDosenID(dosen_kode_dosen)
    prodiid_kaprodi=getProdiIDfromDosenID(kaprodi_kode_dosen)
    if prodiid_dosen == prodiid_kaprodi:
        return True
    else:
        return False

def updateApproval(kode_dosen, prodi_id, field_update, tahun_id=kelas.getTahunID()):
    db=kelas.dbConnect()
    sql=f"UPDATE `wanda`.`perwalian_log` SET `{field_update}` = 'true' WHERE `KodeDosen` = '{kode_dosen}' and `ProdiID` = {prodi_id} and `TahunID` = {tahun_id}"
    with db:
        cur=db.cursor()
        cur.execute(sql)
