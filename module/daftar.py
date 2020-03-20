import pymysql
import config

def dbConnect():
    db=pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

def replymsg(num,msg):
    try:
        insertNumber(num)
        msgreply="oke data sudah masuk dengan berhasil, sekarang Bapak/Ibu dosen sudah bisa memulai kegiatan kelas, selamat mengajar :-)"
    except:
        msgreply="sepertinya nomer ini udah kedaftar deh coba minta tolong ke akang/teteh admin untuk dicek nomor hpnya..."
    return msgreply

def insertNumber(num):
    db=dbConnect()
    sql="INSERT INTO group_auth(number, group_id) VALUES('%s',2)"%(num)
    with db:
        cur=db.cursor()
        cur.execute(sql)