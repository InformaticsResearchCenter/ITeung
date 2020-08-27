from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, cm
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors

from module import kelas, bkd
from lib import wa, reply, message, numbers
import os, config
import pandas as pd
import subprocess
import time

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

from datetime import datetime
from Crypto.Cipher import AES

import string, random, qrcode

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) != None or kelas.getKodeDosen(data[0]) != '':
        ret = True
    else:
        ret = False
    return ret


def replymsg(driver, data):    
    if kelas.cekSiap():    
        num = numbers.normalize(data[0])
        # wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        # wmsg = wmsg.replace('#EMAIL#', kelas.getEmailDosen(kodeDosen))
        # wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
        # wa.typeAndSendMessage(driver, wmsg)
        tahunID = '20192'
        msg = data[3].lower().split(' ')
        msgreply = ""
        try:
            if kelas.getKodeDosen(num):        
                try:
                    npm = [npm for npm in msg if npm.isdigit() and len(npm) == 7][0]
                    # print(npm, kategori)
                    if checkRevisiStatus(npm, tahunID):
                        email = getEmail(kelas.getKodeDosen(num))
                        data = f"{npm};{tahunID};{email}"
                        subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                    else:
                        msgreply = "Revisian dulu weh, blm di acc revisian Anda dari dua penguji..."
                    
                except Exception as e: 
                    msgreply = f"Errornya: {str(e)}"
                    
            elif kelas.getNpmandNameMahasiswa(num):
                try:
                    print("sini")
                    npm, nama=kelas.getNpmandNameMahasiswa(num)
                    if checkRevisiStatus(npm, tahunID):
                        email = getEmail(npm)
                        data = f"{npm};{tahunID};{email}"
                        subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                    else:
                        msgreply = "Revisian dulu weh, blm di acc revisian Anda dari dua penguji..."
                    
                except Exception as e: 
                    msgreply = f"Errornya: {str(e)}"
            else:
                msgreply = f"Hayoo siapa kamu"
            
        except Exception as e: 
            msgreply = f'Wadaw.. anda salah keyword... {str(e)}'
        
        print(msgreply)
        # wa.typeAndSendMessage(driver, msgreply)
        
    else:
        wa.typeAndSendMessage(
            driver, 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....')
    return ''

def run(data):
    data = data.split(';')
    npm = data[0]
    tahunID = data[1]
    kategori = getKategoriSidang(npm, tahunID)
    
    statusSidang(npm, tahunID, kategori)
    makePdf(npm, kategori, tahunID, data[2])

def getEmail(kode):
    db = kelas.dbConnectSiap()
    if kode.isdigit():
        sql = f'select Email from simak_mst_mahasiswa where MhswID = "{kode}"'
    else:
        sql = f'SELECT Email FROM simpati.simak_mst_dosen where Login = "{kode}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

def getKategoriSidang(npm, tahunID):
    db = kelas.dbConnectSiap()
    sql = f"SELECT distinct(Tipe) FROM simpati.simak_croot_bimbingan WHERE MhswID = '{npm}' AND TahunID = '{tahunID}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

def checkKategoriSidang(npm, tahunID):
    db = kelas.dbConnectSiap()
    sql = f"SELECT distinct(Tipe) FROM simpati.simak_croot_bimbingan WHERE MhswID = '{npm}' AND TahunID = '{tahunID}';"
    print(sql)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return row
        else:
            return False

def tipeSidang(tipe):
    dict = {
        'ta': 'Tugas Akhir',
        'i1': 'Internship I',
        'i2': 'Internship II',
        'p3': 'Proyek 3',
        'p2': 'Proyek 2',
        'p1': 'Proyek 1',
    }
    
    return dict.get(tipe, False)

def tipeDosen(tipe):
    dict = {
        'penut': 'Penguji Utama',
        'penpen': 'Penguji Pendamping',
        'koor': 'Koordinator',
        'kaprodi': 'Ketua Program Studi',
    }
    
    return dict.get(tipe, False)

def statusSidang(npm, tahunID, kategori):
    db=kelas.dbConnect()
    if not checkStatusSidang(npm, tahunID, kategori):
        sql = f"INSERT INTO sidang_data (npm, tahun_id, kategori) VALUE ('{npm}', '{tahunID}', '{kategori}')"
        with db:
            cur=db.cursor()
            cur.execute(sql)
    else:
        pass
    

def checkStatusSidang(npm, tahunID, kategori):
    db=kelas.dbConnect()
    sql=f"SELECT npm FROM sidang_data WHERE npm = '{npm}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}'"
    print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False

def checkRevisiStatus(npm, tahunID):
    db=kelas.dbConnect()
    sql=f"SELECT COUNT(DISTINCT(penguji)) as total FROM revisi_data WHERE npm ='{npm}' AND tahun_id = '{tahunID}' AND status = 'True'"
    print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            print(row[0])
            if int(row[0]) == 2:
                print("acc")
                return True
            else:
                return False
        else:
            return False

def getDataMahasiswa(npm):
    db = kelas.dbConnectSiap()
    sql = f"select smm.Nama, smp.Nama from simak_mst_mahasiswa smm, simak_mst_prodi smp where MhswID = '{npm}' AND smm.ProdiID = smp.ProdiID"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return row
        else:
            return False

def listRevisiSidang(npm, tahun_id, penguji):
    db=kelas.dbConnect()
    sql=f'select revisi from revisi_data where npm="{npm}" and tahun_id="{tahun_id}" and penguji="{penguji}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        listRevisi = list()
        print(rows)
        if rows:            
            for i, row in enumerate(rows):
                listRevisi.append([f'{i+1}', row[0]])
            return listRevisi
        else:
            return False

def getDataDosen(dosenid):
    db= kelas.dbConnectSiap()
    sql=f'select Nama, Gelar from simak_mst_dosen where Login="{dosenid}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return f"{row[0].title()} {row[1]}"
        else:
            return None

def getKaProdi(prodiid):
    db = kelas.dbConnectSiap()
    sql = f"select NIPY, Nama from simak_mst_pejabat where ProdiID={prodiid} and JenisJabatanID=5"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row
        else:
            return None

def updateStatusTTD():
    db=kelas.dbConnect()
    sql=f"UPDATE "
    with db:
        cur=db.cursor()
        cur.execute(sql)

def makeLinkVerifiy(kodeDosen, npm, kategori, role, tahunID):
    datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
    timenow = datetime.now().time().strftime('%H:%M:%S')
    module_name="ba_revisi_sidang"
    data = f'{module_name};{datenow};{timenow};{kodeDosen};{npm};{kategori};{role};{tahunID}'
    makeit64 = f'{data}{bkd.randomString(64 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit64.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link

def makeQrcodeLinkVerifySign(link, kodeDosen, npm, kategori):
    img = qrcode.make(link)
    img.save(f'./revisisidang/qrcode/{kodeDosen}-{npm}-{kategori}.png')
    
def verifyDigitalSign(resultpasscode):
    resultpasscode=resultpasscode.split(';')
    tanggal=resultpasscode[1].split('-')[0]
    bulan=bkd.bulanSwitcher(resultpasscode[1].split('-')[1])
    tahun=resultpasscode[1].split('-')[2]
    sah_jam=resultpasscode[2]
    nama_dosen=getDataDosen(resultpasscode[3])
    nama_mahasiswa=  getDataMahasiswa(resultpasscode[4])
    kategori_bimbingan=resultpasscode[5]
    judul = getJudul(resultpasscode[4], resultpasscode[7])
    role= tipeDosen(resultpasscode[6])
    msgreply = f"Tanda tangan berita acara sidang *{kategori_bimbingan}* atas nama *{nama_mahasiswa}* oleh *{nama_dosen}* sebagai *{role}* dengan judul {kategori_bimbingan} *{judul}*\nPenerbitan Tanda Tangan: {sah_jam} {tanggal} {bulan} {tahun}"
    return msgreply

def makePdf(npm, kategori, tahunID, email):    
    noSurat = 'NO. 51/D4-TI/TA/F10/0520'    
    nip, kaProdi = getKaProdi('14')
    kaProdi = f'( {kaProdi} )'
    
    tahunAjaran = f'{tahunID[:4]}/{int(tahunID[:4])+1}' # '2019/2020'
    dataMhs = getDataMahasiswa(npm)
    namaMhs = dataMhs[0]
    prodi = dataMhs[1]
    npmMhs = int(npm)
    kelasMhs = '-'
    
    
    df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')
    df.set_index('npm', inplace=True)
    listPem = ['pem3', 'pem4', 'jadwal','koor', 'jam']
    pem = df.loc[npmMhs, listPem]
    print(pem.values.tolist())
    
    listRevisiPenUt = listRevisiSidang(npm, tahunID, pem[0])
    listRevisiPenPen = listRevisiSidang(npm, tahunID, pem[1])
    
    tanggal = pem[2].split(',')[1].title().strip()
    waktu = pem[4]
    kategori = tipeSidang(kategori)
    judul = getJudul(npm, tahunID)
    
    penUtama = f'( {getDataDosen(pem[0])} )'
    penPendamping = f'( {getDataDosen(pem[1])} )'    
    koor = '( {getDataDosen(pem[3])} )'
    
    kaprodiID = getDosenIDfromNIPY(nip)
    kodeDosens = [pem[0], pem[1], pem[3], kaprodiID]
    listTTD = []
    
    for i, kodeDosen in enumerate(kodeDosens):
        if i == 0:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'penut', tahunID)
        elif i == 1:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'penpen', tahunID)
        elif i == 2:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'koor', tahunID)
        elif i == 3:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'kaprodi', tahunID)
        
        makeQrcodeLinkVerifySign(link, kodeDosen, npm, kategori)
        listTTD.append(f'{kodeDosen}-{npm}-{kategori}')
    
    namaFile = f"revisisidang\\beritaacara\\bap-revisi-sidang-{tahunID}-{npm}.pdf"
    logo = "revisisidang\\logo-poltekpos.png"
    
    doc = SimpleDocTemplate(namaFile,
                            pagesize=A4,
                            rightMargin=1.5*cm,
                            leftMargin=1.5*cm,
                            topMargin=1.5*cm,
                            bottomMargin=1*cm)
    
    contain=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Times', fontSize=12))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontName='Times', fontSize=12))
    styles.add(ParagraphStyle(name='CenterSpacing', alignment=TA_CENTER, fontName='Times', fontSize=12, leading=18))
    
    
    makePages(contain, logo, styles, tahunAjaran, noSurat, namaMhs, npmMhs, kelasMhs, prodi, tanggal, penUtama, penPendamping, kaProdi, koor, kategori, listTTD, waktu, judul, listRevisiPenUt, listRevisiPenPen)
    
    doc.build(contain)
    time.sleep(2)
    # sendEmail(email, f'bap-revisi-sidang-{tahunID}-{npm}.pdf', namaMhs)

def makePages(contain, logo, styles, tahunAjaran, noSurat, namaMhs, npmMhs, kelasMhs, prodi, tanggal, penUtama, penPendamping, kaProdi, koor, kategori, listTTD, waktu, judul, listRevisiPenUt, listRevisiPenPen):
    data = [[Image(logo, 2.78 * cm, 2.38 * cm), Paragraph(f'<font size="14"><b>BERITA ACARA REVISI<br/>{kategori.upper()}<br/>POLITEKNIK POS INDONESIA<br/>TAHUN AJARAN {tahunAjaran}</b></font>', styles["CenterSpacing"]), Paragraph(f'<font size="23"><b>F10</b></font><br/><font size="11"><b>{noSurat}</b></font>', styles["CenterSpacing"])]
        ]
    table = Table(data, [3*cm, 9*cm, 6*cm], len(data)*[3*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    text = f'<font size="12">Saya mahasiswa yang bertanda tangan sebagai berikut,</font>'
    contain.append(Paragraph(text, styles["Justify"]))
    contain.append(Spacer(1, .5*cm))
    
    data = [['Nama Mahasiswa', ':', namaMhs],
            ['NPM', ':', npmMhs],
            ['Judul', ':', judul],
            ['Tanggal', ':', tanggal],
            ['Waktu', ':', waktu],
        ]
    table = Table(data, [5*cm, .5*cm, 12.5*cm], len(data)*[.6*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    text = f'<font size="12">telah melakukan revisi {kategori.title()} pada Prodi {prodi} Politeknik Pos Indonesia Tahun Ajaran {tahunAjaran} sesuai dengan peraturan yang berlaku, berdasarkan dengan perubahan aturan yang ditetapkan selama masa pandemi Covid 19 dengan kegiatan yang dilaksanakan secara daring dan dokumen elektronik.</font>'
    contain.append(Paragraph(text, styles["Justify"]))
    contain.append(Spacer(1, .5*cm))
    
    text = f'<font size="12">Berikut hasil revisi  {kategori.title()}:</font>'
    contain.append(Paragraph(text, styles["Justify"]))
    contain.append(Spacer(1, .5*cm))
    
    text = f'<font size="12">Penguji Utama</font>'
    contain.append(Paragraph(text, styles["Justify"]))
    contain.append(Spacer(1, .3*cm))
        
    data = [['No', 'Uraian', 'Tanda Tangan Mhs']
        ]
    data.extend(listRevisiPenUt)
    
    table = Table(data, [1.5*cm, 10*cm, 4*cm], len(data)*[.8*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ALIGN', (0,0), (2,0), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('SPAN', (2, 1), (-1, -1)),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    text = f'<font size="12">Penguji Pendamping</font>'
    contain.append(Paragraph(text, styles["Justify"]))
    contain.append(Spacer(1, .3*cm))
    
    data = [['No', 'Uraian', 'Tanda Tangan Mhs']
        ]
    data.extend(listRevisiPenPen)
    
    table = Table(data, [1.5*cm, 10*cm, 4*cm], len(data)*[.8*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ALIGN', (0,0), (2,0), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('SPAN', (2, 1), (-1, -1)),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    path = './revisisidang/qrcode/'
    
    data = [[f'Bandung, {tanggal}'],
            ['Mengetahui:'],
            ['Penguji Utama', '', 'Penguji Pendamping'],
            [Image(f'{path}{listTTD[0]}.png', 4 * cm, 4 * cm), '', Image(f'{path}{listTTD[1]}.png', 4 * cm, 4 * cm)],
            [penUtama, '', penPendamping],
            ['Diperiksa oleh,'],
            [Paragraph(f'<font size="12">Ketua<br/>Program Studi {prodi}</font>', styles["CenterSpacing"]), '', Paragraph(f'<font size="12">Koordinator {kategori.title()}<br/>Program Studi {prodi}</font>', styles["CenterSpacing"])],
            [Image(f'{path}{listTTD[3]}.png', 4 * cm, 4 * cm), '', Image(f'{path}{listTTD[2]}.png', 4 * cm, 4 * cm)],
            [kaProdi, '', koor],
        ]
    table = Table(data, [8.5*cm, 1*cm, 8.5*cm], [.8*cm, .8*cm,.8*cm,4.5*cm,.8*cm,.8*cm,1.4*cm,4.5*cm,.8*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 1), (2, 1)),
        ('SPAN', (0, 5), (2,5))
        
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
def sendEmail(email, file, mhs):
    try:
        subject = f"Berita Acara Sidang {mhs}"
        body = f"Jadi ini berita acara sidang {mhs}"

        sender_email = config.email_iteung
        receiver_email = email
        receiver_email = 'divakrishnam@yahoo.com'
        password = config.pass_iteung

        message = MIMEMultipart()
        message["From"] = f'ITeung <{config.email_iteung}>'
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        with open(f'revisisidang\\beritaacara\\{file}', "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            "attachment; filename= %s " % file,
        )

        message.attach(part)
        
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

        print(f'File {file} berhasil dikirim ke {email}')
    except FileNotFoundError:
        print("File tidak ditemukan")
    except Exception as e: 
        print(str(e))

def randomString(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

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
        
def getJudul(npm, tahunID):
    db = kelas.dbConnect()
    sql = f"select judul from bimbingan_data where npm ='{npm}' and tahun_id='{tahunID}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None