from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
import datetime, os, time
from os import path

from module import kelas, bkd
from lib import wa, reply, message, numbers
import config
import pandas as pd
import subprocess

from Crypto.Cipher import AES

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

import qrcode

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) != None or kelas.getKodeDosen(data[0]) != '':
        ret = True
    else:
        ret = False
    return ret

def replymsg(driver, data):
    msgreply = ""    
    if kelas.cekSiap():    
        num = numbers.normalize(data[0])        
        try:
            if getMahasiswa(num):
                npm, prodi, email = getMahasiswa(num)
                
                wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                wmsg = wmsg.replace('#EMAIL#', email)
                wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
                wa .typeAndSendMessage(driver, wmsg)
                prodis = convertProdi(prodi)
                if checkSKPIProdiFile(prodis[0]):
                    dfStatus = pd.read_excel(f"./skpi/list-skpi/list-wisudawan.xlsx")
                    # print(dfStatus)
                    status = dfStatus.loc[dfStatus["NPM"] == int(npm)].values.tolist()[0]
                    # print(status)
                    # print(status[2] != '-', status[3] != '-')
                    if status[2] != '-' and status[3] != '-':
                        data = f"{'mahasiswa'};{npm};{email};{prodi}"
                        # print(data)
                        subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                        msgreply = ""
                    else:
                        msgreply = "Minta approve dulu sana"
                        if status[2] == '-':
                            msgreply += " ke *kaprodi*"
                        if status[3] == '-':
                            msgreply += " sama *wadir 1*"
                        msgreply += " baru bisa minta SKLnya... xixixixi"
                else:   
                    msgreply = "Belum ada nih list data SKLnya..."
                    
                
            else:
                msgreply = f"Ikan teri pake saos.. anda siapa bos..\nSebenarnya ada beberapa kemungkinan, pertama kamu bukan mahasiswa yg udh wisuda.. apalagi ya.. kyknya itu aja.."
            
        except Exception as e:
            msgreply = f'Ikan hiu makan tomat.. ada error mat... {str(e)}'
        
    else:
        wa.typeAndSendMessage(driver, 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....')
    return msgreply

def run(data):
    data = data.split(';')
    kode = data[1]
    email = data[2]
    print(data)
    if data[0] == "mahasiswa":
        prodi = convertProdi(data[3])
        mainPages(kode, prodi, email)
    print("Udahan")

def mainPages(npm = None, prodi = None, email=None):
    checkSKPIDir(prodi[0])
    fileName = f"./skpi/skpi-{prodi[0]}/{giveFileName(npm, prodi[0])}"
    doc = SimpleDocTemplate(fileName,
                            pagesize=A4,
                            rightMargin=2.5*cm,
                            leftMargin=2.5*cm,
                            topMargin=0*cm,
                            bottomMargin=0*cm)
    contain=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Times', fontSize=12))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontName='Times'))
    
    year = datetime.datetime.now().year
    
    df = pd.read_excel(f"./skpi/list-skpi/{prodi[0]}-{year}.xlsx")
    listColumn = ["Nama Lengkap", "Tempat, Tanggal Lahir", "NPM", "Tahun Lulus", "IPK", "Predikat Kelulusan", "Judul Skripsi"]
    df = df.loc[:, listColumn]
    
    dfAkreditasi = pd.read_csv(f"./skpi/akreditasi.csv")
    akreditasiInstitusi = dfAkreditasi.loc[dfAkreditasi["institusi"] == "poltek"].values.tolist()[0]
    akreInstitusi = f'{akreditasiInstitusi[1]} "Terakreditasi {akreditasiInstitusi[2]}"'
    print('Boom')
    dfNomor = pd.read_excel(f"./skpi/list-skpi/list-wisudawan.xlsx")
    print(dfNomor)
    print('Baam')
    nikWadirI, wadirI = getWadirI()
    
    if npm:
        akreditasiProdi = dfAkreditasi.loc[dfAkreditasi["institusi"] == prodi[0]].values.tolist()[0]
        akreProdi = f'{akreditasiProdi[1]} "Terakreditasi {akreditasiProdi[2]}"'
        
        listTTD = []
        
        print(prodi[2])
        nikKaprodi, kaprodi = getKaprodi(prodi[2])
        
        kodeWadirI = getKodeDosen(nikWadirI)
        kodeKaprodi = getKodeDosen(nikKaprodi)
        
        link = makeLinkVerifiy(kodeWadirI, npm, 'wadirI')
        filepathWadirI = makeQrcodeLinkVerifySign(link, kodeWadirI, npm, prodi[0], 'wadirI')
        listTTD.append(filepathWadirI)
        
        link = makeLinkVerifiy(kodeKaprodi, npm, 'kaprodi')
        filepathKaprodi = makeQrcodeLinkVerifySign(link, kodeKaprodi, npm, prodi[0], 'kaprodi')
        listTTD.append(filepathKaprodi)
        
        mahasiswa = df.loc[df["NPM"] == int(npm)].values.tolist()[0]
        tahun = f'{int(mahasiswa[3])-1}/{int(mahasiswa[3])}'
        print(dfNomor.loc[dfNomor["NPM"] == int(npm)])
        nomorA = dfNomor.loc[dfNomor["NPM"] == int(npm)].values.tolist()[0][0]
        
        tanggalBerlaku = "23 Oktober 2020"
        now = datetime.datetime.now()
        tanggalSurat = f"{now.day} {convertMonth(str(now.month))} {now.year}"
        
        createAPage(contain, styles, nomorA, "IX", "2020", akreInstitusi, akreProdi, tahun, "18 September 2020", tanggalSurat, wadirI, nikWadirI, mahasiswa[0], mahasiswa[1], mahasiswa[2], prodi[1], prodi[0][:2], getSemester(prodi[0][:2]), mahasiswa[4], mahasiswa[5], mahasiswa[6], kaprodi, nikKaprodi, listTTD, tanggalBerlaku)
    #     contain.append(PageBreak())

    doc.build(contain)
    
    sendEmail(email, giveFileName(npm, prodi[0]), f"./skpi/skpi-{prodi[0]}/", npm)

def convertMonth(month):
    print(month)
    months = {
        '1': 'Januari',
        '2': 'Februari',
        '3': 'Maret',
        '4': 'April',
        '5': 'Mei',
        '6': 'Juni',
        '7': 'Juli',
        '8': 'Agustus',
        '9': 'September',
        '10': 'Oktober',
        '11': 'November',
        '12': 'Desember',
    }
    return months.get(month, "XXX")

def createAPage(contain, styles, nomorA, nomorB, nomorC, akreInstitusi, akreProdi, tahun, tanggalYudisium, tanggalSurat, wadirI, nikWadirI, nama, ttl, npm, prodi, jenjang, semester, ipk, predikat, judul, kaprodi, nikKaprodi, listTTD, tanggalBerlaku):
    
    contain.append(Image(f'./skpi/header.png', 19*cm, 2.5*cm))
    contain.append(Spacer(1, 0*cm))
    
    ptext = '<font size="15"><b>SURAT KETERANGAN LULUS</b></font>'
    contain.append(Paragraph(ptext, styles["Center"]))
    contain.append(Spacer(1, .2*cm))

    ptext = f'<font size="12">Nomor: 225-{nomorA}/WD-I/PPI/{nomorB}/{nomorC}</font>'
    contain.append(Paragraph(ptext, styles["Center"]))
    contain.append(Spacer(1, .4*cm))

    ptext = '<font size="12">Direktur Politeknik Pos Indonesia menerangkan bahwa:</font>'
    contain.append(Paragraph(ptext, styles["Justify"]))
    contain.append(Spacer(1, .3*cm))

    data = [['Nama', ':', nama],
        ['Tempat/Tgl. Lahir', ':', ttl],
        ['NPM', ':', npm],
        ['Program Studi', ':', prodi],
        ['Jenjang', ':', jenjang.upper()],
        ['Akreditasi Institusi', ':', akreInstitusi],
        ['Akreditasi Program Studi', ':', akreProdi],
    ]

    table = Table(data, [5*cm, .5*cm, 10.5*cm], 7*[.6*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .3*cm))

    ptext = '<font size="12">Telah dinyatakan <b>LULUS</b> berdasarkan keputusan rapat Yudisium pada:</font>'
    contain.append(Paragraph(ptext, styles["Justify"]))
    contain.append(Spacer(1, .3*cm))
    
    styleWrap = styles["BodyText"]
    styleWrap.alignment = TA_JUSTIFY
    styleWrap.fontName = 'Times'
    styleWrap.fontSize = 12
    styleWrap.leading = 14
    
    data = [['Semester', ':', 'Genap'],
    ['Tahun Akademik', ':', tahun],
    ['Tanggal Yudisium', ':', tanggalYudisium],
    ['IPK', ':', ipk],
    ['Predikat Kelulusan', ':', predikat],
    ['Judul Tugas Akhir/Skripsi', ':', Paragraph(judul, styleWrap)],
    ]

    table = Table(data, [5*cm, .5*cm, 10.5*cm], [.6*cm, .6*cm, .6*cm, .6*cm, .6*cm, 3*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),        
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, 0*cm))

    ptext = f'<font size="12">Surat keterangan ini diberikan sebagai pengganti Ijazah Asli yang masih dalam proses penyelesaian dan berlaku sampai dengan tanggal {tanggalBerlaku}.</font>'
    contain.append(Paragraph(ptext, styles["Justify"]))
    contain.append(Spacer(1, .4*cm))

    ptext = '<font size="12">Demikian surat keterangan ini dibuat, agar dapat dipergunakan sebagaimana mestinya.</font>'
    contain.append(Paragraph(ptext, styles["Justify"]))
    contain.append(Spacer(1, .4*cm))

    data = [['Diterbitkan', ':', 'Bandung'],
    ['Pada tanggal', ':', tanggalSurat],
    ]

    table = Table(data, [2.5*cm, .23*cm, 3.3*cm], 2*[.6*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('LEFTPADDING',(0,0),(-1,-1), 0),
    ]))

    data = [['',table],
    [Paragraph('<font size="12"><b>Wakil Direktur I</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Kepala Program Studi</b></font>', styles["Center"])],
    [Paragraph('<font size="12"><b>Bidang Akademik</b></font>', styles["Center"]), Paragraph(f'<font size="12"><b>{prodi}</b></font>', styles["Center"])],
    [Image(listTTD[0], 3.8 * cm, 3.8 * cm), Image(listTTD[1], 3.8 * cm, 3.8 * cm)],
    [Paragraph(f'<font size="12"><b>{wadirI}</b></font>', styles["Center"]), Paragraph(f'<font size="12"><b>{kaprodi}</b></font>', styles["Center"])],
    [Paragraph(f'<font size="12"><b>NIK: {nikWadirI}</b></font>', styles["Center"]), Paragraph(f'<font size="12"><b>NIK: {nikKaprodi}</b></font>', styles["Center"])],
    ]

    table = Table(data, [7*cm, 8.5*cm], [1.7*cm, .5*cm, .5*cm, 3.8*cm, .5*cm, .5*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        # ('LEFTPADDING',(0,0),(-1,-1), 0),
        # ('RIGHTPADDING',(0,0),(-1,-1), 0),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        # ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        # ('BOX', (0,0), (-1,-1), 1, colors.black),        
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .3*cm))
    
    ptext = '<font size="10">*Dokumen ini sah diterbitkan dan telah ditandatangani secara elektronik menggunakan sistem ITeung (IT Service Utility Integrated) System berdasarkan ketentuan yang berlaku di Politeknik Pos Indonesia</font>'
    contain.append(Paragraph(ptext, styles["Justify"]))
    contain.append(Spacer(1, .8*cm))
    
    contain.append(Image(f'./skpi/footer.png', 19*cm, 1.8*cm))
    
    
def sendEmail(email, fileName, path, mhs):
    try:
        subject = f"SKL {mhs}"
        body = f"Jadi ini skl kamu {mhs}"

        sender_email = config.email_iteung
        receiver_email = email
        # receiver_email = 'syafrial.fachri@poltekpos.ac.id'
        password = config.pass_iteung

        message = MIMEMultipart()
        message["From"] = f'ITeung <{config.email_iteung}>'
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        with open(path+fileName, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            "attachment; filename= %s " % fileName,
        )

        message.attach(part)
        
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

        print(f'File {fileName} berhasil dikirim ke {email}')
    except FileNotFoundError:
        print("File tidak ditemukan")
    except Exception as e: 
        print(str(e))

def getDosen(num):
    num = numbers.normalize(num)
    db = kelas.dbConnectSiap()
    sql = "select Login, Email from simak_mst_dosen where Handphone = '{0}'".format(num)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1]]
        else:
            return False
        
def getMahasiswa(num):
    num = numbers.normalize(num)
    db = kelas.dbConnectSiap()
    sql = "select MhswID, ProdiID, Email from simak_mst_mahasiswa where Handphone = '{0}'".format(num)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1], row[2]]
        else:
            return False

def convertProdi(prodi):
    db = kelas.dbConnectSiap()
    sql = f"SELECT Singkatan, Nama, ProdiID FROM simpati.simak_mst_prodi WHERE ProdiID='{prodi}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0].lower(), row[1].title(), row[2]]
        else:
            return None
        
def getWadirI():
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY, Nama FROM simpati.simak_mst_pejabat WHERE JenisJabatanID='2'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1]]
        else:
            return None
        
def getKaprodi(prodi):
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY, Nama FROM simak_mst_pejabat WHERE ProdiID='{prodi}' AND JenisJabatanID=5"
    # print(sql)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1]]
        else:
            return None

def getKodeDosen(nik):
    db = kelas.dbConnectSiap()
    sql = f'select Login from simak_mst_dosen where NIPY="{nik}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

def checkSKPIProdiFile(prodi):
    year = datetime.datetime.now().year
    return path.exists(f"./skpi/list-skpi/{prodi}-{year}.xlsx")

def checkSKPIDir(prodi):
    if path.exists(f"./skpi/skpi-{prodi}"):
        pass
    else:
        os.mkdir(f"./skpi/skpi-{prodi}") 
        
def checkQrCodeDir(prodi):
    if path.exists(f"./skpi/qrcode-{prodi}"):
        pass
    else:
        os.mkdir(f"./skpi/qrcode-{prodi}") 

def giveFileName(npm, prodi):
    if npm:
        fileName = f"skl-{npm}.pdf"
    elif prodi:
        fileName = f"skl-{prodi}.pdf"
    else:
        fileName = f"skl-all.pdf"
        
    return fileName

def getSemester(jenjang):
    listSemester = {
        "d4": "8",
        "d3": "6"
    }

    return listSemester.get(jenjang, None)

def makeLinkVerifiy(kodeDosen, npm, role):
    datenow = datetime.datetime.date(datetime.datetime.now()).strftime('%d-%m-%Y')
    timenow = datetime.datetime.now().time().strftime('%H:%M:%S')
    module_name="skpi"
    data = f'{module_name};{datenow};{timenow};{kodeDosen};{npm};{role}'
    makeit64 = f'{data}{bkd.randomString(64 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit64.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link

def makeQrcodeLinkVerifySign(link, kodeDosen, npm, prodi, role):
    checkQrCodeDir(prodi)
    img = qrcode.make(link)
    filepath = f'./skpi/qrcode-{prodi}/qrcode-{npm}-{kodeDosen}-{role}.png'
    img.save(filepath)
    return filepath

def verifyDigitalSign(resultpasscode):
    data = resultpasscode.split(';')
    tanggal = data[1]
    waktu = data[2]
    kodeDosen = data[3]
    npm = data[4]
    role = data[5]
    
    msgreply = f'SKL {npm} telah ditandatangani oleh {kodeDosen} sebagai {role} penerbitan tanda tangan pada {tanggal} jam {waktu}'
    return msgreply