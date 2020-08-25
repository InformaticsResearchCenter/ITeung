from module import kelas
from lib import wa, reply, message, numbers
import os, config, pandas

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) != None or kelas.getKodeDosen(data[0]) != '':
        ret = True
    else:
        ret = False
    return ret


def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    msg = data[3].lower()
    num = numbers.normalize(data[0])
    tahun_id = kelas.getTahunID()
    
    if kelas.getKodeDosen(num):
        kodeDosen = kelas.getKodeDosen(num)
        npm = [npm for npm in msg.split(' ') if npm.isdigit() and len(npm) == 7][0]
        try:
            if checkMhs(npm):
                if checkRevisi(npm, tahun_id):
                    msgreply = "Ini revisian dari Anda cuy...\n"+checkRevisi(npm, tahun_id, kodeDosen)
                else:
                    msgreply = "Emg udh masukin revisi???"
            else:
                msgreply = "Salah mahasiswa ato npm mungkin..."
        except Exception as e: 
            msgreply = f"Error {str(e)}"
            
    elif kelas.getNpmandNameMahasiswa(num):
        npm, nama=kelas.getNpmandNameMahasiswa(num)
        try:
            if checkMhs(npm):
                if checkRevisi(npm, tahun_id):
                    msgreply = "Selamat revisian cuy...\n"+checkRevisi(npm, tahun_id)
                else:
                    msgreply = "Kamu emg udh sidang? jgn ngadi-ngadi deh..."
            else:
                msgreply = "Kamu emg ikutan? jgn ngadi-ngadi deh..."
        except Exception as e: 
            msgreply = f"Error {str(e)}"
    else:
        msgreply = f"Hayoo siapa kamu"
    
    
    
    return msgreply

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

def checkRevisi(npm, tahun_id, penguji=""):
    db=kelas.dbConnect()
    msg = ""    
    listPenguji = list()
    status =True    
    
    if penguji:
        sql=f'select distinct penguji from revisi_data where npm="{npm}" and tahun_id="{tahun_id}" and penguji="{penguji}"'
    else:
        sql=f'select distinct penguji from revisi_data where npm="{npm}" and tahun_id="{tahun_id}"'
    
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            for row in rows:
                listPenguji.append(row[0])
        else:
            status = False
            
    if(status):
        for penguji in listPenguji:
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
                    # print(revisi)
                    msg += f"\nRevisi untuk {npm} dari {penguji}"
                    for i, x in enumerate(revisi):
                        msg += f"\n{(i+1)}. {x}"
                        
        return msg
            
    else:
        return False