from module import kelas
from module import bkd
from module import absensi_cb_mulai

from lib import numbers

from datetime import datetime
from datetime import date

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.platypus import Image
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import inch
from reportlab.lib.pagesizes import portrait
from reportlab.pdfbase.ttfonts import TTFont

from Crypto.Cipher import AES

import config
import os
import qrcode

def auth(data):
    if numbers.normalize(data[0]) in config.nomor_koor_pleton_cb:
        return True
    else:
        return False

def replymsg(driver, data):
    grp=data[1]
    msg=data[3]
    try:
        materi=msg.split(' materi ')[1]
    except:
        return 'duhh materinya mana nihhh'
    kode_pleton=grp.split("-")[1]
    nama_pleton=absensi_cb_mulai.pletonSwitcher(kode_pleton)
    npm_koor=kelas.getNpmandNameMahasiswa(data[0])[0]
    msgreply=makePDFandSEND(
        kode_pleton=kode_pleton,
        nama_pleton=nama_pleton,
        group_name=grp,
        materi=materi,
        npm_koor_pleton=npm_koor
    )
    msgreply+=f'\nsudah {config.bot_name} kirim absensi PDF ke email {kelas.getStudentEmail(kelas.getNpmandNameMahasiswa(data[0])[0])} yaa...'
    return msgreply

def makeLinkVerifiy(npm_koor_pleton):
    datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
    tanggal = datenow.split('-')[0]
    bulan = datenow.split('-')[1]
    tahun = datenow.split('-')[2]
    jam = datetime.now().time().strftime('%H')
    menit = datetime.now().time().strftime('%M')
    detik = datetime.now().time().strftime('%S')
    jenisdokumen='Absensi Peserta Character Building 2020'
    module_name='absensi_cb_selesai'
    data = f'{module_name};{npm_koor_pleton};{tanggal};{bulan};{tahun};{jam};{menit};{detik};{jenisdokumen};'
    makeitfit = f'{data}{bkd.randomString(96 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeitfit.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link

def verifyDigitalSign(resultpasscode):
    npm_koor_pleton = resultpasscode.split(';')[1]
    tglttd = resultpasscode.split(';')[2]
    blnttd = resultpasscode.split(';')[3]
    thnttd = resultpasscode.split(';')[4]
    jamttd = resultpasscode.split(';')[5]
    mntttd = resultpasscode.split(';')[6]
    dtkttd = resultpasscode.split(';')[7]
    jnsdkm = resultpasscode.split(';')[8]
    data_koor_pleton = kelas.getDataMahasiswa(npm_koor_pleton)
    penerbitantandatangan = f'{jamttd}:{mntttd}:{dtkttd} {tglttd} {bkd.bulanSwitcher(blnttd)} {thnttd}'
    nama_koor_pleton = kelas.getStudentNameOnly(npm_koor_pleton)
    msgreply = f'Ini yaaa data yang Akang/Teteh minta\n\nNPM: {npm_koor_pleton}\nNama Mahasiswa: {nama_koor_pleton}\nHandphone: {data_koor_pleton[2]}\nE-mail: {data_koor_pleton[3]}\n\nJenis Dokumen: {jnsdkm}\nPenerbitan Tanda Tangan: {penerbitantandatangan}'
    return msgreply

def checkDirQrcode(folder_name):
    try:
        os.mkdir(f'{folder_name}/')
    except:
        pass

def makeQrcodeLinkVerifySign(link, npm_koor_pleton, kode_pleton, nama_pleton):
    checkDirQrcode('absensi_cb_qrcode')
    img = qrcode.make(link)
    path_qrcode=f'./absensi_cb_qrcode/{npm_koor_pleton}-{kode_pleton}-{nama_pleton}.png'
    img.save(path_qrcode)
    return path_qrcode

def checkDir(folder_name):
    try:
        os.mkdir(f'{folder_name}/')
    except:
        pass

def getFilePath(email, folder, kode_pleton, nama_pleton, npm_koor_pleton):
    resultpath = []
    devpath = os.getcwd()
    path = '.\\{folder}'.format(folder=folder)
    for root, dirs, files in os.walk(path):
        for i in files:
            if email in i and kode_pleton in i and nama_pleton in i and npm_koor_pleton in i:
                rootpath = os.path.join(root, i)
                resultpath.append(os.path.join(devpath, rootpath))
    return resultpath


def header_footer(canvas, doc):
    canvas.saveState()

    footer = Image('./skpi/footer.png', 19 * cm, 2.5 * cm)
    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)

    canvas.restoreState()

def makePDFandSEND(kode_pleton, nama_pleton, group_name, materi, npm_koor_pleton):
    folder_name='absensi_cb'
    checkDir(folder_name)
    doc = SimpleDocTemplate(f'./{folder_name}/ABSENSI-CB-PLETON-{npm_koor_pleton}-{kode_pleton}-{nama_pleton}-{kelas.getStudentEmail(npm_koor_pleton)}.pdf', pagesize=letter, leftMargin=30, rightMargin=30, topMargin=.1, bottomMargin=130)
    doc.pagesize = portrait(A4)

    elements = []

    elements.append(Image(f'./skpi/header.png', 19 * cm, 2.5 * cm))
    elements.append(Spacer(1, 0 * cm))

    absensi_from_log = kelas.getnumonly(groupname=group_name, tipe='daring')
    npm_and_nama = []
    for phone_number in absensi_from_log:
        peserta_cb_phone_number = numbers.normalize(phone_number[0])
        if peserta_cb_phone_number in config.nomor_koor_pleton_cb:
            continue
        else:
            npm_nama = kelas.getNpmandNameMahasiswa(peserta_cb_phone_number)
            npm_and_nama.append(npm_nama)

    pdfmetrics.registerFont(TTFont('TNR', 'timesdownload.ttf'))
    pdfmetrics.registerFont(TTFont('TNRB', 'timesdownloadbd.ttf'))

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name='absensi_cb_style', fontName="TNRB", fontSize=14, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Times', fontName="TNR"))

    ptext = '<font>ABSENSI CHARACTER BUILDING 2020</font>'
    elements.append(Paragraph(f'{ptext}', styles["absensi_cb_style"]))
    elements.append(Spacer(1, 35))

    waktu_tanggal=datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    data = [
        [f'<font name="Times" size="10">Kode Pleton</font>', f'<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{kode_pleton}</font>', f'<font name="Times" size="10">Nama Pleton</font>', f'<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{nama_pleton}</font>'],
        [f'<font name="Times" size="10">Materi</font>', f'<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{materi}</font>', f'<font name="Times" size="10">Tanggal dan Waktu</font>', f'<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{waktu_tanggal}</font>'],
    ]

    style = TableStyle(
        [
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]
    )
    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    data1 = [[Paragraph(cell, s) for cell in row] for row in data]
    tab = Table(data1, hAlign='CENTER', colWidths=[2.5*cm, .5*cm, 4.5*cm, 4*cm, .5*cm, 4.5*cm])
    tab.setStyle(style)

    elements.append(tab)
    elements.append(Spacer(1, 0.35 * inch))

    data = [['Nomor', 'NPM', 'Nama', 'Program Studi']]
    nomor=1
    for npmnama in npm_and_nama:
        if npmnama:
            data_for_append=[]
            data_for_append.append(f'{str(nomor)}.')
            data_for_append.append(npmnama[0])
            data_for_append.append(npmnama[1])
            data_for_append.append(kelas.getProdiNameWithStudentID(npmnama[0]))
            data.append(data_for_append)
            nomor+=1
        else:
            continue

    style = TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                        ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                        ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                        ])

    s = getSampleStyleSheet()
    s = s["Normal"]
    s.wordWrap = 'CJK'
    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
    t = Table(data2, hAlign='CENTER', colWidths=[1.5 * cm, 2 * cm, 8 * cm, 6 * cm])
    t.setStyle(style)

    elements.append(t)
    elements.append(Spacer(1, 10))

    ptext = '<font size=10> </font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, .5 * inch))

    bulan = date.today().strftime("%m")
    d2 = date.today().strftime(f"%d {bkd.bulanSwitcher(bulan)} %Y")

    ptext = '<font name="Times" size="10">Bandung, ' + d2 + '</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, 12))

    ptext = '<font name="Times" size="10">Koordinator Pleton,</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, .1 * inch))

    qrcode_path=makeQrcodeLinkVerifySign(link=makeLinkVerifiy(npm_koor_pleton), nama_pleton=nama_pleton, kode_pleton=kode_pleton, npm_koor_pleton=npm_koor_pleton)
    im = Image(qrcode_path, 1.5 * inch, 1.5 * inch)
    im.hAlign = "RIGHT"
    elements.append(im)

    ptext = '<font name="Times" size="10">' + kelas.getStudentNameOnly(npm_koor_pleton) + '</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, 1))

    ptext = '<font name="Times" size="10">NIM. ' + npm_koor_pleton + '</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, 1))

    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)

    bkd.mail(
        kelas.getStudentEmail(npm_koor_pleton),
        f'Halooooo, {config.bot_name} ngirim file nich....',
        f'ini ya file Absensi Character Building 2020 yang Akang/Teteh minta silahkan di cek... ehee....',
        getFilePath(
            kelas.getStudentEmail(npm_koor_pleton),
            folder_name,
            kode_pleton,
            nama_pleton,
            npm_koor_pleton
        )
    )

    msgreply = f'Kode Pleton: {kode_pleton}\n' \
               f'Nama Pleton: {nama_pleton}\n' \
               f'Materi: {materi}\n' \
               f'Koordinator Pleton: {kelas.getStudentNameOnly(npm_koor_pleton)}\n' \
               f'Tanggal dan Waktu: {waktu_tanggal}\n' \
               f'Absensi Peserta CB:\n'
    number = 1
    for data_npm_nama in npm_and_nama:
        if data_npm_nama:
            msgreply += f'{number}. {data_npm_nama[0]} - {data_npm_nama[1]}\n'
            number += 1
        else:
            continue
    return msgreply