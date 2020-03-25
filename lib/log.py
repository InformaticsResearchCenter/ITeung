import pymysql, config

from datetime import datetime


#close commit #3
def dbConnectIteung():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

def getDatetimeNow():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save(data):
    if "teung kelas mulai" not in data[3]:
        inserttolog(data)

def logSaveIteungStart(data):
    return inserttolog(data)

def inserttolog(data):
    db = dbConnectIteung()
    sql = "INSERT INTO log VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(getDatetimeNow(), data[0], data[3], data[2], data[1], data[4])
    with db:
        cur = db.cursor()
        cur.execute(sql)