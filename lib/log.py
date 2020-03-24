import pymysql, config

from datetime import datetime

def dbConnectIteung():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

def getDatetimeNow():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save(data):
    if data[3] == 'iteung kelas mulai' or data[3] == 'iiteung kelas mulai':
        print("not input")
    else:
        inserttolog(data)

def inserttolog(data):
    db = dbConnectIteung()
    sql = "INSERT INTO log VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(getDatetimeNow(), data[0], data[3], data[2], data[1], data[4])
    with db:
        cur = db.cursor()
        cur.execute(sql)