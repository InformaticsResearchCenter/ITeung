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
    # tahun_id = '20192'    
    tahun_id = kelas.getTahunID()
    try:
        npm = [npm for npm in data[3].split(' ') if npm.isdigit() and len(npm) == 7][0]
        msg = data[3].split(" id ", 1)[1]
        id = [id for id in msg.split(' ') if npm.isdigit()][0]
        revisi = msg.lstrip(id).strip()
        print(npm, revisi, id)
        if checkRevisi(npm, kodeDosen, id, tahun_id):
            revisiSidang(npm, kodeDosen, revisi, tahun_id, id)
            msgreply = "Sudah update...\n\n"+listRevisi(npm, kodeDosen, tahun_id)
        else:
            msgreply = "Salah id ato gak ada akses"
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply


def checkRevisi(npm, penguji, id, tahun_id):
    db=kelas.dbConnect()
    sql=f'select revisi from revisi_data where npm="{npm}" and penguji="{penguji}" and tahun_id="{tahun_id}" and id="{id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False

def revisiSidang(npm, penguji, revisi, tahun_id, id):
    db=kelas.dbConnect()
    sql=f'UPDATE revisi_data SET revisi="{revisi}" WHERE npm="{npm}" and penguji="{penguji}" and tahun_id="{tahun_id}" and id="{id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        
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