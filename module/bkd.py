from fpdf import FPDF
from module import kelas, siap_jadwal
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from lib import wa, reply

import smtplib, os, config, subprocess, threading

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    kodedosen=kelas.getKodeDosen(data[0])
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#EMAIL#', siap_jadwal.getEmailDosen(kodedosen))
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0], data], cwd=config.cwd)

def run(data):
    makePDFandSend(data)

def checkDir():
    path = '../bkd'
    if not os.path.exists(path):
        t = threading.Thread(target=os.makedirs, args=(path,))
        t.start()
        t.join()
        print('Direktori bkd telah dibuat')

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


def getPresensiDosen(jadwalid):
    db = kelas.dbConnectSiap()
    sql = "select PresensiID from simak_trn_presensi_dosen where TahunID=20192 and JadwalID={jadwalid} and Pertemuan > 0 and Pertemuan < 8".format(
        jadwalid=jadwalid)
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
    sql = "select Tanggal from simak_trn_presensi_dosen WHERE JadwalID={jadwalid}".format(
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


def getDeputiAkademik():
    db = kelas.dbConnectSiap()
    sql = "select Nama from simak_mst_pejabat where JenisJabatanID=9"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    return row[0]


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
    pdf.output('BKD/'+matkuldetails[1] + '-' + matkuldetails[2] + '-' + getLecturerMail(lecturercode) + '.pdf', 'F')

def getFilePath(email, folder):
    resultpath=[]
    devpath = os.getcwd()
    path='.\\{folder}'.format(folder=folder)
    for root, dirs, files in os.walk(path):
        for i in files:
            if email in i:
                rootpath=os.path.join(root, i)
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

def makePDFInner(datalist, matkuldetails, lecturername, pdf):
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
    data = [('No.', 'NPM', 'Nama', '1', '2', '3', '4', '5', '6', '7', 'Total')]
    for i in datalist:
        data.append(i)
    header_data = [['Program Studi', ':', prodi, 'Jadwal', ': ', waktu],
                   ['Kode / Mata Kuliah', ': ', kodenmatkul, 'Ruang', ': ', ruang],
                   ['Pengajar', ': ', lecturername, 'Kelas', ': ', kelasid]]
    footer_data = [['Disahkan Tanggal: {sah}'.format(sah=sahTanggal()), ],
                   ['Pengajar,\n\n\n{lecturername}'.format(lecturername=lecturername), 'Ketua Prodi,\n\n\n{kaprodi}'.format(kaprodi=kaprodi),
                       'Deputi Akademik,\n\n\n{deputiakademik}'.format(deputiakademik=deputiakademik)]
                   ]
    th = pdf.font_size
    # header data
    for row in header_data:
        for i, datum in enumerate(row):
            pdf.set_font('Times', '', 10.0)
            # columns
            if i == 0:
                col_width = epw/6
            elif i == 1 or i == 4:
                col_width = epw/25
            elif i == 2:
                col_width = epw/1.95
            elif i == 3:
                col_width = epw/9
            elif i == 5:
                col_width = epw/8
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
    no_width = epw/25
    npm_width = epw/12
    nama_width = epw/2.65
    pertemuan_width = epw/16
    total_width = epw/16

    for i, row in enumerate(data):
        # last row
        if i == len(data)-1:
            for j, datum in enumerate(row):
                if j == 0:
                    col_width = no_width + npm_width + nama_width
                    pdf.cell(col_width, th, str(datum), border=1, align='R')
                # tanggal
                elif j in range(1, 8):
                    col_width = pertemuan_width
                    pdf.cell(col_width, th, str(datum), border=1)
                # total
                elif j == 8:
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
    pdf.ln(th)
    # footer
    for i, row in enumerate(footer_data):
        x = 0
        y = 0
        for j, datum in enumerate(row):
            if i == 0:
                col_width = (epw/6) + (epw/25) + (epw/1.95) + (epw/8) + (epw/9)
                pdf.set_font('Times', '', 10.0)
                pdf.cell(col_width, th, str(datum))
            else:
                col_width = ((epw/6) + (epw/25*2) +
                             (epw/1.94) + (epw/8) + (epw/9)) / 3
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.set_font('Times', '', 10.0)
                # hapus kalo mau samain lebar kolom ttdnya
                if j == 2:
                    col_width = col_width - 0.5
                else:
                    col_width = col_width + 0.259
                ###
                pdf.multi_cell(col_width, th, datum, border=1, align='C')
                pdf.set_xy(x+col_width, y)
        pdf.ln(th)

def makePDFandSend(data):
    checkDir()
    num = data[0]
    lecturercode = kelas.getKodeDosen(num)
    lecturername = kelas.getNamaDosen(lecturercode)
    mkkodes = getMkKode(lecturercode)
    for mkkode in mkkodes:
        jadwalids = getJadwalID(mkkode[0], lecturercode)
        try:
            pdf = makePDFHeader()
            matkuldetailsfix = None
            for jadwalid in jadwalids:
                studentid, studentname = getandsetStudentIDandStudentNAME(jadwalid[0])
                presensidosens = getPresensiDosen(jadwalid[0])
                pertemuan = countPertemuan(presensidosens)
                datas = list(zip(pertemuan[0], pertemuan[1], pertemuan[2], pertemuan[3], pertemuan[4], pertemuan[5],
                                 pertemuan[6]))
                total = countTotal(datas)
                datas = list(
                    zip(studentid, studentname, pertemuan[0], pertemuan[1], pertemuan[2], pertemuan[3], pertemuan[4],
                        pertemuan[5], pertemuan[6]))
                number = countNumber(studentid)
                matkuldetails = kelas.getMkDetails(jadwalid[0])
                datapdf = list(
                    zip(number, studentid, studentname, pertemuan[0], pertemuan[1], pertemuan[2], pertemuan[3],
                        pertemuan[4], pertemuan[5], pertemuan[6], total))
                tanggal = tanggalBKDPresensi(getTanggalFromPresensiDosen(jadwalid[0]))
                datapdf.append(tanggal)
                makePDFInner(datapdf, matkuldetails, lecturername, pdf)
                matkuldetailsfix = matkuldetails
            makePDFFooter(matkuldetailsfix, lecturercode, pdf)
        except Exception as e:
            print(str(e))
            print('pertemuan kurang dari 7')
    mail(getLecturerMail(lecturercode), 'Halooooo, #BOTNAME# ngirim file nich....'.replace('#BOTNAME#', config.bot_name),
         'ini ya file Absensi BKD yang Bapak/Ibu minta silahkan di cek... ehee....',
         getFilePath(getLecturerMail(lecturercode), 'bkd'))