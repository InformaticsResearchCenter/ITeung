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
        try:
            npm = [npm for npm in msg.split(' ') if npm.isdigit() and len(npm) == 7][0]
        except:
            npm = None
            
        if npm:
            try:
                if checkMhs(npm):
                    if checkRevisi(npm, tahun_id):
                        msgreply = "Ini revisian dari Anda cuy..."+checkRevisi(npm, tahun_id)
                    else:
                        msgreply = "Emg udh masukin revisi???"
                else:
                    msgreply = "Salah mahasiswa ato npm mungkin..."
            except Exception as e: 
                msgreply = f"Error {str(e)}"
        else:
            try:
                if checkRevisiPenguji(tahun_id, kodeDosen):
                    msgreply = "Ini revisian dari anda cuy..."+checkRevisiPenguji(tahun_id, kodeDosen)
                else:
                    msgreply = "Emg udh masukin revisi???"
            except Exception as e: 
                msgreply = f"Error {str(e)}"
            
    elif kelas.getNpmandNameMahasiswa(num):
        npm, nama=kelas.getNpmandNameMahasiswa(num)
        try:
            if checkMhs(npm):
                if checkRevisi(npm, tahun_id):
                    msgreply = "Selamat revisian cuy..., semangat <3<3"+checkRevisi(npm, tahun_id)
                else:
                    msgreply = "Kamu emg udh sidang? jgn ngadi-ngadi deh..., mungkin aja blm dibikin revisinya sama penguji bersangkutan..., semangat <3<3"
            else:
                msgreply = "Kamu emg ikutan sidang? jgn ngadi-ngadi deh..."
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

def getListMhs(kodeDosen, tahun_id):
    db=kelas.dbConnect()    
    listMhs = list()
        
    sql=f'select distinct(npm) from revisi_data where penguji="{kodeDosen}" and tahun_id="{tahun_id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            for row in rows:
                listMhs.append(row[0])
    return listMhs

def getListPenguji(tahun_id, npm):
    db=kelas.dbConnect()    
    listPenguji = list()  
    
    sql=f'select distinct(penguji) from revisi_data where npm="{npm}" and tahun_id="{tahun_id}"'        
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            for row in rows:
                listPenguji.append(row[0])
    return listPenguji
        

def checkRevisiPenguji(tahun_id, kodeDosen):
    db=kelas.dbConnect()    
    msg = ""
    listMhs = getListMhs(kodeDosen, tahun_id)
    # print(listMhs)
    if listMhs:
        for npm in listMhs:
            listPenguji = getListPenguji(tahun_id, npm)
            # print(listPenguji)
            if listPenguji:
                for penguji in listPenguji:
                    sql=f'select revisi, id from revisi_data where npm="{npm}" and tahun_id="{tahun_id}" and penguji="{penguji}"'
                    with db:
                        cur=db.cursor()
                        cur.execute(sql)
                        rows=cur.fetchall()
                        if rows:
                            msg += f"\n\n*Revisi untuk {npm} dari {penguji}*"
                            for i, row in enumerate(rows):
                                msg += f"\n{(i+1)}. {row[0]} ({row[1]})"
            else:
                return False
        return msg
    else:
        return False
    
def checkRevisi(npm, tahun_id):
    db=kelas.dbConnect()
    msg = ""    
    listPenguji = list()
    status =True    
    
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
            sql=f'select revisi, id from revisi_data where npm="{npm}" and penguji="{penguji}" and tahun_id="{tahun_id}"'
            with db:
                cur=db.cursor()
                cur.execute(sql)
                rows=cur.fetchall()
                if rows:
                    msg += f"\n\n*Revisi untuk {npm} dari {penguji}*"
                    for i, row in enumerate(rows):
                        msg += f"\n{(i+1)}. {row[0]} ({row[1]})"
                        
        return msg
            
    else:
        return False