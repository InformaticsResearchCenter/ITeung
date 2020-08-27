from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, cm
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors

from module import kelas
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

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) != None:
        ret = True
    else:
        ret = False
    return ret


def replymsg(driver, data):    
    if kelas.cekSiap():    
        num = numbers.normalize(data[0])
        kodeDosen = kelas.getKodeDosen(num)
        # wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        # wmsg = wmsg.replace('#EMAIL#', kelas.getEmailDosen(kodeDosen))
        # wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
        # wa.typeAndSendMessage(driver, wmsg)
        tahunID = '20192'
        msgreply = ""
        try:
            if kelas.getNpmandNameMahasiswa(num):
                try:
                    npm, nama=kelas.getNpmandNameMahasiswa(num)
                    kategori = getKategoriSidang(npm, tahunID)
                    if checkStatusSidang(npm, tahunID, kategori):
                        email = getEmail(npm)
                        data = f"{npm};{tahunID};{email}"
                        subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                    else:
                        msgreply = "Acc revisi dulu, terus minta BA dulu sama #BOTNAME#..."
                    
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
    makePdf(npm, tahunID, data[2])

def checkStatusSidang(npm, tahunID, kategori):
    db=kelas.dbConnect()
    print()
    sql=f"SELECT npm FROM sidang_data WHERE npm = '{npm}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}' AND penguji_utama = 'True' AND penguji_pendamping  = 'True' AND koordinator  = 'True' AND kaprodi  = 'True'"
    print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False

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

def getDataDosen(dosenid):
    db= kelas.dbConnectSiap()
    sql=f'select Nama, Gelar, NIP from simak_mst_dosen where Login="{dosenid}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return (f"{row[0].title()} {row[1]}", row[2] if row[2] else "Belum Diisi") 
        else:
            return None

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

def makePdf(npm, tahunID, email):
    namaFile = f"revisisidang\\pengesahan-sidang-{npm}-{tahunID}.pdf"
    
    doc = SimpleDocTemplate(namaFile,
                            pagesize=A4,
                            rightMargin=3*cm,
                            leftMargin=4*cm,
                            topMargin=4*cm,
                            bottomMargin=3*cm)
    
    contain=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Times', fontSize=12))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontName='Times', fontSize=12))
    styles.add(ParagraphStyle(name='CenterSpacing', alignment=TA_CENTER, fontName='Times', fontSize=12, leading=16))
        
    df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')
    df.set_index('npm', inplace=True)
    listPem = ['pem1','pem2','pem3', 'pem4', 'jadwal']
    pem = df.loc[int(npm), listPem]
    
    tglSidang = pem[4].split(',')[1].title()
    penUtama, nikPenUtama = getDataDosen(pem[3])
    penPendamping, nikPenPendamping = getDataDosen(pem[2])
    pemUtama, nikPemUtama = getDataDosen(pem[1])
    pemPendamping, nikPemPendamping = getDataDosen(pem[0])
    
    namaMhs, prodi = getDataMahasiswa(npm)
    npmMhs = f'{npm[0]}.{npm[1:3]}.{npm[3]}.{npm[4:]}'
    
    program = tipeSidang(getKategoriSidang(npm, tahunID))
    
    judul = getJudul(npm, tahunID)
        
    koor = 'M. Yusril Helmi Setyawan, S.Kom., M.Kom.'
    nikKoor = '113.74.163'
    
    kaProdi = 'M. Yusril Helmi Setyawan, S.Kom., M.Kom.'
    nikKaProdi = '113.74.163'
    
    makePagePenguji(contain, styles, judul, namaMhs, npmMhs, program, tglSidang, penPendamping, nikPenPendamping, penUtama, nikPenUtama, koor, nikKoor)
    contain.append(PageBreak())
    makePagePembimbing(contain, styles, judul, namaMhs, npmMhs, program, tglSidang, pemUtama, nikPemUtama, pemPendamping, nikPemPendamping, prodi, kaProdi, nikKaProdi)
    
    doc.build(contain)
    
    time.sleep(2)
    sendEmail(email, f'pengesahan-sidang-{npm}-{tahunID}.pdf', namaMhs)
    
def makePagePenguji(contain, styles, judul, namaMhs, npmMhs, program, tglSidang, penPendamping, nikPenPendamping, penUtama, nikPenUtama, koor, nikKoor):
    text = f'<font size="16"><b>LEMBAR PENGESAHAN</b></font>'
    contain.append(Paragraph(text, styles["Center"]))
    contain.append(Spacer(1, 1.4*cm))
    
    text = f'<font size="14"><b>{judul}</b></font>'
    contain.append(Paragraph(text, styles["CenterSpacing"]))
    contain.append(Spacer(1, 1.8*cm))
    
    data = [[namaMhs, npmMhs],
        ]
    table = Table(data, [8.5*cm, 4*cm], len(data)*[.8*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('ALIGN', (-1,-1), (-1,-1), 'LEFT'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    data = [[Paragraph(f'<font size="12">Laporan Program {program} ini telah diperiksa, disetujui dan disidangkan<br/>Di Bandung, {tglSidang}<br/>Oleh :</font>', styles["CenterSpacing"])],
            ['Penguji Pendamping', '', 'Penguji Utama'],
            ['', '', ''],
            [Paragraph(f'<font size="12"><u>{penPendamping}</u><br/>NIK. {nikPenPendamping}</font>', styles["CenterSpacing"]), '', Paragraph(f'<font size="12"><u>{penUtama}</u><br/>NIK. {nikPenUtama}</font>', styles["CenterSpacing"])],
            [Paragraph(f'<font size="12">Menyetujui,<br/>Koordinator {program}</font>', styles["CenterSpacing"])],
            [''],
            [Paragraph(f'<font size="12"><u>{koor}</u><br/>NIK. {nikKoor}</font>', styles["CenterSpacing"])],
        ]
    table = Table(data, [6.7*cm, .2*cm, 6.7*cm], [2*cm,1.2*cm,3*cm,1.8*cm,2*cm,3*cm,1.4*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 4), (2,4)),
        ('SPAN', (0, 5), (2,5)),
        ('SPAN', (0, 6), (2,6)),
        
    ]))
    contain.append(table)

def makePagePembimbing(contain, styles, judul, namaMhs, npmMhs, program, tglSidang, pemUtama, nikPemUtama, pemPendamping, nikPemPendamping, prodi, kaProdi, nikKaProdi):
    text = f'<font size="16"><b>LEMBAR PENGESAHAN</b></font>'
    contain.append(Paragraph(text, styles["Center"]))
    contain.append(Spacer(1, 1.4*cm))
    
    text = f'<font size="14"><b>{judul}</b></font>'
    contain.append(Paragraph(text, styles["CenterSpacing"]))
    contain.append(Spacer(1, 1.8*cm))
    
    data = [[namaMhs, npmMhs],
        ]
    table = Table(data, [8.5*cm, 4*cm], len(data)*[.8*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('ALIGN', (-1,-1), (-1,-1), 'LEFT'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    data = [[Paragraph(f'<font size="12">Laporan Program {program} ini telah diperiksa, disetujui dan disidangkan<br/>Di Bandung, {tglSidang}<br/>Oleh :</font>', styles["CenterSpacing"])],
            ['Pembimbing Utama,', '', 'Pembimbing Pendamping'],
            ['', '', ''],
            [Paragraph(f'<font size="12"><u>{pemUtama}</u><br/>NIK. {nikPemUtama}</font>', styles["CenterSpacing"]), '', Paragraph(f'<font size="12"><u>{pemPendamping}</u><br/>NIK. {nikPemPendamping}</font>', styles["CenterSpacing"])],
            [Paragraph(f'<font size="12">Menyetujui,<br/>Ketua Program Studi {prodi},</font>', styles["CenterSpacing"])],
            [''],
            [Paragraph(f'<font size="12"><u>{kaProdi}</u><br/>NIK. {nikKaProdi}</font>', styles["CenterSpacing"])],
        ]
    table = Table(data, [6.7*cm, .2*cm, 6.7*cm], [2*cm,1.2*cm,3*cm,1.8*cm,2*cm,3*cm,1.4*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 4), (2,4)),
        ('SPAN', (0, 5), (2,5)),
        ('SPAN', (0, 6), (2,6)),
        
    ]))
    contain.append(table)
    
def tipeSidang(tipe):
    dict = {
        'ta': 'Tugas Akhir',
        'i1': 'Internship I',
        'i2': 'Internship II',
        'p3': 'Proyek 3',
        'p2': 'Proyek 2',
        'p1': 'Proyek 1',
    }
    
    return dict.get(tipe, None)

def sendEmail(email, file, mhs):
    try:
        subject = f"Pengesahan Sidang {mhs}"
        body = f"Jadi ini pengesahan sidang {mhs}"

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

        with open(f'revisisidang\\{file}', "rb") as attachment:
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