from module import kelas
from lib import wa, reply, message, numbers
import os, config

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) != None :
        ret = True
    else:
        ret = False
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    msg = data[3].lower()
    num = numbers.normalize(data[0])
    tahun_id = '20192'
    if kelas.getNpmandNameMahasiswa(num):
        npm, nama=kelas.getNpmandNameMahasiswa(num)
        try:
            if checkMhs(npm):
                if checkRevisi(npm, tahun_id):
                    msgreply = checkRevisi(npm, tahun_id)
                    msgreply += f'\n{checkSidang(npm, tahun_id)}'
                else:
                    msgreply = "Revisi dulu gih sana...."
                
            else:
                msgreply = "Kamu emg ikutan sidang? jgn ngadi-ngadi deh..."
        except Exception as e: 
            msgreply = f"Error {str(e)}"
    else:
        msgreply = f"Hayoo siapa kamu"
    
    
    
    return msgreply

def checkSidang(npm, tahun_id):
    db=kelas.dbConnect()
    msg = "*TTD BA & Pengesahan Sidang :*\n\n"
    
    sql=f'select penguji_utama, penguji_pendamping, pembimbing_utama, pembimbing_pendamping, koordinator, kaprodi from sidang_data where npm="{npm}" and tahun_id="{tahun_id}"'
    
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row[0]:
            if row[0]:
                msg += f'Penguji Utama - Accept\n'
            if row[1]:
                msg += f'Penguji Pendamping - Accept\n'
            if row[2]:
                msg += f'Pembimbing Utama - Accept\n'
            if row[3]:
                msg += f'Pembimbing Pendamping - Accept\n'
            if row[4]:
                msg += f'Koordinator - Accept\n'
            if row[5]:
                msg += f'Kepala Prodi - Accept\n'                
        else:
            msg += "Belum Ada"

def checkRevisi(npm, tahun_id):
    db=kelas.dbConnect()
    msg = "*Revisi Sidang :*\n\n"
    
    sql=f'select distinct penguji from revisi_data where npm="{npm}" and tahun_id="{tahun_id}"'
    
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            for row in rows:
                msg += f'{row[0]} - Accept\n'
        else:
            msg += "Belum Ada"

def checkMhs(npm):
    db=kelas.dbConnect()
    sql=f'select npm from bimbingan_data where npm="{npm}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return False