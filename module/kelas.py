from lib import message, wa, reply, alias
from datetime import datetime
from importlib import import_module
from time import sleep
from selenium.webdriver.common.keys import Keys


import config
import pymysql


def dbConnect():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db


def replymsg(driver, msg):
    if sudahinput(getNamaGroup(driver).split("-")[0]) == True:
        msgreply="mohon maaf matakuliah ini tidak bisa dimulai, mohon menunggu hingga minggu depan... terima kasih"
    else:
        msgs = getAwaitingMessageKelasStart('kelas')
        msgs = msgs.replace('#MATKUL#', getMatkul(msg))
        msgs = msgs.replace('#BOTNAME#', config.bot_name)
        msgs.strip()
        wa.typeAndSendMessage(driver, msgs)
        msgreply = startkelas(driver, True, msg)
    return msgreply


def getMatkul(msg):
    msgs = msg.split(" ")
    getIndexMateri = msgs.index("materi")
    getIndexMatkul = msgs.index("matkul")
    matakuliah = listtostring(msgs[getIndexMatkul + 1:getIndexMateri])
    return matakuliah


def getKodeDosen(msg):
    msgs = msg.split(" ")
    getIndexKodeDosen = msgs.index("dosen")
    kodeDosen = msgs[getIndexKodeDosen + 1]
    return kodeDosen


def getDiscussion(msg):
    msgs = msg.split(" ")
    getIndexMateri = msgs.index("materi")
    getIndexMulai = msgs.index("mulai")
    discussion = msgs[getIndexMateri + 1:getIndexMulai]
    return discussion


def selesaiMatkul(msg):
    msgs = msg.split(" ")
    getIndexStart = msgs.index("selesai")
    getIndexClass = msgs.index("matkul")
    matakuliah = listtostring(msgs[getIndexClass + 1:getIndexStart])
    return matakuliah

def listtostring(msg):
    msgs = ' '
    return msgs.join(msg)

def inserttod4ti_3a(npm, number_phone, lecturer, course, discussion, date_time, message, kode_matkul, alias):
    db = dbConnect()
    discussion = listtostring(discussion)
    sql = "insert into d4ti_2b(npm, number_phone, lecturer, course, discussion, date_time, message, kode_matkul, alias) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
    npm, number_phone, lecturer, course, discussion, date_time, message, kode_matkul, alias)
    print(sql)
    with db:
        cur = db.cursor()
        cur.execute(sql)

def startkelas(driver, kelas, msg):
    msgcek = ''
    alscek = ''
    numcek = ''
    discussion = getDiscussion(msg)
    course = getMatkul(msg)
    kodedosen = getKodeDosen(msg)
    getdatetimenow = datetime.now()
    timestart = getdatetimenow.strftime("%Y-%m-%d %H:%M:%S")
    while kelas:
        data = wa.getData(driver)
        getDateTimeNow = datetime.now()
        datetimenow = getDateTimeNow.strftime("%Y-%m-%d %H:%M:%S")
        msg = data[2]
        als = data[1]
        num = data[0]
        alss = als.split('-')[0]
        alss = alias.normalize(alss)
        msg = message.normalize(msg)
        msgs = msg.split(" ")
        if msgcek != msg or (numcek != num and alscek != alss):
            inserttod4ti_3a(npm=alss, number_phone=num, lecturer=kodedosen, course=course, discussion=discussion,
                            date_time=datetimenow, message=msg, kode_matkul=getNamaGroup(driver).split("-")[0], alias=als)
            msgcek = msg
            numcek = num
            alscek = alss
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
                            msgreply = "oke, matkul " + namamatkul + " selesai, dan teman teman yang hadir tadi sudah diinputkan ke absensi siap, terima kasih Bapak/Ibu dosen yang sudah mengajar, selamat beraktivitas kembali, dan jangan lupa ya Cuci Tangan agar temen-temen semua sehat, sampai ketemu dipertemuan selanjutnya dadahhhhh........"
                            kelas = False
    beritaAcara(driver, kodedosen, course, discussion, timestart)
    siapAbsensi(driver, kodedosen, getNamaGroup(driver), timestart)
    return msgreply


def getAwaitingMessageKelasStart(module):
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM waiting_message WHERE module_name = '{0}' AND content LIKE '%mulai%' ORDER BY RAND() LIMIT 1".format(
        module)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content


def sudahinput(kodematkul):
    db = dbConnect()
    sql = "SELECT * from d4ti_2b WHERE DATE_FORMAT(date_time, '%Y-%m-%d') = CURDATE() and kode_matkul = '{0}'".format(kodematkul)
    status = False
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            status = True
    return status


def getTanggalTerakhir():
    db = dbConnect()
    tanggal = ''
    sql = "SELECT DATE_FORMAT(date_time, '%d-%m-%Y') FROM d4ti_2b ORDER BY date_time DESC LIMIT 1"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            tanggal = rows[0]
    return tanggal


def getJamTerakhir():
    db = dbConnect()
    tanggal = ''
    sql = "SELECT DATE_FORMAT(date_time, '%H:%i:%s') FROM d4ti_2b ORDER BY date_time DESC LIMIT 1"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            tanggal = rows[0]
    return tanggal


def getAwaitingMessageKelasStop(module):
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM waiting_message WHERE module_name = '{0}' AND content LIKE '%mulai%' ORDER BY RAND() LIMIT 1".format(
        module)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content


def getNamaDosen(kodedosen):
    db = dbConnect()
    nama = ''
    sql = "SELECT nama FROM dosen WHERE kode_dosen = '{0}'".format(kodedosen)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            nama = rows[0]
    return nama


def getNamaGroup(driver):
    return driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span').text


def getHadirNpm(time):
    db = dbConnect()
    sql = "SELECT DISTINCT npm from d4ti_2b WHERE date_time > '{0}'".format(time)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
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
    messages="Nama Dosen: " + str(namadosen)+"\nMata Kuliah: " + str(matkul)+"\nKelas: " +str(getNamaGroup(driver).split('-')[1])+"\nTanggal: " + str(tanggal)+"\nWaktu Mulai: " + str(waktumulai)+"\nWaktu Selesai: " + str(waktuselesai)+"\nMateri: " + str(materi)
    messages=messages.split("\n")
    for msg in messages:
        wa.typeMessage(driver, msg)
        wa.lineBreakWhatsapp(driver)
    number = 1
    for npm in data:
        wa.typeMessage(driver, str(number)+". "+str(npm))
        wa.lineBreakWhatsapp(driver)
        number=int(number)+1
    wa.sendMessage(driver)

def siapAbsensi(driver, kodedosen, namagroup, timestart):
    kehadirannpm = getHadirNpm(timestart)
    datakehadirannpm = []
    for kehadiran in kehadirannpm:
        for npm in kehadiran:
            datakehadirannpm.append(npm)
    namagroupsplit = namagroup.split("-")
    kodematkul = namagroupsplit[0]
    kodekelas = namagroupsplit[1]
    openSiapwithNewTab(driver)
    switchWindowsHandleto1(driver)
    try:
        loginSiap(driver)
    except:
        print("sudah login")
    sleep(1)
    ClickPresensi(driver)
    TahunAkad(driver)
    findLecturerCode(driver, kodedosen)
    findMatkul(driver, kodematkul, kodekelas)
    TambahPresensi(driver)
    simpan(driver)
    sleep(1)
    AddMahasiswa(driver)
    Mahasiswa(driver, datakehadirannpm)
    Refresh(driver)
    closeTab(driver)
    switchWindowsHandleto0(driver)


def closeTab(driver):
    return driver.close()


def openSiapwithNewTab(driver):
    return driver.execute_script("window.open('http://siap.poltekpos.ac.id/siap/besan.depan.php');")


def switchWindowsHandleto1(driver):
    return driver.switch_to_window(driver.window_handles[1])


def switchWindowsHandleto0(driver):
    return driver.switch_to_window(driver.window_handles[0])


def loginSiap(driver):
    username = driver.find_elements_by_class_name("textbox")[0]
    username.send_keys(config.username_siap)

    sleep(1)

    password = driver.find_elements_by_class_name("textbox")[1]
    password.send_keys(config.password_siap)

    sleep(1)

    login = driver.find_element_by_class_name("button")
    login.click()


def ClickPresensi(driver):
    return driver.find_elements_by_class_name("side")[-1].click()


def findLecturerCode(driver, kodedosen):
    lecturercode = driver.find_elements_by_xpath(
        '/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p/table/tbody/tr[2]/td[2]/select/option')
    for i in lecturercode:
        kodesplit = i.text.split(" ")
        codeoflecturer = kodesplit[-1]
        codeoflecturer = codeoflecturer.lower()
        if kodedosen == codeoflecturer:
            i.click()
            break


def findMatkul(driver, matkul, kelas):
    print(matkul)
    print(kelas)
    listofmatkul = driver.find_elements_by_xpath(
        '/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p/table/tbody/tr[3]/td[2]/select/option')
    for data in listofmatkul:
        matkulsplit = data.text.split(" ")
        if matkulsplit[-1] == '---':
            kodematkul = ''
            kodekelas = ''
        else:
            kodematkul = matkulsplit[2]
            kodekelas = matkulsplit[-6]
        if kodematkul == matkul and kodekelas == kelas:
            data.click()
            break


def TambahPresensi(driver):
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[2]/table/tbody/tr[5]/td/input[2]").click()


def simpan(driver):
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr[7]/td/input[1]").click()


def AddMahasiswa(driver):
    jumTabel = driver.find_elements_by_xpath("/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr")
    return driver.find_element_by_xpath("/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr["+str(len(jumTabel))+"]/td[8]/a").click()


def Mahasiswa(driver, npm):
    mahasiswa = npm
    jumMahasiswa = int(driver.find_elements_by_class_name("inp1")[-1].text)
    index = 1
    for getNpm in range(jumMahasiswa):
        npm = driver.find_element_by_xpath("/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr["+str(index)+"]/td[2]").text
        if npm in mahasiswa:
            driver.find_element_by_xpath("/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr["+str(index)+"]/td[4]/select/option[1]").click()
        else:
            driver.find_element_by_xpath("/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr["+str(index)+"]/td[4]/select/option[4]").click()
        index += 1


def Refresh(driver):
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[2]/table/tbody/tr[5]/td/input[3]").click()


def TahunAkad(driver):
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[1]/table/tbody/tr[1]/td[3]/select/option[2]").click()
