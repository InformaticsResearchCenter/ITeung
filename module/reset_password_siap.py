import string, random, os, config
from lib import numbers, reply, wa
from module import siap


def auth(data):
    return cekNumber(data[0])


def replymsg(driver, data):
    wmsg=reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg=wmsg.replace('#BOTNAME#', config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    loginid = getLoginID(num=data[0])
    newpasswd=passwdGenerate()
    if loginid is not None:
        updatePassword(password=newpasswd, id=loginid)
        msgreply = 'sip sudah #BOTNAME# ganti ini ya *username* sama *password* yang terbaru:\n\nUsername: {id}\nPassword: {passwd}\n\nOke sudah yaaaa, mohon untuk segera diganti ya passwordnya, dadahhh... <3<3'.format(id=loginid, passwd=newpasswd)
    else:
        msgreply = 'aduh #BOTNAME# ga bisa nemuin datanya euyyyy, coba cek nomernya di siap udah sama belum sama di whatsapp, kalo udah diulangi lagi yaa...'
    return msgreply


def passwdGenerate(length=16, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    passwd = ''.join(random.choice(chars) for length in range(length))
    return passwd


def updatePassword(password, id):
    db = siap.dbConnect()
    sql1="UPDATE simak_mst_mahasiswa SET `Password` = MD5(MD5('{password}')) WHERE `Login` = '{id}';" .format(password=password, id=id)
    sql2="UPDATE simak_besan_users SET `user_password` = MD5(MD5('{password}')) WHERE `user_name` = '{id}';".format(password=password, id=id)
    sql3="UPDATE besan_users SET `user_password` = MD5(MD5('{password}')) WHERE `user_name` = '{id}';".format(password=password, id=id)
    with db:
        cur = db.cursor()
        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)


def cekNumber(num):
    db = siap.dbConnect()
    num = numbers.normalize(num)
    lecturer = "select * from simak_mst_dosen where Handphone='{num}'".format(num=num)
    student = "select * from simak_mst_mahasiswa where Handphone='{num}'".format(num=num)
    with db:
        cur = db.cursor()
        cur.execute(lecturer)
        row = cur.fetchone()
        if row is None:
            cur.execute(student)
            row = cur.fetchone()
            if row is None:
                ret = False
            else:
                ret = True
        else:
            ret = True
    return ret


def getLoginID(num):
    db = siap.dbConnect()
    num = numbers.normalize(num)
    lecturer = "select Login from simak_mst_dosen where Handphone='{num}'".format(num=num)
    student = "select Login from simak_mst_mahasiswa where Handphone='{num}'".format(num=num)
    with db:
        cur = db.cursor()
        cur.execute(lecturer)
        row = cur.fetchone()
        if row is None:
            cur.execute(student)
            row = cur.fetchone()
            if row is None:
                result = None
            else:
                result = row[0]
        else:
            result = row[0]
    return result