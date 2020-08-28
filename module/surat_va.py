from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, inch, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

from module import kelas, bkd

import config

def getPekerjaanOrtuAyah(npm):
    db=kelas.dbConnectSiap()
    sql=f'select Nama from simak_ref_pekerjaan_ortu where Pekerjaan=(select PekerjaanAyah from simak_mst_mahasiswa where MhswID={npm})'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
    return rows[0]

def getPekerjaanOrtuIbu(npm):
    db=kelas.dbConnectSiap()
    sql=f'select Nama from simak_ref_pekerjaan_ortu where Pekerjaan=(select PekerjaanIbu from simak_mst_mahasiswa where MhswID={npm})'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
    return rows[0]

def getAlamatLengkapOrtu(npm):
    db=kelas.dbConnectSiap()
    sql=f'select AlamatOrtu, RTOrtu, RWOrtu, KotaOrtu, PropinsiOrtu, KodePosOrtu, NegaraOrtu from simak_mst_mahasiswa where MhswID={npm}'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
    return f'{rows[0]}, RT{rows[1]}/RW{rows[2]}, {rows[3]}, {rows[4]}, {rows[5]}, {rows[6]}'

def makePdfAndSendToEmail(npm):
    foldername='suratva'
    doc = SimpleDocTemplate(f'./{foldername}/SURAT PERNYATAAN-{npm}.pdf', pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    doc.pagesize = portrait(A4)
    elements = []
    for i in range(2):
        namaOrtu=kelas.getParentNamefromStudentID(npm)[i]
        noTelp=kelas.getParentTelpNumberandHandphoneNumber(npm)[0]
        noHandphone=kelas.getParentTelpNumberandHandphoneNumber(npm)[1]
        emailOrtu=kelas.getParentEmailfromStudentID(npm)
        if i == 0:
            pekerjaanOrtu=getPekerjaanOrtuAyah(npm)
        else:
            pekerjaanOrtu=getPekerjaanOrtuIbu(npm)
        alamatLengkapOrtu=getAlamatLengkapOrtu(npm)
        hari=datetime.now().strftime('%d')
        bulan=bkd.bulanSwitcher(datetime.now().strftime('%m'))
        tahun=datetime.now().strftime('%Y')

        logo = Image("logo.png", 7.3 * inch, 1 * inch)
        logo.hAlign = "CENTER"
        elements.append(logo)

        pdfmetrics.registerFont(TTFont('TNR', 'timesdownload.ttf'))
        pdfmetrics.registerFont(TTFont('TNRB', 'timesdownloadbd.ttf'))

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='surat_pernyataan_style', fontName="TNRB", fontSize=16, alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Times', fontName="TNR"))

        ptext = '<font>SURAT PERNYATAAN</font>'
        elements.append(Paragraph(f'<u>{ptext}</u>', styles["surat_pernyataan_style"]))
        elements.append(Spacer(1, 35))

        ptext = f'<font name="Times" size="10">Yang bertanda tangan di bawah ini :</font>'
        elements.append(Paragraph(ptext, styles["Justify"]))
        elements.append(Spacer(1, 8))

        data= [
            [f'<font name="Times" size="10">Nama</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{namaOrtu}</font>'],
            [f'<font name="Times" size="10">KTP</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">1234567890</font>'],
            [f'<font name="Times" size="10">No. Telepon</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{noTelp}</font>'],
            [f'<font name="Times" size="10">No. HP/WA</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{noHandphone}</font>'],
            [f'<font name="Times" size="10">Alamat E-mail</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{emailOrtu}</font>'],
            [f'<font name="Times" size="10">Pekerjaan</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{pekerjaanOrtu}</font>'],
            [f'<font name="Times" size="10">Alamat</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{alamatLengkapOrtu}</font>'],
            [f'<font name="Times" size="10">Lampiran</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">FC KTP dan KK orang tua/Wali (Wajib)</font>']
        ]
        style = TableStyle(
            [
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]
        )
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data1 = [[Paragraph(cell, s) for cell in row] for row in data]
        tab = Table(data1, hAlign='LEFT', colWidths=[3*cm, .5*cm, 10*cm])
        tab.setStyle(style)

        elements.append(tab)
        elements.append(Spacer(1, 0.35 * inch))

        ptext = f'<font name="Times" size="10">Adalah orang tua/wali dari Mahasiswa Politeknik Pos Indonesia :</font>'
        elements.append(Paragraph(ptext, styles["Justify"]))
        elements.append(Spacer(1, 8))

        data= [
            [f'<font name="Times" size="10">Nama</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{kelas.getStudentNameOnly(npm)}</font>'],
            [f'<font name="Times" size="10">NPM</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{npm}</font>'],
            [f'<font name="Times" size="10">No. HP</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{kelas.getStudentPhoneNumberFromNPM(npm)}</font>'],
            [f'<font name="Times" size="10">Alamat E-mail</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{kelas.getStudentEmail(npm)}</font>'],
            [f'<font name="Times" size="10">Prodi/Kelas</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{kelas.getProdiNameWithStudentID(npm)}/{kelas.getKelasMahasiswabyStudentID(npm)}</font>'],
            [f'<font name="Times" size="10">Angkatan</font>', '<font name="Times" size="10">:</font>', f'<font name="Times" size="10">{kelas.getTahunAngkatanWithStudentID(npm)}</font>'],
        ]
        style = TableStyle(
            [
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]
        )
        s = getSampleStyleSheet()
        s = s["BodyText"]
        s.wordWrap = 'CJK'
        data1 = [[Paragraph(cell, s) for cell in row] for row in data]
        tab = Table(data1, hAlign='LEFT', colWidths=[3*cm, .5*cm, 10*cm])
        tab.setStyle(style)

        elements.append(tab)
        elements.append(Spacer(1, 0.25 * inch))

        ptext = f'<font name="Times" size="10">Dengan ini telah melakukan pembayaran sebesar Rp. .................................................................... (.............................................................................) serta menyatakan akan melunasi sisa kewajiban pembayaran uang SPP/Variabel/Tugas Akhir/PKL sebesar Rp. (...............................................................................) Paling lambat tanggal ...........................................................................</font>'
        elements.append(Paragraph(ptext, styles["Justify"]))
        elements.append(Spacer(1, 6))

        ptext = f'<font name="Times" size="10">Demikian surat pernyataan ini saya buat dengan sebenarnya untuk dipergunakan sebagaimana mestinya. Apabila saya melalaikan surat pernyataan ini, maka saya bersedia menerima sanksi sesuai dengan ketentuan yang berlaku di Politeknik Pos Indonesia.</font>'
        elements.append(Paragraph(ptext, styles["Justify"]))
        elements.append(Spacer(1, 12.5))

        data = [
            ['', '', Paragraph(f'<font name="Times">Bandung, {hari} {bulan} {tahun}</font>', styles["Center"])],
            [Paragraph(f'<font name="Times">Mengetahui,</font>', styles["Justify"]), '', Paragraph(f'<font name="Times">Yang Membuat Pernyataan,</font>', styles["Center"])],
            [Paragraph('<font name="Times">Dosen Wali</font>', styles["Justify"]), '',Paragraph('<font name="Times">Orang Tua/Wali</font>', styles["Center"])],
            ['', '', ''],
            ['', '', Paragraph('<font name="Times">Materai</font>', styles["Center"])],
            ['', '', ''],
            [Paragraph(f'<font name="Times">{kelas.getNamaDosen(kelas.getPenasehatAkademik(npm))}</font>', styles["Justify"]), '',Paragraph(f'<font name="Times">{namaOrtu}</font>', styles["Center"])],
            ['', Paragraph('<font name="Times">Menyetujui,</font>', styles["Center"]), ''],
            ['', Paragraph('<font name="Times">Wadir 2 / Ka. BAUK</font>', styles["Center"]), ''],
            ['', '', ''],
            ['', Paragraph('<font name="Times">...........................................</font>', styles["Center"]), ''],
        ]
        table = Table(data, [7*cm, 4.3*cm, 7*cm], [1*cm, .5*cm, .5*cm, .65*cm, .4*cm, .65*cm, .5*cm, .5*cm, .5*cm, 1.7*cm, .5*cm])
        table.setStyle(TableStyle([
            ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ]))
        elements.append(table)
    doc.build(elements)
    bkd.mail(
        kelas.getStudentEmail(npm),
        f'eyyyyooww {config.bot_name} kirim file SURAT PERNYATAAN PENGANGGUHAN SPP/VARIABEL nihhh',
        f'coba dicek dulu ya datanya, jika belum benar, coba cek SIAP-nya ya ubah lagi datanya, terus minta lagi ke {config.bot_name}, untuk surat pernyataannya',
        f'suratva/SURAT PERNYATAAN-{npm}.pdf'
    )