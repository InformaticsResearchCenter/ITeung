import string, random, qrcode

from fpdf import FPDF
from module import kelas, siap_jadwal, cek_tanda_tangan_bap, approve_bap
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from Crypto.Cipher import AES

from lib import reply, numbers, wa

import smtplib, os, config, subprocess, threading


def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret


def replymsg(driver, data):
    kodedosen = kelas.getKodeDosen(data[0])
    num = numbers.normalize(data[0])
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#EMAIL#', siap_jadwal.getEmailDosen(kodedosen))
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0], num], cwd=config.cwd)
    return wmsg


def run(num):
    makePDFandSend(num)


def checkDir():
    try:
        os.mkdir('bkd/')
    except:
        print('sudah ada..')


def getMkKode(lecturercode):
    db = kelas.dbConnectSiap()
    sql = "select DISTINCT (MKKode) from simak_trn_jadwal where TahunID=20192 and DosenID='{lecturercode}'".format(
        lecturercode=lecturercode)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchall()
        if row is not None:
            ret = row
        else:
            ret = ''
    return ret


def getJadwalID(mkkode, lecturercode):
    db = kelas.dbConnectSiap()
    sql = "select JadwalID from simak_trn_jadwal where TahunID=20192 and MKKode='{mkkode}' and DosenID='{lecturercode}'".format(
        mkkode=mkkode, lecturercode=lecturercode)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if rows is not None:
            return rows
        else:
            return ''


def getPresensiDosen(jadwalid, rangepertemuan1, rangepertemuan2):
    db = kelas.dbConnectSiap()
    sql = f"select PresensiID from simak_trn_presensi_dosen where TahunID=20192 and JadwalID={jadwalid} and Pertemuan > {rangepertemuan1} and Pertemuan < {rangepertemuan2} ORDER BY Pertemuan ASC"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchall()
    return row


def getPresensiMahasiswa(presensiid):
    db = kelas.dbConnectSiap()
    sql = "select MhswID, JenisPresensiID from simak_trn_presensi_mahasiswa where PresensiID={presensiid}".format(
        presensiid=presensiid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchall()
    return row


def getListStudent(jadwalid):
    db = kelas.dbConnectSiap()
    sql = "select j.JadwalID, j.TahunID, j.MKKode, j.Nama, j.DosenID, krs.MhswID from simak_trn_jadwal as j join simak_trn_krs as krs where j.jadwalid = krs.jadwalid and j.tahunid=20192 and j.JadwalID = '{0}'".format(
        jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    return rows


def getTanggalFromPresensiDosen(jadwalid):
    db = kelas.dbConnectSiap()
    sql = "select Tanggal from simak_trn_presensi_dosen WHERE JadwalID={jadwalid} ORDER BY Pertemuan ASC".format(
        jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    return rows


def countTotal(datas):
    total = []
    for data in datas:
        count = 0
        for w in data:
            if w == "v":
                count += 1
        total.append(count)
    return total


def countPertemuan(presensidosens):
    pertemuan = []
    for presensidosen in presensidosens:
        presensimahasiswas = getPresensiMahasiswa(presensidosen[0])
        pertemuandetail = []
        for v in presensimahasiswas:
            if v[1] == "H":
                pertemuandetail.append('v')
            else:
                pertemuandetail.append('-')
        pertemuan.append(pertemuandetail)
    return pertemuan


def getandsetStudentIDandStudentNAME(jadwalid):
    studentid = []
    studentname = []
    jadwalserial = kelas.getJadwalSerial(jadwalid=jadwalid)
    if jadwalserial == '0':
        jadwalid = jadwalid
    else:
        jadwalid = jadwalserial
    studentlists = getListStudent(jadwalid)
    for studentlist in studentlists:
        studentid.append(studentlist[-1])
        studentname.append(kelas.getStudentNameOnly(studentlist[-1]))
    return studentid, studentname


def countNumber(studentid):
    number = []
    count = 1
    for i in studentid:
        number.append((str(count)))
        count += 1
    return number


def tanggalBKDPresensi(data):
    datafix = ['Tanggal:']
    for i in data:
        datafix.append(i[0].strftime("%d/%m"))
    return datafix


def getLecturerMail(lecturercode):
    db = kelas.dbConnectSiap()
    sql = "select Email from simak_mst_dosen where Login='{lecturercode}'".format(
        lecturercode=lecturercode)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    return row[0]


def getKaProdi(prodiid):
    db = kelas.dbConnectSiap()
    sql = "select Nama from simak_mst_pejabat where ProdiID={prodiid} and JenisJabatanID=5".format(
        prodiid=prodiid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    return row[0]


def getNipyKaProdi(prodiid):
    db = kelas.dbConnectSiap()
    sql = f"select NIPY from simak_mst_pejabat where ProdiID={prodiid} and JenisJabatanID=5"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def getNipyDeputi(jabatanid):
    db = kelas.dbConnectSiap()
    sql = f"select NIPY from simak_mst_pejabat where JenisJabatanID={jabatanid}"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def getDosenIDfromNIPY(nipy):
    db = kelas.dbConnectSiap()
    sql = f'select Login from simak_mst_dosen where NIPY="{nipy}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def getDeputiAkademik():
    db = kelas.dbConnectSiap()
    sql = "select Nama from simak_mst_pejabat where JenisJabatanID=9"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    return row[0]


def getBKDMatkul(jadwalid):
    db = kelas.dbConnectSiap()
    sql = f"select Pertemuan, Tanggal, MP, JamMulai, JamSelesai from simak_trn_presensi_dosen where JadwalID={jadwalid} ORDER BY Pertemuan ASC"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if rows is not None:
            return rows
        else:
            return None


def cekMateriByGrouping(lecturercode):
    statusbap=[]
    mkkodes=getMkKode(lecturercode)
    for mkkode in mkkodes:
        jadwalids=getJadwalID(mkkode[0], lecturercode)
        for jadwalid in jadwalids:
            data=[]
            data.append(jadwalid[0])
            data.append(cek_tanda_tangan_bap.cekMateriPerkuliahan(jadwalid[0]))
            statusbap.append(data)
    datastatusgrouping=approve_bap.groupingDataBySecondElement(statusbap)
    if False in datastatusgrouping:
        return False, datastatusgrouping[False]
    else:
        return True, datastatusgrouping[True]


def cekApprovalBAPByGrouping(lecturercode):
    statusbap = []
    mkkodes = getMkKode(lecturercode)
    for mkkode in mkkodes:
        jadwalids = getJadwalID(mkkode[0], lecturercode)
        for jadwalid in jadwalids:
            data=[]
            data.append(jadwalid[0])
            data.append(cek_tanda_tangan_bap.cekStatusBKDKaprodi(jadwalid[0]))
            data.append(cek_tanda_tangan_bap.cekStatusBKDDeputi(jadwalid[0]))
            statusbap.append(data)
    datastatusgrouping = approve_bap.groupingDataBySecondElement(statusbap)
    try:
        makeforcheck=datastatusgrouping[True]
    except:
        makeforcheck = datastatusgrouping[False]
    if len(makeforcheck[0]) == 3:
        if True in datastatusgrouping:
            for datalist in datastatusgrouping[True]:
                if False in datalist:
                    if False in datastatusgrouping:
                        datastatusgrouping[False].append(datalist)
                    else:
                        datastatusgrouping[False]=[datalist]
        if False in datastatusgrouping:
            return False, datastatusgrouping[False]
        else:
            return True, datastatusgrouping[True]
    else:
        if False in datastatusgrouping:
            return False, datastatusgrouping[False]
        else:
            return True, datastatusgrouping[True]


def bulanSwitcher(bulannum):
    switcher = {
        '01': 'Januari',
        '02': 'Februari',
        '03': 'Maret',
        '04': 'April',
        '05': 'Mei',
        '06': 'Juni',
        '07': 'Juli',
        '08': 'Agustus',
        '09': 'September',
        '10': 'Oktober',
        '11': 'November',
        '12': 'Desember',
    }
    return switcher.get(bulannum, "Not Found!")


def sahTanggal():
    return datetime.today().strftime('%d {bulan} %Y'.format(bulan=bulanSwitcher(datetime.today().strftime('%m'))))


def makePDFHeader():
    pdf = FPDF(format='A4', unit='in')
    return pdf


def makePDFFooter(matkuldetails, lecturercode, pdf):
    pdf.output('bkd/' + matkuldetails[1] + '-' + matkuldetails[2] + '-' + getLecturerMail(lecturercode) + '.pdf', 'F')


def getFilePath(email, folder):
    resultpath = []
    devpath = os.getcwd()
    path = '.\\{folder}'.format(folder=folder)
    for root, dirs, files in os.walk(path):
        for i in files:
            if email in i:
                rootpath = os.path.join(root, i)
                resultpath.append(os.path.join(devpath, rootpath))
    return resultpath


def mail(to, subject, text, filenames):
    msg = MIMEMultipart()
    msg['From'] = config.email_iteung
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(text))
    for file in filenames:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file.split('\\')[-1])
        msg.attach(part)
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(config.email_iteung, config.pass_iteung)
    mailServer.sendmail(config.email_iteung, to, msg.as_string())
    mailServer.close()


def checkNone(value):
    if value == None:
        value = "-"
    else:
        pass
    return value


def makePDFBAP(pdf, inner_data, no, date, kodematkul, namamatkul, kelasbap, semester, sks):
    pdf.add_page()
    pdf.set_font('Times', '', 14.0)
    height = 0.3

    y = pdf.get_y()
    pdf.image(f"./bkdqrcode/logo.png", h=height * 4)
    # pdf.cell(1.2, height*4, "", border=1, align='C')

    pdf.set_y(y)
    pdf.set_x(height * 6)
    pdf.set_font('Times', 'B', 10.0)
    pdf.multi_cell(3.9, height * 2, "POLITEKNIK POS INDOENSIA", border=1, align='C')
    pdf.ln(0)
    pdf.set_x(height * 6)
    pdf.multi_cell(3.9, height, "Berita Acara Perkuliahan dan \nAbsensi Perkuliahan", border=1, align='C')
    pdf.set_y(y)
    x = pdf.get_x()

    cover_data = ["Kode/No: " + no, "Tanggal: " + date, "Revisi: -", "Halaman: 1"]
    for i in cover_data:
        pdf.set_x(x + 5.3)
        pdf.cell(2.2, height, i, border=1)
        pdf.ln(height)
    pdf.ln(height)
    pdf.ln(height)
    pdf.cell(3, height, f"Kode Matakuliah/Nama Matakuliah : {kodematkul}/{namamatkul}")
    pdf.ln(height)
    pdf.cell(3, height, f"Kelas : {kelasbap}")
    pdf.ln(height)
    pdf.cell(3, height, f"Semester/SKS : {semester}/{sks}")
    pdf.ln(height)

    for x, rows in enumerate(inner_data):
        if x == 0:
            for i, row in enumerate(rows):
                pdf.set_font('Times', 'B', 10.0)
                if i == 0:
                    pdf.cell(0.9, height, str(row), border=1, align='C')
                elif i == 1:
                    pdf.cell(0.8, height, checkNone(row), border=1, align='C')
                elif i == 2:
                    pdf.cell(4.2, height, checkNone(row), border=1, align='C')
                elif i == 3:
                    pdf.cell(0.8, height, checkNone(row), border=1, align='C')
                elif i == 4:
                    pdf.cell(0.8, height, checkNone(row), border=1, align='C')
        else:
            for i, row in enumerate(rows):
                pdf.set_font('Times', '', 10.0)
                if i == 0:
                    pdf.cell(0.9, height, str(row), border=1, align='C')
                elif i == 1:
                    pdf.cell(0.8, height, checkNone(row), border=1, align='C')
                elif i == 2:
                    pdf.cell(4.2, height, checkNone(row), border=1)
                elif i == 3:
                    pdf.cell(0.8, height, checkNone(row), border=1, align='C')
                elif i == 4:
                    pdf.cell(0.8, height, checkNone(row), border=1, align='C')
        pdf.ln(height)


def makePDFInner(datalist, matkuldetails, lecturername, pdf, pdfpertemuan, lecturerid, statusapprove):
    pdf.add_page()
    pdf.set_font('Times', '', 14.0)
    epw = pdf.w - 2 * pdf.l_margin
    col_width = epw / 6
    prodi = kelas.switcherJurusan(matkuldetails[0])
    kaprodi = getKaProdi(matkuldetails[0].split('.')[1])
    deputiakademik = getDeputiAkademik()
    kodenmatkul = matkuldetails[1] + " / " + matkuldetails[2]
    waktu = str(matkuldetails[3])[:-3] + " - " + str(matkuldetails[4])[:-3]
    ruang = matkuldetails[5]
    kelasid = kelas.toKelas(matkuldetails[6])
    prodiqrcode='bkdqrcode/whiteimage.png'
    deputiqrcode='bkdqrcode/whiteimage.png'
    if statusapprove[0] == 'true':
        prodiqrcode=f"bkdqrcode/kaprodiqrcode{lecturerid}.png"
    if statusapprove[1] == 'true':
        deputiqrcode=f"bkdqrcode/deputiqrcode{lecturerid}.png"
    data = [('No.', 'NPM', 'Nama', pdfpertemuan[0], pdfpertemuan[1], pdfpertemuan[2], pdfpertemuan[3], pdfpertemuan[4],
             pdfpertemuan[5], pdfpertemuan[6], 'Total')]
    for i in datalist:
        data.append(i)
    header_data = [['Program Studi', ':', prodi, 'Jadwal', ': ', waktu],
                   ['Kode / Mata Kuliah', ': ', kodenmatkul, 'Ruang', ': ', ruang],
                   ['Pengajar', ': ', lecturername, 'Kelas', ': ', kelasid]]
    footer_data = [['Disahkan Tanggal: {sah}'.format(sah=sahTanggal()), ],
                   [['Pengajar', f"bkdqrcode/dosenqrcode{lecturerid}.png", lecturername],
                    ['Ketua Prodi', prodiqrcode, kaprodi],
                    ['Deputi Akademik', deputiqrcode, deputiakademik]]
                   ]
    th = pdf.font_size
    # header data
    for row in header_data:
        for i, datum in enumerate(row):
            pdf.set_font('Times', '', 10.0)
            # columns
            if i == 0:
                col_width = epw / 6
            elif i == 1 or i == 4:
                col_width = epw / 25
            elif i == 2:
                col_width = epw / 1.95
            elif i == 3:
                col_width = epw / 9
            elif i == 5:
                col_width = epw / 8
            # condition columns
            if datum[:2].lower() == 'd4' or datum[:2].lower() == 'd3':
                pdf.set_font('Times', 'B', 10.0)
            elif 'program studi' == datum.lower():
                pdf.set_font('Times', 'B', 10.0)
            elif datum == ':' and 'program studi' == row[0].lower():
                pdf.set_font('Times', 'B', 10.0)
            pdf.cell(col_width, th, str(datum), border=0)
        pdf.ln(th)
    pdf.ln(th)
    # inner data
    no_width = epw / 25
    npm_width = epw / 12
    nama_width = epw / 2.65
    pertemuan_width = epw / 16
    total_width = epw / 16

    for i, row in enumerate(data):
        # last row
        if i == len(data) - 1:
            if pdfpertemuan[0] == '1':
                startpertemuan = 1
                endpertemuan = 7
            else:
                startpertemuan = 8
                endpertemuan = 14
            for j, datum in enumerate(row):
                if j == 0:
                    col_width = no_width + npm_width + nama_width
                    pdf.cell(col_width, th, str(datum), border=1, align='R')
                # tanggal
                elif j in range(startpertemuan, endpertemuan):
                    col_width = pertemuan_width
                    pdf.cell(col_width, th, str(datum), border=1)
                # total
                elif j == endpertemuan:
                    col_width = total_width
                    pdf.cell(col_width, th, str(datum), border=1)
        # not last row
        else:
            for j, datum in enumerate(row):
                # no
                if j == 0:
                    col_width = no_width
                # npm
                elif j == 1:
                    col_width = npm_width
                # nama
                elif j == 2:
                    col_width = nama_width
                # pertemuan
                elif j in range(3, 10):
                    col_width = pertemuan_width
                # total
                elif j == 10:
                    col_width = total_width

                if i == 0:
                    pdf.set_font('Times', 'B', 10.0)
                    pdf.cell(col_width, th, str(datum), border=1, align='C')
                else:
                    pdf.set_font('Times', '', 10.0)
                    pdf.cell(col_width, th, str(datum), border=1)
        pdf.ln(th)
    # pdf.cell(10, th, "Keterangan:")
    # pdf.ln(th)
    # pdf.cell(10, th, "- Hadir (v)")
    # pdf.ln(th)
    # pdf.cell(10, th, "- Tidak Hadir (-)")
    # pdf.ln(th)
    pdf.ln(th)
    # footer
    for i, row in enumerate(footer_data):
        x = 0
        y = 0
        for j, datum in enumerate(row):
            if i == 0:
                col_width = (epw / 6) + (epw / 25) + (epw / 1.95) + (epw / 8) + (epw / 9)
                pdf.set_font('Times', '', 10.0)
                pdf.cell(col_width, th, str(datum))
                # pdf.ln(th)
            else:
                col_width = ((epw / 6) + (epw / 25 * 2) +
                             (epw / 1.94) + (epw / 8) + (epw / 9)) / 3
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.set_font('Times', '', 10.0)
                # hapus kalo mau samain lebar kolom ttdnya
                if j == 2:
                    col_width = col_width - 0.5
                    img_x = x + (col_width / 8.5)
                else:
                    col_width = col_width + 0.259
                    img_x = x + (col_width / 4.5)
                ###
                for h, wkwk in enumerate(datum):
                    pdf.set_x(x)
                    if h == 1:
                        pdf.image(wkwk, x=img_x, w=1.5)
                    else:
                        pdf.cell(col_width, th, wkwk, align='C')
                    pdf.ln(th)
                pdf.set_xy(x + col_width, y)
        pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    pdf.ln(th)
    # pdf.ln(th)
    # pdf.ln(th)
    pdf.cell(40, th,
             "Dokumen ini telah ditandatangani secara elektronik dan diterbitkan oleh ITeung (IT Service Utility Integrated) System")


def randomString(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def makeLinkVerifiy(kodedosen):
    datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
    tanggal = datenow.split('-')[0]
    bulan = datenow.split('-')[1]
    tahun = datenow.split('-')[2]
    jam = datetime.now().time().strftime('%H')
    menit = datetime.now().time().strftime('%M')
    detik = datetime.now().time().strftime('%S')
    nomordokumen=f'ITeung/{tanggal}/{bulan}/{tahun}'
    jenisdokumen='Berita Acara Perkuliahan dan Absensi Perkuliahan'
    module_name='bkd'
    data = f'{module_name};{kodedosen};{tanggal};{bulan};{tahun};{jam};{menit};{detik};{nomordokumen};{jenisdokumen};'
    makeit112 = f'{data}{randomString(112 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit112.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link


def makeQrcodeLinkVerifySign(link, status, kodedosen):
    if status == 'dosen':
        img = qrcode.make(link)
        img.save(f'./bkdqrcode/dosenqrcode{kodedosen}.png')
    elif status == 'kaprodi':
        img = qrcode.make(link)
        img.save(f'./bkdqrcode/kaprodiqrcode{kodedosen}.png')
    else:
        img = qrcode.make(link)
        img.save(f'./bkdqrcode/deputiqrcode{kodedosen}.png')


def checkDirQrcode():
    try:
        os.mkdir('bkdqrcode/')
    except:
        print('sudah ada..')


def getDosenHomebase(phonenumber):
    num = numbers.normalize(phonenumber)
    db = kelas.dbConnectSiap()
    sql = f'select Homebase from simak_mst_dosen WHERE Handphone="{num}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def countSemester(jadwalid):
    jadwalserial = kelas.getJadwalSerial(jadwalid=jadwalid)
    if jadwalserial == '0':
        jadwalid = jadwalid
    else:
        jadwalid = jadwalserial
    data = kelas.pesertaAbsensi(jadwalid)
    middleDataLength = len(data) // 2
    npm = data[middleDataLength][-1]
    tahunAngkatan = 2000 + int(npm[1:3])
    tahunAjaran = '20192'
    semester = (int(tahunAjaran[:-1]) - tahunAngkatan) * 2 + int(tahunAjaran[-1])
    return semester


def getSks(jadwalid):
    db = kelas.dbConnectSiap()
    sql = f'select SKS from simak_trn_jadwal where JadwalID={jadwalid}'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def cekStatusApproveBAP(jadwalid):
    db=kelas.dbConnectSiap()
    sql=f"select BKD_Prodi, BKD_Deputi from simak_trn_jadwal where JadwalID={jadwalid}"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        return row


def getRencanaKehadiran(jadwalid):
    db=kelas.dbConnectSiap()
    sql=f"select RencanaKehadiran from simak_trn_jadwal where JadwalID={jadwalid}"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return row[0]
        else:
            return None


def makePDFandSend(num):
    checkDir()
    lecturercode = kelas.getKodeDosen(num)
    lecturername = kelas.getNamaDosen(lecturercode)
    dosenHomeBase = getDosenHomebase(num)
    checkDirQrcode()
    # generate dosen barcode
    link = makeLinkVerifiy(lecturercode)
    makeQrcodeLinkVerifySign(link, 'dosen', lecturercode)

    # generate kaprodi barcode
    kaprodinipycode = getNipyKaProdi(dosenHomeBase)
    kaprodiDosenID = getDosenIDfromNIPY(kaprodinipycode)
    link = makeLinkVerifiy(kaprodiDosenID)
    makeQrcodeLinkVerifySign(link, 'kaprodi', lecturercode)

    # generate deputi barcode
    deputinipycode = getNipyDeputi(9)
    deputiDosenID = getDosenIDfromNIPY(deputinipycode)
    link = makeLinkVerifiy(deputiDosenID)
    makeQrcodeLinkVerifySign(link, 'deputi', lecturercode)

    pertemuankurang=[]

    mkkodes = getMkKode(lecturercode)
    for mkkode in mkkodes:
        jadwalids = getJadwalID(mkkode[0], lecturercode)
        try:
            pdf = makePDFHeader()
            matkuldetailsfix = None
            for jadwalid in jadwalids:
                if getRencanaKehadiran(jadwalid[0]) == '0':
                    print('rencana kehadiran kurang dari 0')
                else:
                    print(jadwalid)
                    matkuldetails = kelas.getMkDetails(jadwalid[0])
                    datamatkulbap = getBKDMatkul(jadwalid[0])
                    semester = countSemester(jadwalid[0])
                    sks = getSks(jadwalid[0])
                    nama_kelas = kelas.toKelas(matkuldetails[6])
                    kode_matkul = matkuldetails[1]
                    nama_matkul = matkuldetails[2]
                    datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
                    tanggalbap = datenow.split('-')[0]
                    bulanbap = datenow.split('-')[1]
                    tahunbap = datenow.split('-')[2]
                    kode_nomor = f'ITeung/{tanggalbap}/{bulanbap}/{tahunbap}'
                    tanggalpdfbap = f'{tanggalbap} {bulanSwitcher(bulanbap)} {tahunbap}'
                    datafixbap = []
                    datawkwkbap = ['Pertemuan', 'Tanggal', 'Materi Perkuliahan', 'Jam Mulai', 'Jam Selesai']
                    datafixbap.append(datawkwkbap)
                    for i in datamatkulbap:
                        matkuldatalist = []
                        matkuldatalist.append(i[0])
                        matkuldatalist.append(i[1].strftime('%d-%m-%Y'))
                        matkuldatalist.append(i[2])
                        matkuldatalist.append(str(i[3]))
                        matkuldatalist.append(str(i[4]))
                        datafixbap.append(matkuldatalist)
                    makePDFBAP(pdf, datafixbap, kode_nomor, tanggalpdfbap, kode_matkul, nama_matkul, nama_kelas, semester,
                               sks)
                    studentid, studentname = getandsetStudentIDandStudentNAME(jadwalid[0])
                    presensidosens1 = getPresensiDosen(jadwalid[0], 0, 8)
                    presensidosens2 = getPresensiDosen(jadwalid[0], 7, 15)
                    for i in range(2):
                        if i == 0:
                            pertemuan = countPertemuan(presensidosens1)
                            pdfpertemuan = ['1', '2', '3', '4', '5', '6', '7']
                        else:
                            pertemuan = countPertemuan(presensidosens2)
                            pdfpertemuan = ['8', '9', '10', '11', '12', '13', '14']
                        if len(pertemuan) < 7:
                            rencanakehadiran=getRencanaKehadiran(jadwalid[0])
                            kehadirannormal=14
                            selisihkehadiran=kehadirannormal-int(rencanakehadiran)
                            for i in range(selisihkehadiran):
                                jumlahmahasiswa=len(pertemuan[0])
                                data_pertemuan=[]
                                for j in range(jumlahmahasiswa):
                                    data_pertemuan.append('-')
                                pertemuan.append(data_pertemuan)
                        print(pertemuan)
                        datas = list(zip(pertemuan[0], pertemuan[1], pertemuan[2], pertemuan[3], pertemuan[4], pertemuan[5],
                                         pertemuan[6]))
                        total = countTotal(datas)
                        datas = list(
                            zip(studentid, studentname, pertemuan[0], pertemuan[1], pertemuan[2], pertemuan[3],
                                pertemuan[4],
                                pertemuan[5], pertemuan[6]))
                        number = countNumber(studentid)
                        datapdf = list(
                            zip(number, studentid, studentname, pertemuan[0], pertemuan[1], pertemuan[2], pertemuan[3],
                                pertemuan[4], pertemuan[5], pertemuan[6], total))
                        tanggal = tanggalBKDPresensi(getTanggalFromPresensiDosen(jadwalid[0]))
                        datapdf.append(tanggal)
                        statusapprove=cekStatusApproveBAP(jadwalid[0])
                        makePDFInner(datapdf, matkuldetails, lecturername, pdf, pdfpertemuan, lecturercode, statusapprove)
                        matkuldetailsfix = matkuldetails
            makePDFFooter(matkuldetailsfix, lecturercode, pdf)
        except Exception as e:
            print(str(e))
            print(f'pertemuan kurang dari {config.kehadiran}')
            pertemuankurang.append(jadwalid[0])
    cekkurangmateri = cekMateriByGrouping(lecturercode)
    cekkurangapproval = cekApprovalBAPByGrouping(lecturercode)
    if cekkurangmateri[0] == False or cekkurangapproval[0] == False:
        msgkurang=''
        if len(pertemuankurang) > 0:
            msgkurang+=f'hai haiii, kamu yang request BAP yaaa?{config.whatsapp_api_lineBreak}wahhh ada yang kurang nih pertemuannya ini Jadwal ID nya yaaa:'
            for i in pertemuankurang:
                kelasdetails=kelas.getMkDetails(i)
                msgkurang+=f'{config.whatsapp_api_lineBreak}{i} | {kelasdetails[2]} | {kelas.toKelas(kelasdetails[-1])}'
        if cekkurangmateri[0] == False:
            kurangmateri=''
            for i in cekkurangmateri[1]:
                kelasdetails = kelas.getMkDetails(i[0])
                kurangmateri+=f'{config.whatsapp_api_lineBreak}{i[0]} | {kelasdetails[2]} | {kelas.toKelas(kelasdetails[-1])}'
            msgkurang+=f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}aduhhhh ternyata ada yang kurang nih ketika kamu request BAP, matkul dengan Jadwal ID:{kurangmateri}{config.whatsapp_api_lineBreak}materinya kurang nihhhhh, tolong lengkapi lagiii yaaa caranya ketik ini *iteung panduan dosen kelas online* dan baca panduan nomor 13 dan 14'
        if cekkurangapproval[0] == False:
            kurangapprove = ''
            for i in cekkurangapproval[1]:
                siapayangkurang = ''
                kelasdetails = kelas.getMkDetails(i[0])
                if i[1] == False:
                    siapayangkurang += ' | KAPRODI'
                if i[2] == False:
                    siapayangkurang += ' | DEPUTI AKADEMIK'
                kurangapprove += f'{config.whatsapp_api_lineBreak}{i[0]} | {kelasdetails[2]} | {kelas.toKelas(kelasdetails[-1])} {siapayangkurang}'
            msgkurang += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}wuowwww ada yang kurang nih ketika kamu request BAP, status approval nya masih belum di ACC nih dengan Jadwal ID:{kurangapprove}{config.whatsapp_api_lineBreak}'
        wa.setOutbox(numbers.normalize(num), msgkurang)
    else:
        mail(getLecturerMail(lecturercode),
             f'Halooooo, {config.bot_name} ngirim file nich....',
             f'ini ya file Absensi BKD yang Bapak/Ibu minta silahkan di cek... ehee....',
             getFilePath(getLecturerMail(lecturercode), 'bkd'))

def verifyDigitalSign(resultpasscode):
    kodedosen = resultpasscode.split(';')[1]
    tglttd = resultpasscode.split(';')[2]
    blnttd = resultpasscode.split(';')[3]
    thnttd = resultpasscode.split(';')[4]
    jamttd = resultpasscode.split(';')[5]
    mntttd = resultpasscode.split(';')[6]
    dtkttd = resultpasscode.split(';')[7]
    nmrsrt = resultpasscode.split(';')[8]
    jnsdkm = resultpasscode.split(';')[9]
    datadosen = kelas.getAllDataDosens(kodedosen)
    penerbitantandatangan = f'{jamttd}:{mntttd}:{dtkttd} {tglttd} {bulanSwitcher(blnttd)} {thnttd}'
    namadosen = kelas.getNamaDosen(kodedosen)
    datalahirdosen = datadosen[7].strftime('%d-%m-%Y')
    tahunlahirdosen = datalahirdosen.split('-')[2]
    bulanlahirdosen = bulanSwitcher(datalahirdosen.split('-')[1])
    tanggallahirdosen = datalahirdosen.split('-')[0]
    datalahirdosen = tanggallahirdosen + ' ' + bulanlahirdosen + ' ' + tahunlahirdosen
    msgreply = f'Ini yaaa data yang Akang/Teteh minta\n\nKode Dosen: {kodedosen}\nNama Dosen: {namadosen}\nNIDN: {datadosen[2]}\nTempat/Tgl Lahir: {datadosen[6]}/{datalahirdosen}\nHandphone: {datadosen[12]}\nE-mail: {datadosen[13]}\n\nJenis Dokumen: {jnsdkm}\nNomor Dokumen: {nmrsrt}\nPenerbitan Tanda Tangan: {penerbitantandatangan}'
    return msgreply