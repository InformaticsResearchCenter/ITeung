from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus.tables import Table, TableStyle

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

from Crypto.Cipher import AES

from module import kelas, bkd
import subprocess
from os import path

import datetime, os
import qrcode
from lib import wa, reply, numbers

import config

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) != None:
        ret = True
    else:
        ret = False
    return ret

def replymsg(driver, data):
    msgreply = ""
    if kelas.cekSiap():
        num = numbers.normalize(data[0])        
        try:
            if kelas.getNpmandNameMahasiswa(num):
                npm, nama = kelas.getNpmandNameMahasiswa(num)
                # print(npm, nama)
                tahunID = kelas.getTahunID()
                namaMhs, prodiMhs, singkatan, prodiID, email = getMahasiswaByNpm(npm)
                # print(namaMhs, prodiMhs, singkatan, prodiID, email)
                noSurat = insertMhs(npm, prodiID, tahunID)
                # print(noSurat)
                if checkApproveMhs(npm, prodiID, tahunID):
                    data = f"{npm};{singkatan};{noSurat}"
                    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                    wmsg = wmsg.replace('#EMAIL#', email)
                    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
                    wa.typeAndSendMessage(driver, wmsg)
                else:
                    msgreply = "SKMK anda telah diajukan, silahkan hubungi Ka. Baak untuk minta approve SKMK yang telah diajukan"
            else:
                msgreply = f"Ikan teri pake saos.. anda siapa bos..\nSebenarnya ada beberapa kemungkinan, pertama kamu bukan mahasiswa yg udh wisuda.. Mungkin no hp di SIAP salah kali... apalagi ya.. kyknya itu aja.."
            
        except Exception as e:
            msgreply = f'Ikan hiu makan tomat.. ada error mat... {str(e)}'
            
    else:
        # pass
        wa.typeAndSendMessage(driver, 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu')
    return msgreply

def run(data):
    data = data.split(';')
    npm = data[0]
    singkatan = data[1].lower()
    noSurat = data[2]
    
    makePage(npm, singkatan, noSurat)

def makePage(npm, prodi, noSurat):
    checkDir(f"./skmk/skmk-{prodi}/")
    
    fileName = f"./skmk/skmk-{prodi}/{npm}.pdf"
    
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    tahunID = kelas.getTahunID()
    semester, tahun = getTahunAjaran(tahunID)
    mhs = getMahasiswa(npm)
    
    doc = SimpleDocTemplate(fileName,
                            pagesize=A4,
                            rightMargin=2.5*cm,
                            leftMargin=2.5*cm,
                            topMargin=4*cm,
                            bottomMargin=3*cm)
    contain=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Times', fontSize=12, leading=14))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontName='Times'))
    
    ptext = '<font size="15"><b>SURAT KETERANGAN MASIH KULIAH</b></font>'
    contain.append(Paragraph(ptext, styles["Center"]))
    contain.append(Spacer(1, .4*cm))
    
    ptext = f'<font size="12">No : {noSurat}/SKMK/BAAK/{convertRomawi(month)}/{year}</font>'
    contain.append(Paragraph(ptext, styles["Center"]))
    contain.append(Spacer(1, 1.8*cm))
    
    ptext = '<font size="12">Direktur Politeknik Pos Indonesia menerangkan dengan sesungguhnya bahwa,</font>'
    contain.append(Paragraph(ptext, styles["Justify"]))
    contain.append(Spacer(1, 1*cm))
    
    styleWrap = styles["BodyText"]
    styleWrap.alignment = TA_JUSTIFY
    styleWrap.fontName = 'Times'
    styleWrap.fontSize = 12
    styleWrap.leading = 14
    
    data = [['Nama Mahasiswa', ':', mhs[0]],
        ['Tempat / Tanggal Lahir', ':', f"{mhs[1]}, {convertYmd(mhs[2])}"],
        ['Agama', ':', mhs[3]],
        ['Alamat Mahasiswa', ':', Paragraph(f'{mhs[4]}, Rt. {mhs[5] if mhs[5] != "NULL" else "-"}, Rw. {mhs[6] if mhs[6] != "NULL" else "-"}, {mhs[7]}, {mhs[8]} - {mhs[9]}', styleWrap)],
        ['Program Studi', ':', mhs[10]],
        ['NPM', ':', npm],
        ['Nama Orang Tua', ':', mhs[11]],
        ['Pekerjaan Orang Tua', ':', mhs[12].strip()],
        ['Alamat Orang Tua', ':', Paragraph(f'{mhs[13]}, Rt. {mhs[14] if mhs[14] != "NULL" else "-"}, Rw. {mhs[15] if mhs[15] != "NULL" else "-"}', styleWrap)],
        ['Kota, Kode Pos', ':', f'{mhs[16]}, {mhs[18]}'],
    ]
    table = Table(data, [5*cm, .5*cm, 10.5*cm], [.6*cm, .6*cm, .6*cm, 1.1*cm, .6*cm, .6*cm, .6*cm, .6*cm, 1.1*cm, .6*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'TOP'), 
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    ptext = f'<font size="12">Adalah benar terdaftar dan aktif sebagai Mahasiswa Politeknik Pos Indonesia Semester {semester} Tahun Akademik {tahun}</font>'
    contain.append(Paragraph(ptext, styles["Justify"]))
    contain.append(Spacer(1, .8*cm))
    
    ptext = '<font size="12">Demikian surat keterangan ini dibuat untuk dipergunakan seperlunya</font>'
    contain.append(Paragraph(ptext, styles["Justify"]))
    contain.append(Spacer(1, 1*cm))
    
    nik, nama = getKaBaak()
    
    link = makeLinkVerifiy(getKodeDosen(nik), npm)
    pathTTDKaBaak = makeQrcodeLinkVerifySign(link, npm, prodi)
    
    data = [
        ['', f'Bandung, {day} {convertMonth(month)} {year}'],
        ['', 'Direktur.'],
        ['', 'Ka. BAAK'],
        ['', Image(pathTTDKaBaak, 3.8 * cm, 3.8 * cm)],
        ['', nama],
    ]

    table = Table(data, [8*cm, 8*cm], [.6*cm, .6*cm, .6*cm, 4*cm, .6*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        # ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        # ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'), 
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    contain.append(table)

    doc.build(contain, onFirstPage=headerFooter, onLaterPages=headerFooter)
    
    sendEmail(mhs[19], f"{npm}.pdf", f"./skmk/skmk-{prodi}/", mhs[0])

def headerFooter(canvas, doc):
    canvas.saveState()
    
    header = Image(f'./skmk/header.png', 19*cm, 2.5*cm)
    w, h = header.wrap(doc.width, 2.5*cm)
    header.drawOn(canvas, 1*cm, doc.height + 4*cm)

    footer = Image(f'./skmk/footer.png', 19*cm, 1.8*cm)
    w, h = footer.wrap(doc.width, 2.5*cm)
    footer.drawOn(canvas, 1*cm, h - 1.5*cm)

    canvas.restoreState()

def getKaBaak():
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY, Nama FROM simpati.simak_mst_pejabat WHERE JenisJabatanID='11'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1]]
    
    return None

def getMahasiswa(npm):
    db = kelas.dbConnectSiap()
    sql = f"SELECT smm.Nama, smm.TempatLahir, smm.TanggalLahir, sra.Nama, smm.Alamat, smm.RT, smm.RW, smm.Kota, smm.Propinsi, smm.KodePos, smp.Nama, smm.NamaAyah, srpo.Nama, smm.AlamatOrtu, smm.RTOrtu, smm.RWOrtu, smm.KotaOrtu, smm.PropinsiOrtu, smm.KodePosOrtu, smm.Email FROM simak_mst_mahasiswa as smm, simak_ref_agama as sra, simak_mst_prodi as smp, simak_ref_pekerjaan_ortu as srpo WHERE sra.Agama=smm.Agama AND smp.ProdiID=smm.ProdiID AND srpo.Pekerjaan=smm.PekerjaanAyah AND smm.MhswID = '{npm}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row
    
    return None

def getMahasiswaByNpm(npm):
    db = kelas.dbConnectSiap()
    sql = f"select smm.Nama, smp.Nama, smp.Singkatan, smm.ProdiID, smm.Email from simak_mst_mahasiswa as smm, simak_mst_prodi as smp where smm.ProdiID=smp.ProdiID and smm.MhswID = '{npm}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1], row[2], row[3], row[4]]
    return False

def getKodeDosen(nik):
    db = kelas.dbConnectSiap()
    sql = f'select Login from simak_mst_dosen where NIPY="{nik}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
    return None

def getNamaDosen(kodeDosen):
    db = kelas.dbConnectSiap()
    sql = f"select Nama, Gelar from simak_mst_dosen where Login = '{kodeDosen}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return f"{row[0].title()}, {row[1]}"
    return False

def checkMhs(npm, prodi, tahunID):
    db=kelas.dbConnect()
    sql=f"select id from skmk_data where npm = {npm} and prodiID = {prodi} and tahunID like '{tahunID[:4]}%'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return row[0]
    return False


def insertMhs(npm, prodi, tahunID):
    db=kelas.dbConnect()
    if not checkMhs(npm, prodi, tahunID):
        sql = f"INSERT INTO skmk_data (npm, prodiID, tahunID) VALUE ('{npm}', '{prodi}', '{tahunID}')"
        with db:
            cur=db.cursor()
            cur.execute(sql)

    return checkMhs(npm, prodi, tahunID)
        
def checkApproveMhs(npm, prodi, tahunID):
    db=kelas.dbConnect()
    sql=f"select * from skmk_data where npm = {npm} and prodiID = {prodi} and tahunID like '{tahunID[:4]}%' and approve is not null"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
    return False

def getTahunAjaran(tahunID):
    jenjang = tahunID[-1]
    tahun = f"{tahunID[:4]}/{int(tahunID[:4])+1}"
    
    semesters = {
        "1": "Ganjil",
        "2": "Genap",
        "3": "Genap"
    }
    
    semester = semesters.get(jenjang, "-")
    return [semester, tahun]

def convertYmd(ymd):
    data = ymd.strftime('%d-%m-%Y').split("-")
    return f"{data[0]} {convertMonth(data[1])} {data[2]}"

def convertMonth(month):
    # print(month)
    months = {
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
    return months.get(str(month), "-")

def convertRomawi(month):
    # print(month)
    months = {
        '1': 'I',
        '2': 'II',
        '3': 'III',
        '4': 'IV',
        '5': 'V',
        '6': 'VI',
        '7': 'VII',
        '8': 'VIII',
        '9': 'IX',
        '10': 'X',
        '11': 'XI',
        '12': 'XII',
    }
    return months.get(str(month), "-")

def makeLinkVerifiy(kodeDosen, npm):
    datenow = datetime.datetime.date(datetime.datetime.now()).strftime('%d-%m-%Y')
    timenow = datetime.datetime.now().time().strftime('%H:%M:%S')
    module_name="skmk"
    data = f'{module_name};{datenow};{timenow};{kodeDosen};{npm};'
    makeit64 = f'{data}{bkd.randomString(64 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit64.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link

def makeQrcodeLinkVerifySign(link, npm, prodi):
    checkDir(f"./skmk/qrcode-{prodi}/")
    img = qrcode.make(link)
    filepath = f'./skmk/qrcode-{prodi}/qrcode-{npm}.png'
    img.save(filepath)
    return filepath

def verifyDigitalSign(resultpasscode):
    data = resultpasscode.split(';')
    tanggal = data[1]
    waktu = data[2]
    namaMhs, prodiMhs, singkatan, prodiID, email = getMahasiswaByNpm(data[4])
    namaDosen = getNamaDosen(data[3])
    
    msgreply = f'Surat Keterangan Masih Kuliah {namaMhs} dari prodi {prodiMhs} telah ditandatangani oleh {namaDosen} sebagai Ka. BAAK Politeknik Pos Indonesia, penerbitan tanda tangan pada {tanggal} jam {waktu}.'
    return msgreply

def checkDir(dir_path):
    if path.exists(dir_path):
        pass
    else:
        os.mkdir(dir_path)

def checkFile(file_path):
    return path.exists(file_path)

def sendEmail(email, fileName, path, mhs):
    try:
        subject = f"SKMK {mhs}"
        body = f"Jadi ini skmk kamu {mhs}"

        sender_email = config.email_iteung
        receiver_email = email
        print(email)
        receiver_email = 'divakrishnam@yahoo.com'
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