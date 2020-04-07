from module import kelas
from lib import wa, reply
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

import os
import subprocess
import string
import ssl
import smtplib
import config
import time
import unicodedata
import re
import urllib.request
import sys
import pandas as pd
import pymysql


def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret


def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    kodedosen = kelas.getKodeDosen(data[0])
    subprocess.Popen(["python", "main_jadwal_uts.py", kodedosen],
                     cwd=r"C:\Users\LENOVO\Desktop\ITeung")
    return ''


def dbConnectSiap():
    db = pymysql.connect(config.db_host_siap,
                         config.db_username_siap,
                         config.db_password_siap,
                         config.db_name_siap)
    return db


def getEmailDosen(matkul, kelas, tahun):
    db = dbConnectSiap()
    sql = """
            select d.Email,j.JadwalID,j.TahunID,j.NamaKelas,CASE
            WHEN j.ProdiID ='.13.' THEN 'D3 Teknik Informatika'
            WHEN j.ProdiID ='.14.' THEN 'D4 Teknik Informatika'
            WHEN j.ProdiID ='.23.' THEN 'D3 Manajemen Informatika'
            WHEN j.ProdiID ='.33.' THEN 'D3 Akuntansi'
            WHEN j.ProdiID ='.34.' THEN 'D4 Akuntansi Keuangan'
            WHEN j.ProdiID ='.43.' THEN 'D3 Manajemen Pemasaran'
            WHEN j.ProdiID ='.44.' THEN 'D4 Manajemen Perusahaan'
            WHEN j.ProdiID ='.53.' THEN 'D3 Logistik Bisnis'
            WHEN j.ProdiID ='.54.' THEN 'D4 Logistik Bisnis'
            END AS namaprodi,j.MKKode,j.DosenID,d.Nama,j.Nama,j.HariID,
            j.JamMulai,j.JamSelesai,j.DosenID 
            from simak_trn_jadwal as j join simak_mst_dosen as d
            where  j.dosenid=d.login and j.MKKode = '""" + matkul + """' 
            and j.NamaKelas = '""" + kelas + """' and TahunID = '""" + tahun + """';
        """

    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if "/" in rows[0]:
            return rows[0][0:rows[0].find("/") - 1].replace(" ", "")
        elif rows[0] != None and rows[0] != "":
            return rows[0].replace(" ", "")
        else:
            return 'NULL'


def getMatkulDosen(dosen, tahun):
    db = dbConnectSiap()
    sql = """
            select j.JadwalID,j.TahunID,j.NamaKelas,CASE
            WHEN j.ProdiID ='.13.' THEN 'D3 Teknik Informatika'
            WHEN j.ProdiID ='.14.' THEN 'D4 Teknik Informatika'
            WHEN j.ProdiID ='.23.' THEN 'D3 Manajemen Informatika'
            WHEN j.ProdiID ='.33.' THEN 'D3 Akuntansi'
            WHEN j.ProdiID ='.34.' THEN 'D4 Akuntansi Keuangan'
            WHEN j.ProdiID ='.43.' THEN 'D3 Manajemen Pemasaran'
            WHEN j.ProdiID ='.44.' THEN 'D4 Manajemen Perusahaan'
            WHEN j.ProdiID ='.53.' THEN 'D3 Logistik Bisnis'
            WHEN j.ProdiID ='.54.' THEN 'D4 Logistik Bisnis'
            END AS namaprodi,j.MKKode,j.Nama,j.HariID,
            j.JamMulai,j.JamSelesai,j.DosenID 
            from simak_trn_jadwal as j join simak_mst_dosen as d
            where  j.dosenid=d.login and j.DosenID = '""" + dosen + """' 
            and TahunID = '""" + tahun + """';
        """
    with db:
        matkul = []
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            matkul.append([row[2], row[3], row[4], row[5]])
    return pd.DataFrame(matkul, columns=['kelas', 'prodi', 'matkul', 'nama_matkul'])


def makeFile(driver, list_prodi_ujian, filters):
    launchJadwalUjianMenu(driver)
    getFile(driver, list_prodi_ujian, filters)
    driver.quit()


def getFile(driver, list_prodi_ujian, filters):
    chooseUjian(driver, filters)
    prodi_ujian = Select(
        driver.find_element_by_xpath("//select[@name='prodi']"))
    for prodi_selected in list_prodi_ujian:
        if getProdiFromDropdown(driver, prodi_selected, filters):
            printAbsensiUjian(driver, filters, prodi_selected)


def printAbsensiUjian(driver, filters, prodi):
    time.sleep(3)
    tabel_select = driver.find_element_by_xpath(
        "//table[@cellpadding='4' and @cellspacing='1']/tbody")
    time.sleep(3)
    index = 1
    while True:
        try:
            index += 1
            matkul_select = tabel_select.find_element_by_xpath(
                "//tr[" + str(index) + "]/td[8]").text
            time.sleep(1)
            matkul_select = matkul_select.replace(" ", "_")
            matkul_select = matkul_select.replace("-", "_")
            matkul_select = matkul_select.replace("(", "")
            matkul_select = matkul_select.replace(")", "")
            kelas_select = tabel_select.find_element_by_xpath(
                "//tr[" + str(index) + "]/td[9]").text
            time.sleep(1)
            kode_matkul_select = tabel_select.find_element_by_xpath(
                "//tr[" + str(index) + "]/td[7]").text
            time.sleep(2)
            email_select = getEmailDosen(
                kode_matkul_select, kelas_select, filters['tahun'])
            kelas_select = int(kelas_select.strip("0"))
            kelas_select = convertKelas(kelas_select)
            filename = ''
            if email_select != None:
                filename = "{}-{}-{}-{}-{}-{}".format(filters['tahun'], setUjian(
                    filters['jenis']), filters['program'], matkul_select, kelas_select, email_select)
            else:
                filename = "{}-{}-{}-{}-{}-NULL".format(filters['tahun'], setUjian(
                    filters['jenis']), filters['program'], matkul_select, kelas_select)
            checkDir(prodi)
            if os.path.exists('absensi/' + prodi + '/' + filename + '.pdf'):
                os.remove('absensi/' + prodi + '/' + filename + '.pdf')
            try:
                edit_select = tabel_select.find_element_by_xpath(
                    "//tr[" + str(index) + "]/td[16]/a")
                time.sleep(1)
                edit_select.send_keys(Keys.ENTER)
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)
                url_select = driver.find_element_by_link_text(
                    "Cetak Laporan").get_attribute('href')
                urllib.request.urlretrieve(
                    url_select, 'absensi/' + prodi + '/' + filename + '.txt')
                time.sleep(2)
                makePDFOfAbsensiUjian(filename, prodi)
                time.sleep(2)
                if os.path.exists('absensi/' + prodi + '/' + filename + '.txt'):
                    os.remove('absensi/' + prodi + '/' + filename + '.txt')
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)
                print('File ' + filename + '.pdf berhasil dibuat')
            except NoSuchElementException:
                continue
        except NoSuchElementException:
            break

#########################


def makeFileForDosen(driver, dosens, filters):
    launchJadwalUjianMenu(driver)
    prodis = []
    nama_dosens = []
    for dosen in dosens:
        matkul = getMatkulDosen(dosen, filters['tahun'])
        prodis.extend(matkul['prodi'].tolist())
        nama_dosens.extend(matkul['nama_dosen'].tolist())

    prodis = list(set(prodis))
    nama_dosens = list(set(nama_dosens))
    all_ujian = getAllUjian(driver, prodis, nama_dosens, filters)
    print(all_ujian)
    print("\nSelesai mengambil semua ujian")
    for dosen in dosens:
        matkul = getMatkulDosen(dosen, filters['tahun'])
        matkul.sort_values(by=['prodi'], inplace=True)
        print(matkul)
        getFileForDosen(driver, all_ujian, matkul, filters)
    driver.quit()


def getFileForDosen(driver, all_ujian, matkul, filters):
    total = len(matkul)
    gagal = 0
    berhasil = 0
    for index, row in matkul.iterrows():
        ujian = all_ujian.loc[(all_ujian['matkul'] == row['nama_matkul']) & (all_ujian['prodi'] == row['prodi'])
                              & (all_ujian['kelas'] == int(row['kelas'].strip("0")))]
        if(ujian.empty):
            print("Jadwal "+row['nama_matkul']+" kelas " +
                  row['kelas']+" tidak ada di SIAP")
            gagal += 1
        else:
            index_ujian = ujian.iloc[0]['index']
            prodi_ujian = ujian.iloc[0]['prodi']
            matkul = {
                "prodi": prodi_ujian,
                "index": str(index_ujian),
                "kelas": ujian.iloc[0]['kelas'],
                "matkul": ujian.iloc[0]['matkul']
            }
            printAbsensiUjianForDosen(driver, matkul, filters)


def printAbsensiUjianForDosen(driver, matkul, filters):
    chooseUjian(driver, filters)
    prodi_ujian = Select(
        driver.find_element_by_xpath("//select[@name='prodi']"))
    for prodis in prodi_ujian.options:
        prodi = prodis.text[5:]
        if matkul['prodi'] == prodi:
            prodi_ujian.select_by_value(prodis.text[:2])
            break

    tampil_ujian = driver.find_element_by_xpath("//input[@name='Tampilkan']")
    tampil_ujian.send_keys(Keys.ENTER)

    time.sleep(2)
    tabel_select = driver.find_element_by_xpath(
        "//table[@cellpadding='4' and @cellspacing='1']/tbody")
    time.sleep(2)
    try:
        dhu_select = tabel_select.find_element_by_xpath(
            "//tr[" + matkul['index'] + "]/td[16]/a")
        print('Jadwal {} kelas {} diproses'.format(
            matkul['matkul'], matkul['kelas']))
        time.sleep(2)
        matkul_select = tabel_select.find_element_by_xpath(
            "//tr[" + matkul['index'] + "]/td[8]").text
        time.sleep(1)
        kelas_select = tabel_select.find_element_by_xpath(
            "//tr[" + matkul['index'] + "]/td[9]").text
        time.sleep(1)
        kode_matkul_select = tabel_select.find_element_by_xpath(
            "//tr[" + matkul['index'] + "]/td[7]").text

        email_select = getEmailDosen(
            kode_matkul_select, kelas_select, filters['tahun'])
        kelas_select = int(kelas_select.strip("0"))
        kelas_select = convertKelas(kelas_select)
        matkul_select = matkul_select.replace(" ", "_").replace("-", "_")
        matkul_select = matkul_select.replace("(", "").replace(")", "")
        filename = ''
        # Test with your email
        # email_select = 'divakrishnam@yahoo.com'
        if email_select != None:
            filename = "{}-{}-{}-{}-{}-{}".format(filters['tahun'], setUjian(
                filters['jenis']), filters['program'], matkul_select, kelas_select, email_select)
        else:
            filename = "{}-{}-{}-{}-{}-NULL".format(filters['tahun'], setUjian(
                filters['jenis']), filters['program'], matkul_select, kelas_select)

        checkDir(matkul['prodi'])

        if os.path.exists('absensi/'+prodi+'/'+filename+'.pdf'):
            os.remove('absensi/'+prodi+'/'+filename+'.pdf')

        dhu_select.send_keys(Keys.ENTER)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        url_select = driver.find_element_by_link_text(
            "Cetak Laporan").get_attribute('href')
        urllib.request.urlretrieve(
            url_select, 'absensi/'+prodi+'/'+filename+'.txt')
        time.sleep(2)

        makePDFOfAbsensiUjian(filename, prodi)
        if os.path.exists('absensi/'+prodi+'/'+filename+'.txt'):
            os.remove('absensi/'+prodi+'/'+filename+'.txt')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
        print('File '+filename+'.pdf berhasil dibuat')
    except NoSuchElementException:
        print('Jadwal {} kelas {} belum diatur'.format(
            matkul['matkul'], matkul['kelas']))


def launchJadwalUjianMenu(driver):
    driver.get("http://siap.poltekpos.ac.id/")
    user_siap = driver.find_element_by_xpath("//input[@name='user_name']")
    user_siap.send_keys(config.username_siap)
    pass_siap = driver.find_element_by_xpath("//input[@name='user_pass']")
    pass_siap.send_keys(config.password_siap)
    login_siap = driver.find_element_by_xpath("//input[@name='login']")
    login_siap.send_keys(Keys.ENTER)
    jadwal_menu = driver.find_element_by_link_text("Jadwal Ujian 1")
    jadwal_menu.click()


def chooseUjian(driver, filters):
    tahun_ujian = Select(
        driver.find_element_by_xpath("//select[@name='tahun']"))
    tahun_ujian.select_by_value(filters['tahun'])
    jenis_ujian = Select(
        driver.find_element_by_xpath("//select[@name='ujian']"))
    jenis_ujian.select_by_value(filters['jenis'])
    program_ujian = Select(
        driver.find_element_by_xpath("//select[@name='prid']"))
    program_ujian.select_by_value(filters['program'])


def getAllUjian(driver, prodis, dosens, filters):
    chooseUjian(driver, filters)
    list_ujian = pd.DataFrame()
    for prodi_selected in prodis:
        if getProdiFromDropdown(driver, prodi_selected):
            tampil_ujian = driver.find_element_by_xpath(
                "//input[@name='Tampilkan']")
            tampil_ujian.send_keys(Keys.ENTER)

            result_generate = genDataFrameUjian(driver, prodi_selected, dosens)
            list_ujian = pd.concat([result_generate, list_ujian])

    return list_ujian


def genDataFrameUjian(driver, prodi_selected, dosen):
    time.sleep(2)
    tabel_select = driver.find_element_by_xpath(
        "//table[@cellpadding='4' and @cellspacing='1']/tbody")
    time.sleep(2)
    index = 1
    dict_data = []
    while True:
        try:
            index += 1
            dosen_select = tabel_select.find_element_by_xpath(
                "//tr[" + str(index) + "]/td[13]").text
            time.sleep(1)
            if dosen_select in dosen:
                matkul_select = tabel_select.find_element_by_xpath(
                    "//tr[" + str(index) + "]/td[8]").text
                time.sleep(1)
                kelas_select = tabel_select.find_element_by_xpath(
                    "//tr[" + str(index) + "]/td[9]").text
                time.sleep(1)
                kode_matkul_select = tabel_select.find_element_by_xpath(
                    "//tr[" + str(index) + "]/td[7]").text
                time.sleep(2)
                kelas_select = int(kelas_select.strip("0"))
                data = {'prodi': prodi_selected, 'matkul': matkul_select,
                        'kelas': kelas_select, 'kode_matkul': kode_matkul_select, 'index': index}
                dict_data.append(data)
            print('.', end='', flush=True)
        except NoSuchElementException:
            break

    df_data = pd.DataFrame(dict_data)
    return df_data


def getProdiFromDropdown(driver, prodi_selected):
    prodi_ujian = Select(
        driver.find_element_by_xpath("//select[@name='prodi']"))
    for prodis in prodi_ujian.options:
        prodi = prodis.text[5:].lower()
        prodi_selected = prodi_selected.lower()
        if prodi_selected == prodi:
            prodi_ujian.select_by_value(prodis.text[:2])
            return True
            break
    print('Prodi {} tidak ada'.format(prodis.text[5:]))
    return False


def makePDFOfAbsensiUjian(filename, prodi):
    pdf = setPdfFormat()
    # Read file txt
    path = 'absensi/{}/{}.txt'.format(prodi, filename)
    file = open(path)
    all_lines = file.readlines()
    # Get length lines file txt
    length_lines = len(all_lines)
    # Make first page
    if length_lines < 61:
        makeCellPdf(pdf, all_lines, 1, length_lines)
    else:
        makeCellPdf(pdf, all_lines, 1, 61)
    # Make second page if exist
    if length_lines > 61:
        makeCellPdf(pdf, all_lines, 63, length_lines)
    pdf.output('absensi/{}/{}.pdf'.format(prodi, filename))


def makeCellPdf(pdf, all, begin, end):
    char_re = removeSpecialChar()
    pdf.add_page()
    for i in range(begin, end):
        pdf.cell(0, 4, txt=char_re.sub('', all[i]), ln=1, border=0)


def setPdfFormat():
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_font('Consolas', '', 'consola.ttf', uni=True)
    pdf.set_font("Consolas", size=7.4)
    return pdf


def removeSpecialChar():
    all_chars = (chr(i) for i in range(sys.maxunicode))
    control_chars = ''.join(
        c for c in all_chars if unicodedata.category(c) == 'Cc')
    control_char_re = re.compile('[%s]' % re.escape(control_chars))
    return control_char_re


def convertKelas(kelas):
    list_kelas = list(string.ascii_lowercase)
    list_nomor = list(range(1, 27))
    dict_kelas = dict(zip(list_nomor, list_kelas))
    for k, v in dict_kelas.items():
        if k == kelas:
            return v.upper()
            break
    return 'Kelas tidak terdaftar'


def checkDir(prodi):
    path = 'absensi/{}'.format(prodi)
    if not os.path.exists(path):
        os.makedirs(path)
        print('Direktori {} telah dibuat'.format(prodi))


def setUjian(ujian):
    ujian = int(ujian)
    if ujian == 1:
        return 'UTS'
    elif ujian == 2:
        return 'UAS'
    else:
        return 'XXX'


def sendEmail(file):
    subject = "Absensi {} Mata Kuliah {} Kelas {} Prodi {}".format(
        file['ujian'], file['matkul'], file['kelas'], file['prodi'])
    body = "Ini file absensi Ujitan UTS Semester Genap oleh iteung ya..., mohon untuk dicek kembali filenya jika ada yang salah mohon untuk diinformasikan ke admin iteung yaa....:) \nAbsensi {} Mata Kuliah {} Kelas {} Prodi {}".format(
        file['ujian'], file['matkul'], file['kelas'], file['prodi'])

    sender_email = config.email_iteung
    receiver_email = file['tujuan']
    password = config.pass_iteung

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email

    message.attach(MIMEText(body, "plain"))

    os.chdir(r'absensi/{}'.format(file['prodi']))
    os.rename(file['nama_lama'], file['nama_baru'])
    filename = file['nama_baru']

    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    os.rename(file['nama_baru'], file['nama_lama'])
    os.chdir(r'../../')
    return True


def sendFileUjian(list_prodi_ujian, filters):
    for prodi_selected in list_prodi_ujian:
        directory = 'absensi/'+prodi_selected
        for filename in os.listdir(directory):
            if filename.endswith(".pdf") and filename.startswith(filters['tahun']+'-'+setUjian(filters['jenis'])+'-'+filters['program']):
                nama_baru = filename[:-4].split("-")
                email_dosen = nama_baru[5]
                if email_dosen == 'NULL':
                    continue
                else:
                    file = {'nama_lama': filename,
                            'prodi': prodi_selected,
                            'nama_baru': nama_baru[0]+'-'+nama_baru[1]+'-'+nama_baru[2]+'-'+nama_baru[3]+'-'+nama_baru[4]+'.pdf',
                            'tujuan': email_dosen,
                            'ujian': nama_baru[1],
                            'matkul': nama_baru[3],
                            'kelas': nama_baru[4],
                            'prodi': prodi_selected}
                    sendEmail(file)
                    print('File '+filename+' berhasil dikirim ke '+email_dosen)

###############################


def sendFileUjianDosen(dosens, filters):
    for dosen in dosens:
        matkul = getMatkulDosen(dosen, filters['tahun'])
        for prodi_selected in matkul['prodi'].unique():
            directory = 'absensi/'+prodi_selected
            for ind in matkul.index:
                for filename in os.listdir(directory):
                    if filename.endswith(".pdf") and filename.startswith(filters['tahun']+'-'+setUjian(filters['jenis'])+'-'+filters['program']):
                        nama_baru = filename[:-4].split("-")
                        email_dosen = nama_baru[5]
                        matkul_select = matkul['nama_matkul'][ind].replace(
                            " ", "_")
                        matkul_select = matkul_select.replace("-", "_")
                        matkul_select = matkul_select.replace("(", "")
                        matkul_select = matkul_select.replace(")", "")

                        if nama_baru[3] == matkul_select and nama_baru[4] == convertKelas(int(matkul['kelas'][ind].strip("0"))):

                            if email_dosen == 'NULL':
                                continue
                            else:
                                file = {'nama_lama': filename,
                                        'prodi': prodi_selected,
                                        'nama_baru': nama_baru[0]+'-'+nama_baru[1]+'-'+nama_baru[2]+'-'+nama_baru[3]+'-'+nama_baru[4]+'.pdf',
                                        'tujuan': email_dosen,
                                        'ujian': nama_baru[1],
                                        'matkul': nama_baru[3],
                                        'kelas': nama_baru[4],
                                        'prodi': prodi_selected}
                                if sendEmail(file):
                                    print('File '+filename +
                                          ' berhasil dikirim ke '+email_dosen)
                                else:
                                    print('File '+filename +
                                          ' gagal dikirim ke '+email_dosen)


def setUjian(ujian):
    ujian = int(ujian)
    if ujian == 1:
        return 'UTS'
    elif ujian == 2:
        return 'UAS'
    else:
        return 'XXX'


def convertKelas(kelas):
    list_kelas = list(string.ascii_lowercase)
    list_nomor = list(range(1, 27))
    dict_kelas = dict(zip(list_nomor, list_kelas))
    for k, v in dict_kelas.items():
        if k == kelas:
            return v.upper()
            break
    return "Kelas tidak terdaftar"
