import pymysql, config

from numba import jit
from datetime import datetime

@jit(nopython=True)
def dbConnectIteung():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

@jit(nopython=True)
def getDatetimeNow():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@jit(nopython=True)
def save(data):
    if "teung kelas mulai" not in data[3]:
        inserttolog(data)

@jit(nopython=True)
def logSaveIteungStart(data):
    return inserttolog(data)

@jit(nopython=True)
def normalizeSql(msg):
    msg = msg.replace("'", "")
    msg = msg.strip()
    return msg

@jit(nopython=True)
def inserttolog(data):
    db = dbConnectIteung()
    sql = "INSERT INTO log VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(getDatetimeNow(), data[0], normalizeSql(data[3]), data[2], data[1], data[4])
    with db:
        cur = db.cursor()
        cur.execute(sql)