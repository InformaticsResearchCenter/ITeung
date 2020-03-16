from lib import lecturerPhoneNumber, message, wa, reply
from datetime import datetime
from importlib import import_module
import config
import pymysql

def dbConnect():
    db=pymysql.connect(config.db_host,config.db_username,config.db_password,config.db_name)
    return db

def replymsg(driver, msg):
    msgs=getAwaitingMessageKelasStart('kelas')
    msgs=msgs.replace('#MATKUL#', getMatkul(msg))
    msgs=msgs.replace('#BOTNAME#', config.bot_name)
    msgs.strip()
    wa.typeAndSendMessage(driver, msgs)
    msgreply=startkelas(driver, True, msg)
    return msgreply

def getMatkul(msg):
    msgs = msg.split(" ")
    getIndexMateri = msgs.index("materi")
    getIndexMatkul = msgs.index("matkul")
    matakuliah = listtostring(msgs[getIndexMatkul+1:getIndexMateri])
    return matakuliah

def getKodeDosen(msg):
    msgs=msg.split(" ")
    getIndexKodeDosen=msgs.index("dosen")
    kodeDosen=msgs[getIndexKodeDosen+1]
    return kodeDosen

def getDiscussion(msg):
    msgs=msg.split(" ")
    getIndexMateri=msgs.index("materi")
    getIndexMulai=msgs.index("mulai")
    discussion= msgs[getIndexMateri+1:getIndexMulai]
    return discussion

def selesaiMatkul(msg):
    msgs = msg.split(" ")
    print(msgs)
    getIndexStart = msgs.index("selesai")
    getIndexClass = msgs.index("matkul")
    matakuliah = listtostring(msgs[getIndexClass+1:getIndexStart])
    return matakuliah

def listtostring(msg):
    msgs = ' '
    return msgs.join(msg)

def numberAuth(num):
    if num in lecturerPhoneNumber.phoneNumber:
        return True
    else:
        return False

def inserttod4ti_3a(npm, number_phone, lecturer, course, discussion, date_time, message):
    db=dbConnect()
    discussion=listtostring(discussion)
    sql="insert into d4ti_3a(npm, number_phone, lecturer, course, discussion, date_time, message) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(npm, number_phone, lecturer, course, discussion, date_time, message)
    print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)

def startkelas(driver, kelas, msg):
    msgcek=''
    alscek=''
    numcek=''

    discussion=getDiscussion(msg)
    course=getMatkul(msg)
    kodedosen=getKodeDosen(msg)

    getdatetimenow = datetime.now()
    timestart = getdatetimenow.strftime("%Y-%m-%d %H:%M:%S")

    while kelas:
        data = wa.getData(driver)

        getDateTimeNow = datetime.now()

        datetimenow = getDateTimeNow.strftime("%Y-%m-%d %H:%M:%S")

        msg = data[2]
        als = data[1]
        num = data[0]

        als=als.split('-')[0]

        msg = message.normalize(msg)
        msgs = msg.split(" ")

        if msgcek != msg or (numcek != num and alscek != als):
            inserttod4ti_3a(npm=als, number_phone=num, lecturer=kodedosen, course=course, discussion=discussion, date_time=datetimenow, message=msg)
            msgcek=msg
            numcek=num
            alscek=als

        if msg.find(config.bot_name) >= 0:
            if len(msgs) == 1:
                msgreply = reply.getOpeningMessage()
            else:
                msgreply = reply.message(msg)
                if msgreply[:2] == 'm:':
                    if msgreply[2:] == 'kelas':
                        if msgs[-1] == "selesai":
                            modulename = msgreply.split(":")[1]
                            mod = import_module('module.' + modulename)
                            namamatkul = mod.selesaiMatkul(msg)
                            msgreply = "oke, matkul " + namamatkul + " selesai"
                            kelas = False
    beritaAcara(driver, kodedosen, course, discussion, timestart)
    return msgreply

def getAwaitingMessageKelasStart(module):
    db=dbConnect()
    content= ''
    sql = "SELECT content FROM waiting_message WHERE module_name = '{0}' AND content LIKE '%mulai%' ORDER BY RAND() LIMIT 1".format(module)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            content=rows[0]
    return content

def getTanggalTerakhir():
    db = dbConnect()
    tanggal=''
    sql="SELECT DATE_FORMAT(date_time, '%d-%m-%Y') FROM d4ti_3a ORDER BY date_time DESC LIMIT 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            tanggal=rows[0]
    return tanggal

def getJamTerakhir():
    db = dbConnect()
    tanggal=''
    sql="SELECT DATE_FORMAT(date_time, '%H:%i:%s') FROM d4ti_3a ORDER BY date_time DESC LIMIT 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            tanggal=rows[0]
    return tanggal

def getAwaitingMessageKelasStop(module):
    db=dbConnect()
    content= ''
    sql = "SELECT content FROM waiting_message WHERE module_name = '{0}' AND content LIKE '%mulai%' ORDER BY RAND() LIMIT 1".format(module)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            content=rows[0]
    return content

def getNamaDosen(kodedosen):
    db=dbConnect()
    nama=''
    sql="SELECT nama FROM dosen WHERE kode_dosen = '{0}'".format(kodedosen)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            nama=rows[0]
    return nama

def getHadirNpm(time):
    db = dbConnect()
    sql="SELECT DISTINCT npm from d4ti_3a WHERE date_time > '{0}'".format(time)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
    return rows

def beritaAcara(driver, kodedosen, course, discussion, timestart):
    namadosen = getNamaDosen(kodedosen)
    matkul = course
    tanggal = getTanggalTerakhir()
    waktumulai = str(timestart).split(" ")[1]
    waktuselesai = getJamTerakhir()
    materi = listtostring(discussion)
    kehadirannpm = getHadirNpm(timestart)
    data = []
    for kehadiran in kehadirannpm:
        for npm in kehadiran:
            data.append(npm)
    messages = "Nama Dosen: " + namadosen \
               + "\n Mata Kuliah: " + matkul \
               + "\n Tanggal: " + tanggal \
               + "\n Waktu Mulai: " + waktumulai \
               + "\n Waktu Selesai: " + waktuselesai \
               + "\n Materi: " + materi
    wa.typeAndSendMessage(driver, messages)
    number = 1
    for npm in data:
        wa.typeAndSendMessage(driver, str(number)+". "+npm)
        number=int(number)+1