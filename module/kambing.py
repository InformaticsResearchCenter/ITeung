from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import date
from module import kelas, bkd, approve_kambing
from lib import numbers
from datetime import datetime
from Crypto.Cipher import AES

import qrcode, config, os

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
        print(rows)
        if rows is not None:
            return rows
        else:
            return None


def getDataByPertemuanandNPM(npm, pertemuanke, kode_dosen):
    db=kelas.dbConnectSiap()
    sql=f"select * from simak_croot_bimbingan where MhswID={npm} and Pertemuan_={pertemuanke} and DosenID='{kode_dosen}'"
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
        status, datawekwek=getDataByPertemuanandNPM(npm, pertemuan, kode_dosen)
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


def getStudentEmail(npm):
    db = kelas.dbConnectSiap()
    sql = f"select Email from simak_mst_mahasiswa where MhswID={npm}"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


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


def getKodeDosenBimbingan(npm):
    db = kelas.dbConnect()
    sql = f"select pembimbing1, pembimbing2 from bimbingan_data where npm={npm}"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row
        else:
            return None


def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) == None:
        ret = False
    else:
        ret = True
    return ret


def replymsg(driver, data):
    num = numbers.normalize(data[0])
    studentid,studentname=kelas.getNpmandNameMahasiswa(num)
    # status_nilai, nilai_total=True, 100
    statusapprovalkambing = cekApprovalKambingAtBeginning(studentid)
    if statusapprovalkambing is not None:
        if 'false' in statusapprovalkambing or '' in statusapprovalkambing:
            msgreply='wiwiwiwiwi KAMBING kamu belum di approve nih sama Bapak/Ibu dosen yang ini nih:'
            if 'false' == statusapprovalkambing[0] or '' == statusapprovalkambing[0]:
                kodedosen1=getKodeDosenBimbingan(studentid)[0]
                namadosen=kelas.getNamaDosen(kodedosen1)
                msgreply+=f'\n{kodedosen1} | {namadosen} | PEMBIMBING 1'
            if 'false' == statusapprovalkambing[1] or '' == statusapprovalkambing[1]:
                kodedosen1 = getKodeDosenBimbingan(studentid)[1]
                namadosen = kelas.getNamaDosen(kodedosen1)
                msgreply += f'\n{kodedosen1} | {namadosen} | PEMBIMBING 2'
        else:
            status_nilai, nilai_total=totalNilai(studentid, config.MINIMUM_PERTEMUAN_BIMBINGAN)
            if status_nilai:
                WRONG_KEYWORD = False
                try:
                    JUDUL_BIMBINGAN = data[3].split(' kambing ')[1]
                except:
                    WRONG_KEYWORD = True
                if WRONG_KEYWORD:
                    msgreply = 'ada yang salah keywordnya'
                else:
                    KODE_DOSEN_BIMBINGAN=getKodeDosenBimbingan(studentid)
                    if KODE_DOSEN_BIMBINGAN is None:
                        msgreply=f'data dengan npm {studentid} tidak ditemukan'
                    else:
                        for KODE_DOSEN in KODE_DOSEN_BIMBINGAN:
                            NAMA_DOSEN = kelas.getNamaDosen(KODE_DOSEN)
                            print(NAMA_DOSEN)
                            NIDN_DOSEN = getNIDNDosen(KODE_DOSEN)
                            TAHUN_AJARAN = kelas.getTahunAjaran(kelas.getProdiIDwithStudentID(studentid)).split(' ')[-1]
                            photo = f'{config.link_foto_siap}{getFotoRoute(studentid)}'
                            makePdf(
                                npm_mahasiswa=studentid,
                                nama_mahasiswa=studentname,
                                tipe_bimbingan=switcherTipeBimbingan(getTipeBimbingan(studentid)),
                                nama_pembimbing=NAMA_DOSEN,
                                kode_dosen_pembimbing=KODE_DOSEN,
                                nidn_pembimbing=NIDN_DOSEN,
                                tahun_ajaran=TAHUN_AJARAN,
                                photo=photo,
                                judul=JUDUL_BIMBINGAN,
                                total_nilai=str(nilai_total)
                            )
                        bkd.mail(kelas.getDataMahasiswa(studentid)[3],
                                 f'eyyowwwwwww {config.bot_name} nihhhh mau nganter file yang kamu mintaaa',
                                 f'ini ya file KAMBING (Kartu Bimbingan) yang Akang/Teteh minta silahkan di cek... ehee....',
                                 bkd.getFilePath(kelas.getDataMahasiswa(studentid)[3], 'kambing'))
                        msgreply=f"sudah selesai dan sudah dikirim ke email kamu yang {kelas.getDataMahasiswa(studentid)[3]} yaa...."
            else:
                msgreply=f'mohon maaf belum bisa cetak kartu bimbingan dikarenakan pertemuan masih ada yang kurang dari 8'
    else:
        msgreply=f'mohon maaf data dengan npm {studentid} tidak bisa ditemukan'
    return msgreply


def cekApprovalKambingAtBeginning(npm):
    db=kelas.dbConnect()
    sql=f'select approval_pembimbing1, approval_pembimbing2 from bimbingan_data where npm={npm}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row
        else:
            return None


def makePdf(npm_mahasiswa, nama_mahasiswa, tipe_bimbingan, kode_dosen_pembimbing, nama_pembimbing, nidn_pembimbing,  tahun_ajaran, photo, judul, total_nilai):
    checkDir()
    makeQrcodeVerifySign(
        link=makeLinkVerify(kode_dosen=kode_dosen_pembimbing,
                            npm_mahasiswa=npm_mahasiswa,
                            tipe_bimbingan=tipe_bimbingan,
                            total_nilai=total_nilai),
        kode_dosen=kode_dosen_pembimbing,
        npm_mahasiswa=npm_mahasiswa,
        tipe_bimbingan=tipe_bimbingan
    )
    bulan = date.today().strftime("%m")
    d2 = date.today().strftime(f"%d {bkd.bulanSwitcher(bulan)} %Y")
    STUDENT_EMAIL=getStudentEmail(npm_mahasiswa)
    doc = SimpleDocTemplate(f'./kambing/{npm_mahasiswa}-{kode_dosen_pembimbing}-{STUDENT_EMAIL}.pdf', pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    doc.pagesize = portrait(A4)
    elements = []

    logo = Image("logoKAMBING.png", 3.5 * inch, 1 * inch)
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
              '<font name="Times" size="12">: ' + nama_pembimbing + '</font>']]

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
    inner_data_list=makeListDataBimbinganByDosens(npm_mahasiswa, kode_dosen_pembimbing)
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

    data = approve_kambing.getDataPembimbing(npm_mahasiswa, kode_dosen_pembimbing)
    pembimbingke = approve_kambing.pembimbingPositionAs(data, kode_dosen_pembimbing)
    if approve_kambing.cekApprovalTrueorFalse(npm_mahasiswa, pembimbingke):
        qrcode = f"./kambingqrcode/{npm_mahasiswa}-{kode_dosen_pembimbing}-{tipe_bimbingan}.png"
    else:
        qrcode = f"./kambingqrcode/whiteimage.png"
    im = Image(qrcode, 1.5 * inch, 1.5 * inch)
    im.hAlign = "RIGHT"
    elements.append(im)

    ptext = '<font name="Times" size="12">' + nama_pembimbing + '</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, 1))

    ptext = '<font name="Times" size="12">NIDN. ' + nidn_pembimbing + '</font>'
    elements.append(Paragraph(ptext, styles["Right"]))
    elements.append(Spacer(1, 12))

    doc.build(elements)


def makeLinkVerify(kode_dosen, npm_mahasiswa, tipe_bimbingan, total_nilai):
    datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
    timenow = datetime.now().time().strftime('%H:%M:%S')
    module_name="kambing"
    data = f'{module_name};{datenow};{timenow};{kode_dosen};{npm_mahasiswa};{tipe_bimbingan};{total_nilai};'
    makeit64 = f'{data}{bkd.randomString(64 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit64.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link


def makeQrcodeVerifySign(link, npm_mahasiswa, kode_dosen, tipe_bimbingan):
    checkDirQrcode()
    img = qrcode.make(link)
    img.save(f'./kambingqrcode/{npm_mahasiswa}-{kode_dosen}-{tipe_bimbingan}.PNG')


def verifyDigitalSign(resultpasscode):
    resultpasscode=resultpasscode.split(';')
    tanggal=resultpasscode[1].split('-')[0]
    bulan=bkd.bulanSwitcher(resultpasscode[1].split('-')[1])
    tahun=resultpasscode[1].split('-')[2]
    sah_jam=resultpasscode[2]
    nama_dosen=kelas.getNamaDosen(resultpasscode[3])
    npm_mahasiswa=resultpasscode[4]
    kode_tipe_bimbingan=switcherTipeBimbingantoKode(resultpasscode[5])
    total_nilai=resultpasscode[6]
    msgreply = f"Ini data yang diminta yaaaa\n\nNama Dosen: {nama_dosen}\nPenerbitan Tanda Tangan: {sah_jam} {tanggal} {bulan} {tahun}"
    for i in getDataBimbinganForReply(npm_mahasiswa, resultpasscode[3]):
        msgreply+=f"\n\nPertemuan: {i[0]}\nTanggal: {i[1].strftime('%d-%m-%Y')}\nSudah Dikerjakan: {i[2].split(';')[0]}\nPekerjaan Selanjutnya: {i[2].split(';')[1]}\nNilai: {i[3]}"
    msgreply+=f'\n\n*Nilai Rata-Rata _{total_nilai}_*'
    return msgreply


def switcherTipeBimbingantoKode(tipe_bimbingan):
    switcher = {
        "TUGAS AKHIR": "ta",
        "INTERNSHIP I": "i1",
        "INTERNSHIP II": "i2",
        "PROYEK I": "p1",
        "PROYEK II": "p2",
        "PROYEK III": "p3",
    }
    return switcher.get(tipe_bimbingan, 'NOT FOUND!!')

def checkDir():
    try:
        os.mkdir('kambing/')
    except:
        print('sudah ada..')


def checkDirQrcode():
    try:
        os.mkdir('kambingqrcode/')
    except:
        print('sudah ada..')


def getDataBimbinganForReply(npm, kode_dosen):
    db=kelas.dbConnectSiap()
    sql=f"select Pertemuan_, Tanggal, Topik, Nilai from simak_croot_bimbingan where MhswID={npm} and DosenID='{kode_dosen}' order by Pertemuan_ asc"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows == ():
            return None
        else:
            return rows