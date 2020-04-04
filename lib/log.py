import pymysql, config

from datetime import datetime


#closes commit #3
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

def normalizeSql(msg):
    msg = msg.replace("'", "")
    msg = msg.strip()
    return msg

#close commit 11
def inserttolog(data):
    db = dbConnectIteung()
    try:
        sql = "INSERT INTO log VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(getDatetimeNow(), data[0], normalizeSql(data[3]), normalizeSql(data[2]), normalizeSql(data[1]), data[4])
        with db:
            cur = db.cursor()
            cur.execute(sql)
    except:
        sql = "INSERT INTO log VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(getDatetimeNow(), data[0], normalizeSql(data[3]), normalizeSql('anak alay'), normalizeSql(data[1]), data[4])
        with db:
            cur = db.cursor()
            cur.execute(sql)
