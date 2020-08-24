from module import kelas
from lib import wa, reply, message, numbers
import os, config, pandas


def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    num = numbers.normalize(data[0])
    kodeDosen = kelas.getKodeDosen(num)
    tahun_id = kelas.getTahunID()
    try:
        msg = data[3].split(';')
        npm = [npm for npm in msg[0].split(' ') if npm.isdigit() and len(npm) == 7][0]
        if checkMhs(npm):
            revisi = ';'.join([data.strip() for data in msg[1:] if data != ''])
            revisiSidang(npm, kodeDosen, revisi, tahun_id)
            msgreply = "Sudah masuk...\n\n"+checkRevisi(npm, kodeDosen, tahun_id)
        else:
            msgreply = "Mahasiswanya tdk terdaftar ato salah npm mungkin..."
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def checkRevisi(npm, penguji, tahun_id):
    db=kelas.dbConnect()
    sql=f'select revisi from revisi_data where npm="{npm}" and penguji="{penguji}" and tahun_id="{tahun_id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            listRevisi = list()
            for row in rows:
                listRevisi.extend(row[0].split(";"))
            revisi = set(listRevisi)
            msg = f"Revisi untuk {npm} dari {penguji}"
            for i, x in enumerate(revisi):
                msg += f"\n{(i+1)}. {x}"
                
            return msg
        else:
            return False

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

def revisiSidang(npm, penguji, revisi, tahun_id):
    db=kelas.dbConnect()
    sql=f"INSERT INTO revisi_data (npm, penguji, revisi, tahun_id) VALUE ('{npm}', '{penguji}', '{revisi}', '{tahun_id}')"
    with db:
        cur=db.cursor()
        cur.execute(sql)