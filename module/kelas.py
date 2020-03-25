from lib import wa, numbers
from datetime import datetime
from time import sleep

import config
import pymysql

# def replymsg(driver, data):
#     log.logSaveIteungStart(data)
#     msg = data[3]
#     grp = data[1]
#     num = data[0]
#     msg = message.normalize(msg)
#     msgs = list(msg.split(" "))
#     coursename=getDataMatkul(grp.split('-')[0], kodeKelas(grp.split('-')[1]), num)[1]
#     starttimeclass=getDataMatkul(grp.split('-')[0], kodeKelas(grp.split('-')[1]), num)[3]
#     endtimeclass=getDataMatkul(grp.split('-')[0], kodeKelas(grp.split('-')[1]), num)[4]
#     if msgs[-1] == 'mulai':
#         if sudahinput(wa.getGroupName(driver)) == True:
#             msgreply = "mohon maaf matakuliah ini tidak bisa dimulai, mohon menunggu hingga minggu depan... terima kasih"
#         else:
#             if isMatkul(grp.split('-')[0], kodeKelas(grp.split('-')[1]), num):
#                 messages=getAwaitingMessageKelasStart('kelas')
#                 messages=messages.replace('#MATKUL#', coursename)
#                 messages=messages.replace('#BOTNAME#', config.bot_name)
#                 msgreply=messages
#             else:
#                 msgreply='mohon maaf kode dosen bapak/ibu dengan kode matkul ini tidak ditemukan'
#     else:
#         msgreply='oke selesai crot!'
#         beritaAcara(driver, num, coursename, starttimeclass, endtimeclass, grp)
#     return msgreply

def dbConnect():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db

def dbConnectSiap():
    db= pymysql.connect(config.db_host_siap, config.db_username_siap, config.db_password_siap, config.db_name_siap)
    return db

def kodeKelas(kode):
    switcher = {
        'A': '01',
        'B': '02',
        'C': '03',
        'D': '04',
        'E': '05',
        'F': '06',
        'G': '07',
        'H': '08',
        'I': '09',
        'J': '10',
    }
    return switcher.get(kode, "Not Found!")

def getnumonly(groupname):
    db=dbConnect()
    sql="select distinct number from log where DATE_FORMAT(timestamps, '%Y-%m-%d') = CURDATE() and groupname = '{0}'".format(groupname)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            return rows
        else:
            return ''

def getNpmandNameMahasiswa(num):
    num = numbers.normalize(num)
    db=dbConnectSiap()
    sql="select MhswID, Nama from simak_mst_mahasiswa where Handphone = '{0}'".format(num)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            return rows

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

def beritaAcara(driver, num, coursename, starttimeclass, endtimeclass, groupname, data):
    lecturername = getNamaDosen(getKodeDosen(num))
    tanggal = datetime.now().strftime("%d-%m-%Y")
    kodekelas=wa.getGroupName(driver).split('-')[1]
    messages = "Nama Dosen: " + str(lecturername) + \
               "\nMata Kuliah: " + str(coursename) + \
               "\nKelas: " + str(kodekelas) + \
               "\nTanggal: " + str(tanggal) + \
               "\nWaktu Mulai: " + str(starttimeclass) + \
               "\nWaktu Selesai: " + str(endtimeclass)
    messages = messages.split("\n")
    for msg in messages:
        wa.typeMessage(driver, msg)
        wa.lineBreakWhatsapp(driver)
    number = 1
    studentnumber=data
    for studentnum in studentnumber:
        if studentnum is not '':
            studentid=getNpmandNameMahasiswa(studentnum)[0]
            studentname=getNpmandNameMahasiswa(studentnum)[1]
            wa.typeMessage(driver, str(number)+". "+studentid+" "+studentname)
            wa.lineBreakWhatsapp(driver)
            number=int(number)+1
    wa.sendMessage(driver)
    msgreply="Oke teman-teman Matakuliah "+coursename+" sudah selesai dan telah berhasil diinputkan absensinya, mohon jaga kesehatan teman-teman yaaaa.... selalu cuci tangan teman-teman, dadaaaahhhhhh <3"
    return msgreply


def siapAbsensi(driver, num, namagroup, namamatkul):
    try:
        tanggalsekarang=datetime.now().strftime("%d/%m/%Y")
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
        findLecturerCode(driver, getKodeDosen(num).lower())
        findMatkul(driver, kodematkul, kodekelas)
        gettanggalabsen=driver.find_elements_by_xpath('/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr')
        gettanggalabsensiapterakhir=driver.find_element_by_xpath('/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr['+str(len(gettanggalabsen))+']/td[3]').text
        if tanggalsekarang == gettanggalabsensiapterakhir:
            AddMahasiswa(driver)
            hadir=Mahasiswa(driver, namagroup)
            Refresh(driver)
            closeTab(driver)
            switchWindowsHandleto0(driver)
        else:
            TambahPresensi(driver)
            simpan(driver)
            sleep(1)
            hadir=AddMahasiswa(driver)
            Mahasiswa(driver, namagroup)
            Refresh(driver)
            closeTab(driver)
            switchWindowsHandleto0(driver)
        msgreply = hadir
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
    return driver.find_element_by_xpath("/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr[" + str(len(jumTabel)) + "]/td[8]/a").click()


def Mahasiswa(driver, groupname):
    dataPhoneNumber=[]
    jumMahasiswa = int(driver.find_elements_by_class_name("inp1")[-1].text)
    index = 1
    numberphone=getnumonly(groupname)
    for getNpm in range(jumMahasiswa):
        for number in numberphone:
            if getNpmandNameMahasiswa(number[0]) is not None:
                npmMahasiswa=getNpmandNameMahasiswa(number[0])[0]
                npm = driver.find_element_by_xpath(
                    "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                        index) + "]/td[2]").text
                if npm == npmMahasiswa:
                    driver.find_element_by_xpath(
                        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                            index) + "]/td[4]/select/option[1]").click()
                    dataPhoneNumber.append(number[0])
                else:
                    driver.find_element_by_xpath(
                        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                            index) + "]/td[4]/select/option[4]").click()
        index += 1
    return dataPhoneNumber


def Refresh(driver):
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[2]/table/tbody/tr[5]/td/input[3]").click()


def TahunAkad(driver):
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[1]/table/tbody/tr[1]/td[3]/select/option[2]").click()
