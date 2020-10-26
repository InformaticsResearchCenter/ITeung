from datetime import datetime

from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors

from module import kelas
from module import bkd
from module import perwalian_mulai

from lib import sql_to_dictionary

from Crypto.Cipher import AES

import config
import string
import random
import qrcode

import os

def auth(data):
    if kelas.getKodeDosen(data[0]):
        return True
    else:
        return False

def getDosenDataDictionaryDump(kode_dosen):
    db=kelas.dbConnectSiap()
    sql=f'select * from simak_mst_dosen where Login="{kode_dosen}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        return sql_to_dictionary.fetchOneMode(data, cur)

def daysEnToInd(day):
    switcher = {
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    return switcher.get(day, None)

def catatanToList(catatan):
    data=[]
    nomor_urut=1
    for i in catatan.split(', '):
        data_i=[]
        data_i.append(f'{nomor_urut}.')
        data_i.append(i)
        data.append(data_i)
        nomor_urut+=1
    return data

def hadirAbsensiData(group_name, tipe):
    data=kelas.getnumonly(group_name, tipe)
    data_fix=[]
    nomor_urut=1
    for i in data:
        data_i=[]
        data_i.append(f'{nomor_urut}.')
        try:
            npm, nama=kelas.getNpmandNameMahasiswa(i[0])
            data_i.append(f'{nama}')
            data_i.append(f'{npm}')
            data_i.append(f'{kelas.getHandphoneMahasiswa(npm)}')
            data_i.append(f'HADIR')
            data_fix.append(data_i)
            nomor_urut+=1
        except:
            pass
    return data_fix

def insertLogPerwalian(kode_dosen, prodi_id, kelas_id, tahun_id, tahun_angkatan, jumlah_peserta, jumlah_hadir, jumlah_tidak_hadir, catatan):
    db=kelas.dbConnect()
    sql=f"INSERT INTO " \
        f"`wanda`.`perwalian_log` " \
        f"(`Id`, `KodeDosen`, `ProdiID`, `Kelas`, `TahunID`, `TahunAngkatan`, `JumlahMahasiswa`, `JumlahHadir`, `JumlahTidakHadir`, `Catatan`, `ApproveKaprodi`, `ApproveDeputi`) " \
        f"VALUES " \
        f"(DEFAULT, '{kode_dosen}', {prodi_id}, {kelas_id}, {tahun_id}, {tahun_angkatan}, {jumlah_peserta}, {jumlah_hadir}, {jumlah_tidak_hadir}, '{catatan}', 'false', 'false');"
    with db:
        cur=db.cursor()
        cur.execute(sql)

def updateLogPerwalian(id, jumlah_hadir, jumlah_tidak_hadir, catatan):
    db=kelas.dbConnect()
    sql=f"UPDATE `wanda`.`perwalian_log` SET `JumlahHadir` = {jumlah_hadir}, `JumlahTidakHadir` = {jumlah_tidak_hadir}, `Catatan` = '{catatan}' WHERE `Id` = {id};"
    with db:
        cur=db.cursor()
        cur.execute(sql)

def cekPerwalianLog(kode_dosen, prodi_id, tahun_id, group_name, jumlah_peserta, jumlah_hadir, jumlah_tidak_hadir, catatan):
    db=kelas.dbConnect()
    sql=f'select * from perwalian_log where KodeDosen="{kode_dosen}" and TahunID={tahun_id}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            id=row[0]
            updateLogPerwalian(
                id,
                jumlah_hadir,
                jumlah_tidak_hadir,
                catatan
            )
        else:
            insertLogPerwalian(
                kode_dosen,
                prodi_id,
                ord(group_name.split('-')[2].lower()) - 96,
                kelas.getTahunID(),
                f"{group_name.split('-')[3]}1",
                jumlah_peserta,
                jumlah_hadir,
                jumlah_tidak_hadir,
                catatan
            )

def randomString(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def makeLinkVerifiy(kodedosen):
    datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
    tanggal = datenow.split('-')[0]
    bulan = datenow.split('-')[1]
    tahun = datenow.split('-')[2]
    jam = datetime.now().time().strftime('%H')
    menit = datetime.now().time().strftime('%M')
    detik = datetime.now().time().strftime('%S')
    jenisdokumen='Absensi Perwalian'
    module_name='perwalian_selesai'
    data = f'{module_name};{kodedosen};{tanggal};{bulan};{tahun};{jam};{menit};{detik};{jenisdokumen};'
    makeit112 = f'{data}{randomString(112 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit112.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link

def makeQrcodeLinkVerifySign(link, status, kodedosen):
    tahunid=kelas.getTahunID()
    if status == 'dosen':
        img = qrcode.make(link)
        img.save(f'./surat_perwalian_qrcode/dosenqrcode-{tahunid}-{kodedosen}.png')
    elif status == 'kaprodi':
        img = qrcode.make(link)
        img.save(f'./surat_perwalian_qrcode/kaprodiqrcode-{tahunid}-{kodedosen}.png')
    else:
        img = qrcode.make(link)
        img.save(f'./surat_perwalian_qrcode/deputiqrcode-{tahunid}-{kodedosen}.png')

def checkDirQrcode():
    try:
        os.mkdir('surat_perwalian_qrcode/')
    except:
        pass

def checkDir():
    try:
        os.mkdir('surat_perwalian/')
    except:
        pass

def cekStatusApprovePerwalian(kode_dosen, tahun_id):
    db=kelas.dbConnect()
    sql=f"select ApproveKaprodi, ApproveDeputi from perwalian_log where KodeDosen='{kode_dosen}' and TahunID={tahun_id}"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        return row

def replymsg(driver, data):
    dosen_data=getDosenDataDictionaryDump(kelas.getKodeDosen(data[0]))
    home_base_prodi=dosen_data['Homebase']
    nama_dosen = kelas.getNamaDosen(dosen_data['Login'])
    nama_kaprodi = kelas.getNamaDosen(bkd.getDosenIDfromNIPY(bkd.getNipyKaProdi(home_base_prodi)))
    nama_deputi = kelas.getNamaDosen(bkd.getDosenIDfromNIPY(bkd.getNipyDeputi(9)))
    nama_prodi = kelas.getNamaProdiFromProdiID(home_base_prodi)['Nama']
    tipe_kelas=data[1].split('-')[2]
    catatan=data[3].split(' catatan ')[1]
    jmlPesertaPerwalian=len(perwalian_mulai.getPesertaPerwalian(kelas.getKodeDosen(data[0]), f"{data[1].split('-')[3]}1"))
    mainPages(
        kelas.getKodeDosen(data[0]),
        home_base_prodi,
        nama_dosen,
        nama_kaprodi,
        nama_deputi,
        nama_prodi,
        tipe_kelas,
        catatan,
        data[1],
        jmlPesertaPerwalian,
    )
    msgreply=f'okeeeee sudah yaaa, file PDF sudah {config.bot_name} kirim ke {dosen_data["Email"]}'
    return msgreply

def mainPages(kode_dosen, prodi_id, nama_dosen, nama_kaprodi, nama_deputi, nama_prodi, tipe_kelas, catatan, group_name, jmlPesertaPerwalian):
    checkDir()

    namaFile = f"surat_perwalian/SURAT-PERWALIAN-{kode_dosen}-{kelas.getTahunID()}-{prodi_id}-{tipe_kelas}-{kelas.getEmailDosen(kode_dosen)}.pdf"

    #check dir qrcode
    checkDirQrcode()

    # generate dosen barcode
    link = makeLinkVerifiy(kode_dosen)
    makeQrcodeLinkVerifySign(link, 'dosen', kode_dosen)

    # generate kaprodi barcode
    kaprodinipycode = bkd.getNipyKaProdi(prodi_id)
    kaprodiDosenID = bkd.getDosenIDfromNIPY(kaprodinipycode)
    link = makeLinkVerifiy(kaprodiDosenID)
    makeQrcodeLinkVerifySign(link, 'kaprodi', kode_dosen)

    # generate deputi barcode
    deputinipycode = bkd.getNipyDeputi(9)
    deputiDosenID = bkd.getDosenIDfromNIPY(deputinipycode)
    link = makeLinkVerifiy(deputiDosenID)
    makeQrcodeLinkVerifySign(link, 'deputi', kode_dosen)

    masukan=catatanToList(catatan)
    
    namaDeputi = nama_deputi
    namaKaprodi = nama_kaprodi
    namaDosen = nama_dosen

    prodi = nama_prodi

    listMahasiswa = hadirAbsensiData(group_name, 'daring')

    jumlahMhs = jmlPesertaPerwalian
    jumlahHadir = len(listMahasiswa)
    jumlahTdkHadir = jumlahMhs - jumlahHadir

    cekPerwalianLog(
        kode_dosen,
        prodi_id,
        kelas.getTahunID(),
        group_name,
        jumlahMhs,
        jumlahHadir,
        jumlahTdkHadir,
        catatan
    )

    statusappove=cekStatusApprovePerwalian(kode_dosen, kelas.getTahunID())

    qrDeputi = 'bkdqrcode/whiteimage.png'

    if statusappove[1] == 'true':
        qrDeputi = f'surat_perwalian_qrcode/deputiqrcode-{kelas.getTahunID()}-{kode_dosen}.png'

    qrKaprodi = 'bkdqrcode/whiteimage.png'
    if statusappove[0] == 'true':
        qrKaprodi = f'surat_perwalian_qrcode/kaprodiqrcode-{kelas.getTahunID()}-{kode_dosen}.png'

    qrDosen = f'surat_perwalian_qrcode/dosenqrcode-{kelas.getTahunID()}-{kode_dosen}.png'
    
    tahunAkademik = f'{int(kelas.getTahunID()[:-1])} - {int(kelas.getTahunID()[:-1])+1}'
    hariSekarang = daysEnToInd(datetime.now().strftime('%A'))
    tglSekarang = bkd.sahTanggal()

    listMasukan = masukan
    
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
    
    createBeritaAcaraPage(contain, styles, tahunAkademik, hariSekarang, tglSekarang, namaDosen, prodi, tipe_kelas, jumlahMhs, jumlahHadir, jumlahTdkHadir, listMasukan, namaDeputi, namaKaprodi, qrDeputi, qrKaprodi, qrDosen)
    createAbsensiPage(contain, styles, namaDosen, prodi, tipe_kelas, listMahasiswa, namaDeputi, namaKaprodi, qrDeputi, qrKaprodi, qrDosen)
    
    doc.build(contain)

    bkd.mail(
        kelas.getEmailDosen(kode_dosen),
        f'alooooo {config.bot_name} kirim file Absensi Perwalian NICHHHHHHH',
        f'Tolong dicek kembali yaaa datanya, dan jangan lupa buruann minta approvalnya ke KAPRODI dan DEPUTI yaa....',
        bkd.getFilePath(
            kelas.getEmailDosen(kode_dosen),
            'surat_perwalian',
            kelas.getTahunID()
        )
    )
    
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
        [Image(qrDosen, 4*cm, 4*cm), Image(qrKaprodi, 4*cm, 4*cm), Image(qrDeputi, 4*cm, 4*cm)],
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
    
    data = [[Paragraph('<font size="12"><b>No</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Nama Mahasiswa</b></font>', styles["Center"]), Paragraph('<font size="12"><b>NPM</b></font>', styles["Center"]), Paragraph('<font size="12"><b>No Handphone</b></font>', styles["Center"]), Paragraph('<font size="12"><b>Keterangan</b></font>', styles["Center"])]]
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
        [Image(qrDosen, 4*cm, 4*cm), Image(qrKaprodi, 4*cm, 4*cm), Image(qrDeputi, 4*cm, 4*cm)],
        [Paragraph(f'<font size="12"><u>{namaDosen}</u></font>', styles["Center"]), Paragraph(f'<font size="12"><u>{namaKaprodi}</u></font>', styles["Center"]), Paragraph(f'<font size="12"><u>{namaDeputi}</u></font>', styles["Center"])],
        ]

    table = Table(data, [6.8*cm, 6.8*cm, 6.8*cm], [.6*cm, 4.5*cm, 1*cm])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Times-Roman', 12),
        ('ALIGN',(0,1),(-1,-1),'CENTER'),
    ]))
    contain.append(table)

def verifyDigitalSign(resultpasscode):
    kodedosen = resultpasscode.split(';')[1]
    tglttd = resultpasscode.split(';')[2]
    blnttd = resultpasscode.split(';')[3]
    thnttd = resultpasscode.split(';')[4]
    jamttd = resultpasscode.split(';')[5]
    mntttd = resultpasscode.split(';')[6]
    dtkttd = resultpasscode.split(';')[7]
    jnsdkm = resultpasscode.split(';')[8]
    datadosen = kelas.getAllDataDosens(kodedosen)
    penerbitantandatangan = f'{jamttd}:{mntttd}:{dtkttd} {tglttd} {bkd.bulanSwitcher(blnttd)} {thnttd}'
    namadosen = kelas.getNamaDosen(kodedosen)
    datalahirdosen = datadosen[7].strftime('%d-%m-%Y')
    tahunlahirdosen = datalahirdosen.split('-')[2]
    bulanlahirdosen = bkd.bulanSwitcher(datalahirdosen.split('-')[1])
    tanggallahirdosen = datalahirdosen.split('-')[0]
    datalahirdosen = tanggallahirdosen + ' ' + bulanlahirdosen + ' ' + tahunlahirdosen
    msgreply = f'Ini yaaa data yang Akang/Teteh minta\n\nKode Dosen: {kodedosen}\nNama Dosen: {namadosen}\nNIDN: {datadosen[2]}\nTempat/Tgl Lahir: {datadosen[6]}/{datalahirdosen}\nHandphone: {datadosen[12]}\nE-mail: {datadosen[13]}\n\nJenis Dokumen: {jnsdkm}\nPenerbitan Tanda Tangan: {penerbitantandatangan}'
    return msgreply