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
                wa .typeAndSendMessage(driver, wmsg)
                
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
                        msgreply = ""
                    else:
                        msgreply = "Blm ada tuh..."
                    
            elif kelas.getNpmandNameMahasiswa(num):
                try:
                    npm, nama=kelas.getNpmandNameMahasiswa(num)
                    
                    email = getEmail(npm)
                    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                    wmsg = wmsg.replace('#EMAIL#', email)
                    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
                    wa .typeAndSendMessage(driver, wmsg)
                    
                    kategori = getKategoriSidang(npm, tahunID)
                    if checkRevisiStatus(npm, tahunID):
                        if checkStatusSidang(npm, tahunID, kategori):
                            
                            data = f"{'mahasiswa'};{npm};{tahunID};{email};{kategori}"
                            subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                            msgreply = ""
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
        
        
    else:
        wa.typeAndSendMessage(
            driver, 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu hingga beberapa menit kemudian, lalu ulangi kembali, terima kasih....')
    return msgreply

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
        
        checkDir(f'./revisisidang/beritaacara/')
        namaFile = f"revisisidang\\beritaacara\\bap-revisi-sidang-{tahunID}-{dosenID}.pdf"
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
        
        try:
            for npm in npms:
                npm = npm[0]
                if checkStatusSidang(npm, tahunID, tipe):                
                    makePdf(npm, tipe, tahunID, email, contain, styles)
                    contain.append(PageBreak())
            else:
                pass
        except Exception as e:
            print(str(e))
        
        doc.build(contain)
        time.sleep(2)
        sendEmail(email, f'bap-revisi-sidang-{tahunID}-{dosenID}.pdf', dosenID)
        print("udh cuy")
        
    elif data[0] == 'mahasiswa':
        npm = data[1]
        tahunID = data[2]
        email = data[3]
        kategori = data[4]
        
        checkDir(f'./revisisidang/beritaacara/')
        namaFile = f"revisisidang\\beritaacara\\bap-revisi-sidang-{tahunID}-{npm}.pdf"
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
        
        makePdf(npm, kategori, tahunID, email, contain, styles)
        
        doc.build(contain)
        time.sleep(2)
        sendEmail(email, f'bap-revisi-sidang-{tahunID}-{npm}.pdf', npm)
        print("udh coy")

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
        'pnt': 'Penguji Utama',
        'pnp': 'Penguji Pendamping',
        'kor': 'Koordinator',
        'kpr': 'Ketua Program Studi',
    }
    
    return dict.get(tipe, False)

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

def checkStatusSidang(npm, tahunID, kategori):
    db=kelas.dbConnect()
    # sql=f"SELECT npm FROM sidang_data WHERE npm = '{npm}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}'"
    sql=f"SELECT npm FROM sidang_data WHERE npm = '{npm}' AND tahun_id = '{tahunID}' AND kategori = '{kategori}' and (penguji_utama is not null and penguji_utama <> '') and (penguji_pendamping is not null and penguji_pendamping <> '') and (pembimbing_utama is not null and pembimbing_utama <> '') and (pembimbing_pendamping is not null and pembimbing_pendamping <> '') and (koordinator is not null and koordinator <> '') and (kaprodi is not null and kaprodi <> '')"
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

def listRevisiSidang(npm, tahun_id, penguji, styleWrap):
    db=kelas.dbConnect()
    sql=f'select revisi from revisi_data where npm="{npm}" and tahun_id="{tahun_id}" and penguji="{penguji}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        listRevisi = list()
        if rows:            
            for i, row in enumerate(rows):
                listRevisi.append([f'{i+1}', Paragraph(row[0].capitalize(), styleWrap)])
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
            return f"{row[0].title()}, {row[1]}"
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

def makeLinkVerifiy(kodeDosen, npm, kategori, role, tahunID):
    datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
    timenow = datetime.now().time().strftime('%H:%M:%S')
    module_name="ba_sidang"
    data = f'{module_name};{datenow};{timenow};{kodeDosen};{npm};{kategori};{role};{tahunID}'
    makeit64 = f'{data}{bkd.randomString(64 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit64.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link

def makeQrcodeLinkVerifySign(link, kodeDosen, npm, kategori):
    checkDir(f'./revisisidang/qrcodeberitaacara/')
    img = qrcode.make(link)
    img.save(f'./revisisidang/qrcodeberitaacara/{kodeDosen}-{npm}-{kategori}.png')
    
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
    msgreply = f"Tanda tangan berita acara sidang *{kategori_bimbingan}* atas nama *{nama_mahasiswa}* oleh *{nama_dosen}* sebagai *{role}* dengan judul {kategori_bimbingan} *{judul}*\nPenerbitan Tanda Tangan: {sah_jam} {tanggal} {bulan} {tahun}"
    return msgreply

def makePdf(npm, kategori, tahunID, email, contain, styles):    
    noSurat = 'NO. 51/D4-TI/TA/F10/0520'    
    nip, kaProdi = getKaProdi('14')
    kaProdi = f'( {kaProdi} )'    
    tahunAjaran = f'{tahunID[:4]}/{int(tahunID[:4])+1}' # '2019/2020'
    df = pd.read_excel(f'jadwal_sidang_ta_14.xlsx')    
    listPem = ['pem3', 'pem4', 'jadwal','koor', 'jam']
    pem = df.loc[(df["npm"] == int(npm)) & (df["tahun"] == int(tahunID)), listPem].values.tolist()[0]
    
    kaprodiID = getDosenIDfromNIPY(nip)
    
    logo = "revisisidang\\logo-poltekpos.png"
    
    styleWrap = styles["BodyText"]
    styleWrap.alignment = TA_JUSTIFY
    styleWrap.fontName = 'Times'
    styleWrap.fontSize = 12
    
    dataMhs = getDataMahasiswa(npm)
    namaMhs = dataMhs[0]
    prodi = dataMhs[1]
    npmMhs = int(npm)
    
    listRevisiPenUt = listRevisiSidang(npm, tahunID, pem[0], styleWrap)
    listRevisiPenPen = listRevisiSidang(npm, tahunID, pem[1], styleWrap)
    
    tanggal = pem[2].split(',')[1].title().strip()
    waktu = pem[4]
    judul = getJudul(npm, tahunID).upper()
    
    penUtama = f'( {getDataDosen(pem[0])} )'
    penPendamping = f'( {getDataDosen(pem[1])} )'    
    koor = f'( {getDataDosen(pem[3])} )'
    
    kodeDosens = [pem[0], pem[1], pem[3], kaprodiID]
    listTTD = []
    
    for i, kodeDosen in enumerate(kodeDosens):
        if i == 0:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'pnt', tahunID)
        elif i == 1:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'pnp', tahunID)
        elif i == 2:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'kor', tahunID)
        elif i == 3:
            link = makeLinkVerifiy(kodeDosen, npm, kategori, 'kpr', tahunID)
        
        makeQrcodeLinkVerifySign(link, kodeDosen, npm, kategori)
        listTTD.append(f'{kodeDosen}-{npm}-{kategori}')
        
    
    kategori = tipeSidang(kategori)
    
    makePages(contain, logo, styles, tahunAjaran, noSurat, namaMhs, npmMhs, prodi, tanggal, penUtama, penPendamping, kaProdi, koor, kategori, listTTD, waktu, judul, listRevisiPenUt, listRevisiPenPen, styleWrap)

def checkDir(path):
    try:
        os.mkdir(path)
    except:
        pass #print('sudah ada..')

def makePages(contain, logo, styles, tahunAjaran, noSurat, namaMhs, npmMhs, prodi, tanggal, penUtama, penPendamping, kaProdi, koor, kategori, listTTD, waktu, judul, listRevisiPenUt, listRevisiPenPen, styleWrap):
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
            ['Judul', ':', Paragraph(judul, styleWrap)],
            ['Tanggal', ':', tanggal],
            ['Waktu', ':', waktu],
        ]
    table = Table(data, [5*cm, .5*cm, 12.5*cm], [.6*cm, .6*cm, 2.4*cm, .6*cm, .6*cm, ])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
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
    
    table = Table(data, [1.5*cm, 10*cm, 4*cm], len(data)*[1.5*cm])
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
    table = Table(data, [1.5*cm, 10*cm, 4*cm], len(data)*[1.4*cm])
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
    
    path = './revisisidang/qrcodeberitaacara/'
    
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
    table = Table(data, [8.5*cm, 1*cm, 8.5*cm], [.8*cm, .8*cm,.8*cm,4.5*cm,.8*cm,.8*cm,1.8*cm,4.5*cm,.8*cm])
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
        # receiver_email = 'divakrishnam@yahoo.com'
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
        if row:
            return row[0]
        else:
            return "Ini Judul"