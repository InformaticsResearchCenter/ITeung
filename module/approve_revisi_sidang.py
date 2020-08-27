from module import kelas
from lib import wa, reply, message, numbers
import os, config
import pandas as pd

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
    tahun_id = '20192'
    try:
        npm = [npm for npm in data[3].split(' ') if npm.isdigit() and len(npm) == 7][0]
        if checkMhs(npm, kodeDosen):
            approveRevisiSidang(npm, kodeDosen, tahun_id)        
            msgreply = f"Dah diapprove ya {npm} oleh {kodeDosen}"
        else:
            msgreply = f"Anda bukan penguji {npm}"
            
    except Exception as e: 
        msgreply = f"Error {str(e)}"
    
    return msgreply

def approveRevisiSidang(npm, penguji, tahun_id):
    db=kelas.dbConnect()
    sql=f'UPDATE revisi_data SET status="True" WHERE npm="{npm}" and penguji="{penguji}" and tahun_id="{tahun_id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)

def checkMhs(npm, kodeDosen):
    df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')
    df.set_index('npm', inplace=True)
    listPem = ['pem3', 'pem4', ]
    pem = df.loc[int(npm), listPem].values.tolist()
    
    if kodeDosen in pem:
        return True
    else:
        return False
    