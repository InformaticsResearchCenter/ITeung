import time
import datetime

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, cm
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors

def mainPages():
    namaFile = "perwalian.pdf"
    
    namaDeputi = 'Marwanto Rahmatuloh, ST., MT.'
    namaKaprodi = 'M. Yusril Helmi S, S.Kom., M.Kom.'    
    namaDosen = 'Rolly Maulana Awangga ST., MT'
    qrDeputi = 'logo-poltekpos.png'
    qrKaprodi = 'logo-poltekpos.png'
    qrDosen = 'logo-poltekpos.png'
    prodi = 'D4 Teknik Informatika'
    kelas = 'A'
    
    tahunAkademik = '2020 - 2021'
    hariSekarang = 'Jumat'
    tglSekarang = '21 Agustus 2020'
    jumlahMhs = '18'
    jumlahHadir = '17'
    jumlahTdkHadir = '1'
    ketuaKelas = 'Dick Grayson'
    listMasukan = [['1.', '..............................................................'],
            ['2.', '..............................................................'],
            ['3.', '..............................................................'],
        ]
    
    listMahasiswa = [
        ['1.', 'Kadek Diva Krishna Murti', '1174006', '6289677709045', 'v'],
        ['2.', 'Jason Todd', '1174000', '6282144361462', 'v'],
        ]
    
    doc = SimpleDocTemplate(namaFile,
                            pagesize=A4,
                            rightMargin=2.5*cm,
                            leftMargin=2.5*cm,
                            topMargin=2.5*cm,
                            bottomMargin=2.5*cm)
    
    contain=[]
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName='Times', fontSize=12))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontName='Times'))
    
    createBeritaAcaraPage(contain, styles, tahunAkademik, hariSekarang, tglSekarang, namaDosen, prodi, kelas, jumlahMhs, jumlahHadir, jumlahTdkHadir, listMasukan, namaDeputi, namaKaprodi, qrDeputi, qrKaprodi, qrDosen)
    createAbsensiPage(contain, styles, namaDosen, prodi, kelas, listMahasiswa, namaDeputi, namaKaprodi, qrDeputi, qrKaprodi, qrDosen)
    
    doc.build(contain)
    
def createBeritaAcaraPage(contain, styles, tahunAkademik, hariSekarang, tglSekarang, namaDosen, prodi, kelas, jumlahMhs, jumlahHadir, jumlahTdkHadir, listMasukan, namaDeputi, namaKaprodi, qrDeputi, qrKaprodi, qrDosen):
    text = '<font size="14"><b>BERITA ACARA PERWALIAN</b></font>'
    contain.append(Paragraph(text, styles["Center"]))
    contain.append(Spacer(1, .5*cm))
    
    text = f'<font size="14"><b>TAHUN AKADEMIK {tahunAkademik}</b></font>'
    contain.append(Paragraph(text, styles["Center"]))
    contain.append(Spacer(1, 1.5*cm))
    
    text = f'<font size="12">Pada hari ini {hariSekarang} tanggal {tglSekarang}, telah dilaksanakan Perwalian Tahun Akademik {tahunAkademik} dengan data sebagai berikut:</font>'
    contain.append(Paragraph(text, styles["Justify"]))
    contain.append(Spacer(1, .5*cm))
    
    data = [['Nama Dosen Wali', ':', namaDosen],
            ['Jurusan / Kelas', ':', f'{prodi} / {kelas}'],
            ['Jumlah  Mahasiswa', ':', jumlahMhs],
            ['Jumlah yang hadir', ':', jumlahHadir],
            ['Jumlah yang tidak hadir', ':', jumlahTdkHadir],
        ]
    table = Table(data, [5*cm, .5*cm, 10.5*cm], len(data)*[.6*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    text = '<font size="12">Catatan masukan dari mahasiswa :</font>'
    contain.append(Paragraph(text, styles["Justify"]))
    contain.append(Spacer(1, .1*cm))
    
    table = Table(listMasukan, [.8*cm, 15.2*cm], len(listMasukan)*[.6*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    
    
    data = [
        [Paragraph('<font size="12"><b>Dosen Wali,</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Ketua Prodi,</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Deputi Akademik,</b></font>', styles["Center"])],
        [Image(qrDeputi, 4*cm, 4*cm), Image(qrKaprodi, 4*cm, 4*cm), Image(qrDosen, 4*cm, 4*cm)],
        [Paragraph(f'<font size="12"><u>{namaDosen}</u></font>', styles["Center"]), Paragraph(f'<font size="12"><u>{namaKaprodi}</u></font>', styles["Center"]), Paragraph(f'<font size="12"><u>{namaDeputi}</u></font>', styles["Center"])],
        ]

    table = Table(data, [6.8*cm, 6.8*cm, 6.8*cm], [.6*cm, 4.5*cm, 1*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('ALIGN',(0,1),(-1,-1),'CENTER'),
    ]))
    contain.append(table)
    
    contain.append(PageBreak())

def createAbsensiPage(contain, styles, namaDosen, prodi, kelas, listMahasiswa, namaDeputi, namaKaprodi, qrDeputi, qrKaprodi, qrDosen):
    text = '<font size="14"><b>ABSENSI PERWALIAN</b></font>'
    contain.append(Paragraph(text, styles["Center"]))
    contain.append(Spacer(1, 1.5*cm))
    
    data = [['NAMA DOSEN', ':', namaDosen],
            ['PROGRAM STUDI', ':', prodi],
            ['KELAS', ':', kelas],
        ]
    table = Table(data, [5*cm, .5*cm, 10.5*cm], len(data)*[.6*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    data = [[Paragraph('<font size="12"><b>No</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Nama Mahasiswa</b></font>', styles["Center"]), Paragraph('<font size="12"><b>NPM</b></font>', styles["Center"]), Paragraph('<font size="12"><b>No Handphone<br/>E-mail</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Tanda<br/>Tangan</b></font>', styles["Center"])]]
    data.extend(listMahasiswa)
    
    table = Table(data, [1*cm, 6*cm, 2*cm, 4.5*cm, 2*cm], len(data)*[1.5*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('ALIGN',(0,1),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),
    ]))
    contain.append(table)
    contain.append(Spacer(1, .7*cm))
    
    data = [
        [Paragraph('<font size="12"><b>Dosen Wali,</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Ketua Prodi,</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Deputi Akademik,</b></font>', styles["Center"])],
        [Image(qrDeputi, 4*cm, 4*cm), Image(qrKaprodi, 4*cm, 4*cm), Image(qrDosen, 4*cm, 4*cm)],
        [Paragraph(f'<font size="12"><u>{namaDosen}</u></font>', styles["Center"]), Paragraph(f'<font size="12"><u>{namaKaprodi}</u></font>', styles["Center"]), Paragraph(f'<font size="12"><u>{namaDeputi}</u></font>', styles["Center"])],
        ]

    table = Table(data, [6.8*cm, 6.8*cm, 6.8*cm], [.6*cm, 4.5*cm, 1*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('ALIGN',(0,1),(-1,-1),'CENTER'),
    ]))
    contain.append(table)

mainPages()