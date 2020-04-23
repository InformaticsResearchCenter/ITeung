import pymysql, config

from datetime import datetime


#closes commit #3
def dbConnectIteung():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

def getDatetimeNow():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save(num, msg, als, grp, isgrp):
    inserttolog(num, msg, als, grp, isgrp)

def logSaveIteungStart(data):
    return inserttolog(data)

def normalizeSql(msg):
    msg = msg.replace("'", "")
    msg = msg.replace("\\", "")
    msg = msg.strip()
    return msg

#close commit 11
def inserttolog(num, msg, als, grp, isgrp):
    db = dbConnectIteung()
    try:
        sql = "INSERT INTO log VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(getDatetimeNow(), num, normalizeSql(msg), normalizeSql(als), normalizeSql(grp), isgrp)
        with db:
            cur = db.cursor()
            cur.execute(sql)
    except:
        sql = "INSERT INTO log VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(getDatetimeNow(), num, normalizeSql(msg), normalizeSql('anak alay'), normalizeSql(grp), isgrp)
        with db:
            cur = db.cursor()
            cur.execute(sql)
