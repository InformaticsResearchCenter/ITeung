import pymysql
import config

def dbConnect():
    db=pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

def replymsg(num):
    msgreply=insertNumber(num)
    return msgreply

def insertNumber(num):
    db=dbConnect()
    sql="INSERT INTO group_auth(number, group_id) VALUES ('%s',2)"%(num)
    with db:
        cur=db.cursor()
        cur.execute(sql)