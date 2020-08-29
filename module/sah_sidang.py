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
        tahunID = '20192'
        msg = data[3].lower().split(' ')
        msgreply = ""
        try:
            if kelas.getKodeDosen(num):          
                dosenID = kelas.getKodeDosen(num)
                
                email = kelas.getEmailDosen(dosenID)
                wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                wmsg = wmsg.replace('#EMAIL#', email)
                wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
                wa.typeAndSendMessage(driver, wmsg)
                
                tipe = 'ta'
                
                df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')
                listPem = ['koor', 'tipe', 'tahun']
                df = df.loc[:, listPem]
                df = df.drop_duplicates()
                df = df.loc[(df["koor"] == dosenID) & (df["tipe"] == tipe) & (df["tahun"] == int(tahunID))]
                
                if df.empty:
                    msgreply = "Harus koornya cuy ato Anda salah tipe sidang..."
                else:
                    if checkStatusSidangKoor(dosenID, tahunID, tipe):
                        data = f"{'dosen'};{dosenID};{tahunID};{email};{tipe}"
                        subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                    else:
                        msgreply = "Blm ada tuh..."
                    
            elif kelas.getNpmandNameMahasiswa(num):
                try:
                    npm, nama=kelas.getNpmandNameMahasiswa(num)
                    
                    email = getEmail(npm)
                    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                    wmsg = wmsg.replace('#EMAIL#', email)
                    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
                    wa.typeAndSendMessage(driver, wmsg)
                    
                    kategori = getKategoriSidang(npm, tahunID)
                    if checkRevisiStatus(npm, tahunID):
                        if checkStatusSidang(npm, tahunID, kategori):
                            email = getEmail(npm)
                            data = f"{'mahasiswa'};{npm};{tahunID};{email};{kategori}"
                            subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                        else:
                            msgreply = "Approve dulu dari semuanya pembimbing, penguji, koordinator, kaprodi..."
                    else:
                        msgreply = "Approve dulu dari semuanya kedua penguji..."
                    
                except Exception as e: 
                    msgreply = f"Errornya: {str(e)}"
            else:
                msgreply = f"Hayoo siapa kamu"
            
        except Exception as e: 
            msgreply = f'Wadaw.. anda salah keyword... {str(e)}'
        
        print(msgreply)
        wa.typeAndSendMessage(driver, msgreply)
        
    else:
        wa.typeAndSendMessage(
            driver, 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....')
    return ''

def run(data):
    data = data.split(';')
    if data[0] == 'dosen':
        dosenID = data[1]
        tahunID = data[2]
        email = data[3]
        tipe = data[4]
        
        df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')
        listPem = ['npm', 'koor', 'tipe', 'tahun']
        df = df.loc[:, listPem]
        df = df.drop_duplicates()
        npms = df.loc[(df["koor"] == dosenID) & (df["tahun"] == int(tahunID)), ['npm']].values.tolist()
        
        checkDir(f'./revisisidang/pengesahan/')
        namaFile = f"revisisidang\\pengesahan\\pengesahan-sidang-{tahunID}-{dosenID}.pdf"
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
        styles.add(ParagraphStyle(name='CenterSpacing', alignment=TA_CENTER, fontName='Times', fontSize=12, leading=18))
        
        try:
            for npm in npms:
                npm = npm[0]
                if checkStatusSidang(npm, tahunID, tipe):                
                    makePdf(str(npm), tipe, tahunID, email, contain, styles)
                    contain.append(PageBreak())
            else:
                pass
        except Exception as e:
            print(str(e))
        
        doc.build(contain)
        time.sleep(2)
        sendEmail(email, f'pengesahan-sidang-{tahunID}-{dosenID}.pdf', dosenID)
        print("udh cuy")
        
    elif data[0] == 'mahasiswa':
        npm = data[1]
        tahunID = data[2]
        email = data[3]
        kategori = data[4]
        
        checkDir(f'./revisisidang/pengesahan/')
        namaFile = f"revisisidang\\pengesahan\\pengesahan-sidang-{tahunID}-{npm}.pdf"
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
        styles.add(ParagraphStyle(name='CenterSpacing', alignment=TA_CENTER, fontName='Times', fontSize=12, leading=18))
        
        makePdf(npm, kategori, tahunID, email, contain, styles)
        
        doc.build(contain)
        time.sleep(2)
        sendEmail(email, f'pengesahan-sidang-{tahunID}-{npm}.pdf', npm)
        print("udh coy")

def makePdf(npm, kategori, tahunID, email, contain, styles):
    df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')
    df.set_index('npm', inplace=True)
    listPem = ['pem1','pem2','pem3', 'pem4', 'jadwal','koor']
    pem = df.loc[int(npm), listPem]
    
    tglSidang = pem[4].split(',')[1].title()
    penUtama, nikPenUtama = getDataDosen(pem[3])
    penPendamping, nikPenPendamping = getDataDosen(pem[2])
    pemUtama, nikPemUtama = getDataDosen(pem[1])
    pemPendamping, nikPemPendamping = getDataDosen(pem[0])
    namaMhs, prodi = getDataMahasiswa(npm)
    print(npm[0],npm[1:3],npm[3],npm[4:])
    npmMhs = f"{npm[0]}.{npm[1:3]}.{npm[3]}.{npm[4:]}"
    program = tipeSidang(getKategoriSidang(npm, tahunID))
    
    judul = getJudul(npm, tahunID).upper()
    
    namaKoor, nikKoor = getDataDosen(pem[5])
    koor = f'{namaKoor}'
    nikKoor = f'{nikKoor}'
    nikKaProdi, kaProdi = getKaProdi('14')
    
    kaprodiID = getDosenIDfromNIPY(nikKaProdi)
    kodeDosens = [pem[0], pem[1], pem[2], pem[3], pem[5], kaprodiID]
    listTTD = []
    for i, kodeDosen in enumerate(kodeDosens):
        if i == 0:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'pmt', tahunID)
        elif i == 1:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'pmp', tahunID)
        elif i == 2:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'pnt', tahunID)
        elif i == 3:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'pnp', tahunID)
        elif i == 4:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'kor', tahunID)
        elif i == 5:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'kpr', tahunID)
        
        makeQrcodeLinkVerifySign(link, kodeDosen, npm, kategori)
        listTTD.append(f'{kodeDosen}-{npm}-{kategori}')
    
    makePagePenguji(contain, styles, judul, namaMhs, npmMhs, program, tglSidang, penPendamping, nikPenPendamping, penUtama, nikPenUtama, koor, nikKoor, listTTD)
    contain.append(PageBreak())
    makePagePembimbing(contain, styles, judul, namaMhs, npmMhs, program, tglSidang, pemUtama, nikPemUtama, pemPendamping, nikPemPendamping, prodi, kaProdi, nikKaProdi, listTTD)
    
def makePagePenguji(contain, styles, judul, namaMhs, npmMhs, program, tglSidang, penPendamping, nikPenPendamping, penUtama, nikPenUtama, koor, nikKoor, listTTD):
    text = f'<font size="16"><b>LEMBAR PENGESAHAN</b></font>'
    contain.append(Paragraph(text, styles["Center"]))
    contain.append(Spacer(1, 1*cm))
    
    text = f'<font size="14"><b>{judul}</b></font>'
    contain.append(Paragraph(text, styles["CenterSpacing"]))
    contain.append(Spacer(1, .7*cm))
    
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
    contain.append(Spacer(1, .4*cm))
    
    path = './revisisidang/qrcodepengesahan/'
    
    data = [[Paragraph(f'<font size="12">Laporan Program {program} ini telah diperiksa, disetujui dan disidangkan<br/>Di Bandung, {tglSidang}<br/>Oleh :</font>', styles["CenterSpacing"])],
            ['Penguji Pendamping', '', 'Penguji Utama'],
            [Image(f'{path}{listTTD[3]}.png', 4 * cm, 4 * cm), '', Image(f'{path}{listTTD[2]}.png', 4 * cm, 4 * cm)],
            [Paragraph(f'<font size="12"><u>{penPendamping}</u><br/>NIK. {nikPenPendamping}</font>', styles["CenterSpacing"]), '', Paragraph(f'<font size="12"><u>{penUtama}</u><br/>NIK. {nikPenUtama}</font>', styles["CenterSpacing"])],
            [Paragraph(f'<font size="12">Menyetujui,<br/>Koordinator {program}</font>', styles["CenterSpacing"])],
            [Image(f'{path}{listTTD[4]}.png', 4 * cm, 4 * cm)],
            [Paragraph(f'<font size="12"><u>{koor}</u><br/>NIK. {nikKoor}</font>', styles["CenterSpacing"])],
        ]
    table = Table(data, [6.7*cm, .2*cm, 6.7*cm], [2*cm,.6*cm,4.1*cm,2*cm,1.2*cm,4.1*cm,1.4*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 4), (2,4)),
        ('SPAN', (0, 5), (2,5)),
        ('SPAN', (0, 6), (2,6)),
#         ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
# ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    contain.append(table)

def makePagePembimbing(contain, styles, judul, namaMhs, npmMhs, program, tglSidang, pemUtama, nikPemUtama, pemPendamping, nikPemPendamping, prodi, kaProdi, nikKaProdi, listTTD):
    text = f'<font size="16"><b>LEMBAR PENGESAHAN</b></font>'
    contain.append(Paragraph(text, styles["Center"]))
    contain.append(Spacer(1, 1*cm))
    
    text = f'<font size="14"><b>{judul}</b></font>'
    contain.append(Paragraph(text, styles["CenterSpacing"]))
    contain.append(Spacer(1, .7*cm))
    
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
    contain.append(Spacer(1, .4*cm))
    
    path = './revisisidang/qrcodepengesahan/'
    
    data = [[Paragraph(f'<font size="12">Laporan Program {program} ini telah diperiksa, disetujui dan disidangkan<br/>Di Bandung, {tglSidang}<br/>Oleh :</font>', styles["CenterSpacing"])],
            ['Pembimbing Utama,', '', 'Pembimbing Pendamping'],
            [Image(f'{path}{listTTD[0]}.png', 4 * cm, 4 * cm), '', Image(f'{path}{listTTD[1]}.png', 4 * cm, 4 * cm)],
            [Paragraph(f'<font size="12"><u>{pemUtama}</u><br/>NIK. {nikPemUtama}</font>', styles["CenterSpacing"]), '', Paragraph(f'<font size="12"><u>{pemPendamping}</u><br/>NIK. {nikPemPendamping}</font>', styles["CenterSpacing"])],
            [Paragraph(f'<font size="12">Menyetujui,<br/>Ketua Program Studi {prodi},</font>', styles["CenterSpacing"])],
            [Image(f'{path}{listTTD[5]}.png', 4 * cm, 4 * cm)],
            [Paragraph(f'<font size="12"><u>{kaProdi}</u><br/>NIK. {nikKaProdi}</font>', styles["CenterSpacing"])],
        ]
    table = Table(data, [6.7*cm, .2*cm, 6.7*cm],  [2*cm,.6*cm,4.1*cm,2*cm,1.2*cm,4.1*cm,1.4*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
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
        # receiver_email = 'divakrishnam@yahoo.com'
        password = config.pass_iteung

        message = MIMEMultipart()
        message["From"] = f'ITeung <{config.email_iteung}>'
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        with open(f'revisisidang\\pengesahan\\{file}', "rb") as attachment:
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

def checkDir(path):
    try:
        os.mkdir(path)
    except:
        pass #print('sudah ada..')
        
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
        
def checkRevisiStatus(npm, tahunID):
    db=kelas.dbConnect()
    sql=f"SELECT COUNT(DISTINCT(penguji)) as total FROM revisi_data WHERE npm ='{npm}' AND tahun_id = '{tahunID}' AND status = 'True'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            if int(row[0]) == 2:
                return True
            else:
                return False
        else:
            return False

def getJudul(npm, tahunID):
    db = kelas.dbConnect()
    sql = f"select judul from bimbingan_data where npm ='{npm}' and tahun_id='{tahunID}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            return "Ini Judul"
        
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

def makeLinkVerifiy(kodeDosen, npm, kategori, role, tahunID):
    datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
    timenow = datetime.now().time().strftime('%H:%M:%S')
    module_name="sah_sidang"
    data = f'{module_name};{datenow};{timenow};{kodeDosen};{npm};{kategori};{role};{tahunID}'
    
    makeit64 = f'{data}{bkd.randomString(64 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit64.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    # print(link)
    return link

def makeQrcodeLinkVerifySign(link, kodeDosen, npm, kategori):
    checkDir(f'./revisisidang/qrcodepengesahan/')
    img = qrcode.make(link)
    img.save(f'./revisisidang/qrcodepengesahan/{kodeDosen}-{npm}-{kategori}.png')
    
def verifyDigitalSign(resultpasscode):
    resultpasscode=resultpasscode.split(';')
    tanggal=resultpasscode[1].split('-')[0]
    bulan=bkd.bulanSwitcher(resultpasscode[1].split('-')[1])
    tahun=resultpasscode[1].split('-')[2]
    sah_jam=resultpasscode[2]
    nama_dosen=getDataDosen(resultpasscode[3])
    nama_mahasiswa=  getDataMahasiswa(resultpasscode[4])
    kategori_bimbingan= tipeSidang(resultpasscode[5])
    judul = getJudul(resultpasscode[4], resultpasscode[7])
    role= tipeDosen(resultpasscode[6])
    msgreply = f"Tanda tangan pengesahan sidang *{kategori_bimbingan}* atas nama *{nama_mahasiswa}* oleh *{nama_dosen}* sebagai *{role}* dengan judul {kategori_bimbingan} *{judul}*\nPenerbitan Tanda Tangan: {sah_jam} {tanggal} {bulan} {tahun}"
    return msgreply

def tipeDosen(tipe):
    dict = {
        'pmt': 'Pembimbing Utama',
        'pnp': 'Pembimbing Pendamping',
        'pnt': 'Penguji Utama',
        'pnp': 'Penguji Pendamping',
        'kor': 'Koordinator',
        'kpr': 'Ketua Program Studi',
    }
    
    return dict.get(tipe, False)

def checkStatusSidang(npm, tahunID, kategori):
    db=kelas.dbConnect()
    # sql=f"SELECT npm FROM sidang_data WHERE npm = '{npm}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}'"
    sql=f"SELECT npm FROM sidang_data WHERE npm = '{npm}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}' and (penguji_utama is not null and penguji_utama <> '') and (penguji_pendamping is not null and penguji_pendamping <> '') and (pembimbing_utama is not null and pembimbing_utama <> '') and (pembimbing_pendamping is not null and pembimbing_pendamping <> '')"
    # print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
        else:
            return False

def checkStatusSidangKoor(koor, tahunID, kategori):
    db=kelas.dbConnect()
    # sql=f"SELECT npm FROM sidang_data WHERE npm = '{npm}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}'"
    sql=f"SELECT COUNT(DISTINCT(koordinator)) as total FROM sidang_data WHERE koordinator = '{koor}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}' and (penguji_utama is not null and penguji_utama <> '') and (penguji_pendamping is not null and penguji_pendamping <> '') and (pembimbing_utama is not null and pembimbing_utama <> '') and (pembimbing_pendamping is not null and pembimbing_pendamping <> '') and (koordinator is not null and koordinator <> '') and (kaprodi is not null and kaprodi <> '')"
    # print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row[0] > 0:
            return True
        else:
            return False
        
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