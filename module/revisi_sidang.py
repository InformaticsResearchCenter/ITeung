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
    # wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    # wa.typeAndSendMessage(driver, wmsg)
    num = numbers.normalize(data[0])
    kodeDosen = kelas.getKodeDosen(num)
    tahun_id = kelas.getTahunID()
    try:
        msg = data[3].split(';')
        if len(msg) > 1 and msg[1] != "":
            npm = [npm for npm in msg[0].split(' ') if npm.isdigit() and len(npm) == 7][0]
            if checkMhs(npm):
                revisi = ';'.join([data.strip().strip(';') for data in msg[1:] if data != '' and data != ' '])
                if revisi:
                    for r in revisi.split(';'):
                        print(r)
                        if checkRevisi(npm, kodeDosen, r, tahun_id):
                            pass
                        else:
                            revisiSidang(npm, kodeDosen, r, tahun_id)
                    msgreply = "Sudah masuk...\n\n"+listRevisi(npm, kodeDosen, tahun_id)
                else:
                    msgreply = "Revisinya mana, btw jgn lupa pake ; buat misahin revisinya"
            else:
                msgreply = "Mahasiswanya tdk terdaftar ato salah npm mungkin..."
        else:
            msgreply = "Revisinya mana, btw jgn lupa pake ; buat misahin revisinya"
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def checkRevisi(npm, penguji, revisi, tahun_id):
    db=kelas.dbConnect()
    sql=f'select revisi from revisi_data where npm="{npm}" and penguji="{penguji}" and tahun_id="{tahun_id}" and revisi="{revisi}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False

def listRevisi(npm, penguji, tahun_id):
    db=kelas.dbConnect()
    sql=f'select revisi, id from revisi_data where npm="{npm}" and penguji="{penguji}" and tahun_id="{tahun_id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows:            
            msg = f"Revisi untuk {npm} dari {penguji}"
            for i, row in enumerate(rows):
                msg += f"\n{(i+1)}. {row[0]} ({row[1]})"
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

