from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import date
from module import kelas
from lib import numbers, message

import qrcode, config

def getTipeBimbingan(npm):
    db = kelas.dbConnectSiap()
    sql = f"select DISTINCT(tipe) from simak_croot_bimbingan where MhswID={npm}"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def getFotoRoute(npm):
    db = kelas.dbConnectSiap()
    sql = f"select Foto from simak_mst_mahasiswa where MhswID={npm}"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def getAllDataBimbingan(npm):
    db = kelas.dbConnectSiap()
    sql = f"select * from simak_croot_bimbingan where MhswID={npm} ORDER BY Pertemuan_ DESC"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if rows is not None:
            return rows
        else:
            return None


def getAllNilaiBimbingan(npm):
    db = kelas.dbConnectSiap()
    sql = f"select Nilai from simak_croot_bimbingan where MhswID={npm}"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if rows is not None:
            return rows
        else:
            return None

def totalNilai(npm, MINIMUM_PERTEMUAN):
    ALL_DATA_BIMBINGAN = getAllDataBimbingan(npm)
    ALL_NILAI_BIMBINGAN = getAllNilaiBimbingan(npm)
    LAST_PERTEMUAN_BIMBINGAN = ALL_DATA_BIMBINGAN[0][5]
    if len(ALL_DATA_BIMBINGAN) < 16:
        status, totalnilai=False, 0
    else:
        if LAST_PERTEMUAN_BIMBINGAN < MINIMUM_PERTEMUAN:
            totalnilai = 0
            for nilai in ALL_NILAI_BIMBINGAN:
                totalnilai += nilai[0]
            status, totalnilai = True, totalnilai / (MINIMUM_PERTEMUAN * 2)
        else:
            totalnilai = 0
            for nilai in ALL_NILAI_BIMBINGAN:
                totalnilai += nilai[0]
            status, totalnilai = True, totalnilai / (LAST_PERTEMUAN_BIMBINGAN * 2)
    return status, totalnilai


def getNIDNDosen(dosenid):
    db=kelas.dbConnectSiap()
    sql=f"select NIDN from simak_mst_dosen where Login='{dosenid}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def getDataBimbinganwithMhswIDandDosenID(npm, dosenid):
    db=kelas.dbConnectSiap()
    sql=f"select * from simak_croot_bimbingan where MhswID={npm} and DosenID='{dosenid}' order by Pertemuan_ desc"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            return rows
        else:
            return None


def getDataByPertemuanandNPM(npm, pertemuanke):
    db=kelas.dbConnectSiap()
    sql=f"select * from simak_croot_bimbingan where MhswID={npm} and Pertemuan_={pertemuanke} order by Pertemuan_ asc"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            return True, rows
        else:
            return False, ''


def makeListDataBimbinganByDosens(npm, kode_dosen):
    dataBimbingan=getDataBimbinganwithMhswIDandDosenID(npm, kode_dosen)
    if dataBimbingan[0][5] < 8:
        setStart=8
    else:
        setStart=dataBimbingan[0][5]
    pertemuan = 1
    databimbinganforPDF=[]
    for i in range(setStart):
        status, datawekwek=getDataByPertemuanandNPM(npm, pertemuan)
        if status:
            data=[]
            data.append(str(pertemuan))
            data.append(datawekwek[8].strftime('%d-%m-%Y'))
            data.append(datawekwek[7].split(';')[0])
            data.append(datawekwek[7].split(';')[1])
            data.append(str(datawekwek[6]))
            databimbinganforPDF.append(data)
        else:
            data=[]
            data.append(str(pertemuan))
            data.append('-')
            data.append('-')
            data.append('-')
            data.append('-')
            databimbinganforPDF.append(data)
        pertemuan+=1
    return databimbinganforPDF


def makeQrcode(data, npm_mahasiswa):
    img = qrcode.make(data)
    img.save(f"{npm_mahasiswa}.PNG")


def switcherTipeBimbingan(tipe):
    switcher = {
        'ta': 'TUGAS AKHIR',
        'i1': 'INTERNSHIP I',
        'i2': 'INTERNSHIP II',
        'p1': 'PROYEK I',
        'p2': 'PROYEK II',
        'p3': 'PROYEK III',
    }
    return switcher.get(tipe, "Not Found!!")


def replymsg(data, driver):
    num = numbers.normalize(data[0])
    msg = data[1]
    msg = message.normalize(msg)
    studentid,studentname=kelas.getNpmandNameMahasiswa(num)
    status_nilai, nilai_total=True, 100
    # status_nilai, nilai_total=totalNilai(npm, config.MINIMUM_PERTEMUAN_BIMBINGAN)
    if status_nilai:
        WRONG_KEYWORD = False
        try:
            KODE_DOSEN_1 = msg.split(' kode dosen 1 ')[1].split(' ')[0]
            KODE_DOSEN_2 = msg.split(' kode dosen 2 ')[1]
            JUDUL_BIMBINGAN = data[1].split(' kambing ')[1].split(' kode dosen 1 ')[0]
        except:
            WRONG_KEYWORD = True
        if WRONG_KEYWORD:
            msgreply = 'ada yang salah keywordnya'
        else:
            NAMA_DOSEN_1 = kelas.getNamaDosen(KODE_DOSEN_1)
            NAMA_DOSEN_2 = kelas.getNamaDosen(KODE_DOSEN_2)
            NIDN_DOSEN_1 = getNIDNDosen(KODE_DOSEN_1)
            NIDN_DOSEN_2 = getNIDNDosen(KODE_DOSEN_2)
            TAHUN_AJARAN = kelas.getTahunAjaran(kelas.getProdiIDwithStudentID(studentid)).split(' ')[-1]
            photo = f'{config.link_foto_siap}{getFotoRoute(studentid)}'
            makePdf(
                npm_mahasiswa=studentid,
                nama_mahasiswa=studentname,
                tipe_bimbingan=switcherTipeBimbingan(getTipeBimbingan(studentid)),
                nama_pembimbing_1=NAMA_DOSEN_1,
                kode_dosen_pembimbing_1=KODE_DOSEN_1,
                kode_dosen_pembimbing_2=KODE_DOSEN_2,
                nama_pembimbing_2=NAMA_DOSEN_2,
                nidn_pembimbing_1=NIDN_DOSEN_1,
                nidn_pembimbing_2=NIDN_DOSEN_2,
                tahun_ajaran=TAHUN_AJARAN,
                photo=photo,
                judul=JUDUL_BIMBINGAN,
                total_nilai=str(nilai_total)
            )
            msgreply=f"{photo}"
    else:
        msgreply=f'mohon maaf belum bisa cetak kartu bimbingan dikarenakan pertemuan masih ada yang kurang dari 8'
    return msgreply

def makePdf(npm_mahasiswa, nama_mahasiswa, tipe_bimbingan, kode_dosen_pembimbing_1, kode_dosen_pembimbing_2, nama_pembimbing_1, nama_pembimbing_2, nidn_pembimbing_1, nidn_pembimbing_2, tahun_ajaran, photo, judul, total_nilai):
    qrdata='12345678900123809128390092340923890482390840928349082309482093849023894082309842093849283904809238490283094829034890238409283904829304892038490283094823948290348092384231209381023'
    makeQrcode(qrdata, "1184047")
    d2=date.today().strftime('%d %B %Y')
    doc = SimpleDocTemplate(f'{npm_mahasiswa}.pdf', pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    doc.pagesize = portrait(A4)
    elements = []

    logo = Image("logo.png", 3.5 * inch, 1 * inch)
    logo.hAlign = "LEFT"
    elements.append(logo)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

    ptext = '<font name="Times" size="14">FORMULIR KEGIATAN</font>'
    elements.append(Paragraph(ptext, styles["Center"]))
    elements.append(Spacer(1, 12))

    ptext = f'<font name="Times" size="14">{tipe_bimbingan}</font>'
    elements.append(Paragraph(ptext, styles["Center"]))
    elements.append(Spacer(1, 12))

    ptext = '<font name="Times" size="14">TA. ' + tahun_ajaran + '</font>'
    elements.append(Paragraph(ptext, styles["Center"]))
    elements.append(Spacer(1, 0.5 * inch))

    image = Image(photo, 1.1 * inch, 1.5 * inch)
    image.hAlign = "RIGHT"
    elements.append(image)
    elements.append(Spacer(1, 1.5 * inch))

    ptext = '<font size=12> </font>'
    elements.append(Paragraph(ptext, styles["Center"]))
    elements.append(Spacer(1, -3 * inch))

    table = [['<font name="Times" size="12">Nama</font>', '<font name="Times" size="12">: ' + nama_mahasiswa + '</font>'],
             ['<font name="Times" size="12">Npm</font>', '<font name="Times" size="12">: ' + npm_mahasiswa + '</font>'],
             ['<font name="Times" size="12">Judul</font>', '<font name="Times" size="12">: ' + judul + '</font>'],
             ['<font name="Times" size="12">Pembimbing</font>',
              '<font name="Times" size="12">: ' + nama_pembimbing_1 + '</font>']]

    style = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                        ('VALIGN', (0, 0), (0, -1), 'TOP'),
                        ('ALIGN', (0, -1), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE')
                        ])

    s = getSampleStyleSheet()
    s = s["BodyText"]
    s.wordWrap = 'CJK'
    data1 = [[Paragraph(cell, s) for cell in row] for row in table]
    tab = Table(data1, hAlign='LEFT', colWidths=[75, 290])
    tab.setStyle(style)

    elements.append(tab)
    elements.append(Spacer(1, 0.6 * inch))

    data = [['Pertemuan', 'Tanggal', 'Sudah Dikerjakan', 'Pekerjaan Selanjutnya', 'Nilai']]
    inner_data_list=makeListDataBimbinganByDosens(npm_mahasiswa, kode_dosen_pembimbing_1)
    for i in inner_data_list:
        data.append(i)
    nilai_data_list=['', '', '', 'Rata-Rata: ', total_nilai]
    data.append(nilai_data_list)

    # Get this line right instead of just copying it from the docs
    style = TableStyle([('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                        ('VALIGN', (0, 0), (0, -1), 'MIDDLE'),
                        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                        ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('INNERGRID', (0, 0), (-1, -1), 0.50, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                        ])

    # Configure style and word wrap
    s = getSampleStyleSheet()
    s = s["Normal"]
    s.wordWrap = 'CJK'
    data2 = [[Paragraph(cell, s) for cell in row] for row in data]
    t = Table(data2, hAlign='CENTER', colWidths=[62.5, 65, 180, 180, 40])
    t.setStyle(style)

    elements.append(t)
    elements.append(Spacer(1, 10))

    ptext = '<font size=12> </font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, .5 * inch))

    ptext = '<font name="Times" size="12">Bandung, ' + d2 + '</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, 12))

    ptext = '<font name="Times" size="12">Pembimbing,</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, .1 * inch))

    qrcode = f"./{npm_mahasiswa}.png"
    im = Image(qrcode, 1.5 * inch, 1.5 * inch)
    im.hAlign = "RIGHT"
    elements.append(im)

    ptext = '<font name="Times" size="12">' + nama_pembimbing_1 + '</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, 1))

    ptext = '<font name="Times" size="12">NIDN. ' + nidn_pembimbing_1 + '</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, 12))

    doc.build(elements)

data=['6285155494985', 'iteung minta kambing WANDA (WhatsApp Tanpa Derita) kode dosen NN257L']
result=replymsg(data, '')
print(result)