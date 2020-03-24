from lib import message, wa, reply, alias, numbers
from datetime import datetime
from importlib import import_module
from time import sleep

import config
import pymysql


def dbConnect():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

def dbConnectSiap():
    db= pymysql.connect(config.db_host_siap, config.db_username_siap, config.db_password_siap, config.db_name_siap)
    return db

def replymsg(driver, msg):
    if sudahinput(wa.getGroupName(driver).split("-")[0]) == True:
        msgreply = "mohon maaf matakuliah ini tidak bisa dimulai, mohon menunggu hingga minggu depan... terima kasih"
    else:
        msgs = getAwaitingMessageKelasStart('kelas')
        msgs = msgs.replace('#MATKUL#', getMatkul(msg))
        msgs = msgs.replace('#BOTNAME#', config.bot_name)
        msgs.strip()
        wa.typeAndSendMessage(driver, msgs)
        msgreply = startkelas(driver, True, msg)
    return msgreply

def isMatkul(kodematkul, kodekelas,num):
    num=numbers.normalize(num)
    db=dbConnectSiap()
    sql = "select MKKode, Nama, HariID, JamMulai, JamSelesai, NamaKelas from simak_trn_jadwal where DosenID = '{0}' and TahunID = '".format(getKodeDosen(num)) + config.siap_tahun_id + "' and NamaKelas = '{0}' and MKKode = '{1}'".format(kodekelas, kodematkul)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            return True
        else:
            return False

def getDataMatkul(kodematkul, kodekelas, num):
    num = numbers.normalize(num)
    db = dbConnectSiap()
    sql = "select MKKode, Nama, HariID, DATE_FORMAT(JamMulai, '%H:%i:%s'), DATE_FORMAT(JamSelesai, '%H:%i:%s'), NamaKelas from simak_trn_jadwal where DosenID = '{0}' and TahunID = '".format(getKodeDosen(num)) + config.siap_tahun_id + "' and NamaKelas = '{0}' and MKKode = '{1}'".format(kodekelas, kodematkul)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            return rows
        else:
            return ''

def getKodeDosen(num):
    num = numbers.normalize(num)
    kodedosen=''
    db=dbConnectSiap()
    sql="select Login from simak_mst_dosen where Handphone = '{0}'".format(num)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            kodedosen=rows[0]
    return kodedosen

def getAwaitingMessageKelasStart(module):
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM waiting_message WHERE module_name = '{0}' AND content LIKE '%mulai%' ORDER BY RAND() LIMIT 1".format(module)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content

def sudahinput(groupname):
    db = dbConnect()
    sql = "SELECT * from log WHERE DATE_FORMAT(timestamps, '%Y-%m-%d') = CURDATE() and groupname = '{0}' and message LIKE '%teung kelas mulai%'".format(groupname)
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
    db = dbConnectSiap()
    sql = "select Nama, Gelar from simak_mst_dosen where Login = '{0}'".format(kodedosen)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            namadosen=rows[0]
            gelar= rows[1]
            if gelar[0]=='D' or gelar[0]=="I" or gelar[0]=='i':
                return gelar+namadosen
            else:
                return namadosen+' '+gelar

def getHadirAlias(time):
    db = dbConnect()
    sql = "SELECT DISTINCT alias from d4ti_2b WHERE date_time > '{0}'".format(time)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

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
    kehadiranalias = getHadirAlias(timestart)
    data = []
    for kehadiran in kehadiranalias:
        for hadir in kehadiran:
            data.append(hadir)
    messages = "Nama Dosen: " + str(namadosen) + \
               "\nMata Kuliah: " + str(matkul) + \
               "\nKelas: " + str(wa.getGroupName(driver).split('-')[1]) + \
               "\nTanggal: " + str(tanggal) + \
               "\nWaktu Mulai: " + str(waktumulai) + \
               "\nWaktu Selesai: " + str(waktuselesai) + \
               "\nMateri: " + str(materi)
    messages = messages.split("\n")
    for msg in messages:
        wa.typeMessage(driver, msg)
        wa.lineBreakWhatsapp(driver)
    number = 1
    for npm in data:
        wa.typeMessage(driver, str(number) + ". " + str(npm).replace('-', ' '))
        wa.lineBreakWhatsapp(driver)
        number = int(number) + 1
    wa.sendMessage(driver)


def siapAbsensi(driver, kodedosen, namagroup, timestart, namamatkul):
    try:
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
        msgreply = "oke, matkul " + namamatkul + " selesai, dan teman teman yang hadir tadi sudah diinputkan ke absensi siap, terima kasih Bapak/Ibu dosen yang sudah mengajar, selamat beraktivitas kembali, dan jangan lupa ya Cuci Tangan agar temen-temen semua sehat, sampai ketemu dipertemuan selanjutnya dadahhhhh........"
    except Exception as e:
        msgreply = "error: " + str(e)
        closeTab(driver)
        switchWindowsHandleto0(driver)
    return msgreply


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
    jumTabel = driver.find_elements_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr")
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr[" + str(
            len(jumTabel)) + "]/td[8]/a").click()


def Mahasiswa(driver, npm):
    mahasiswa = npm
    jumMahasiswa = int(driver.find_elements_by_class_name("inp1")[-1].text)
    index = 1
    for getNpm in range(jumMahasiswa):
        npm = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                index) + "]/td[2]").text
        if npm in mahasiswa:
            driver.find_element_by_xpath(
                "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                    index) + "]/td[4]/select/option[1]").click()
        else:
            driver.find_element_by_xpath(
                "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                    index) + "]/td[4]/select/option[4]").click()
        index += 1


def Refresh(driver):
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[2]/table/tbody/tr[5]/td/input[3]").click()


def TahunAkad(driver):
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[1]/table/tbody/tr[1]/td[3]/select/option[2]").click()
