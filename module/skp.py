from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import reportlab.lib
import reportlab.platypus

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

from Crypto.Cipher import AES
from module import kelas, bkd

from os import path
from lib import wa, reply, numbers
import qrcode

import os

import numpy as np
import pandas as pd

import config
import subprocess

import datetime

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) != None:
        ret = True
    else:
        ret = False
    return ret

def replymsg(driver, data):
    msgreply = ""
    if kelas.cekSiap():
        num = numbers.normalize(data[0])        
        try:
            if kelas.getNpmandNameMahasiswa(num):
                npm, nama = kelas.getNpmandNameMahasiswa(num)

                tahunID = kelas.getTahunID()
                namaMhs, prodiMhs, singkatan, prodiID, email = getMahasiswaByNpm(npm)
                id_surat = checkApproveMhs(npm)

                if id_surat:
                    data = f"{npm};{singkatan};{email};{id_surat}"
                    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0],data], cwd=config.cwd)
                    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
                    wmsg = wmsg.replace('#EMAIL#', email)
                    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
                    wa.typeAndSendMessage(driver, wmsg)
                else:
                    if checkAjukanMhs(npm):
                        ajukanSKPI(npm)
                        msgreply = "SKPI kamu telah diajukan, hubungi staff *Wadir 1* (Bu Tetty) untuk meminta approve SKPI yang telah diajukan. Harap menunggu dengan sabar, karena kamu pasti mendapatkan yang lebih baik dari dia."
                    else:
                        msgreply = f"Kamu bercanda deh, mana mungkin kamu bisa memintanya"
            else:
                msgreply = f"Sakit, ketika kamu meminta sesuatu tetapi tidak saya berikan karena saya tidak mengenalmu."
            
        except Exception as e:
            msgreply = f'Lucu ya, karena pesanmu itu membuatku merasa bersalah.. {str(e)}'
            
    else:
        # pass
        wa.typeAndSendMessage(driver, 'Mohon maaf server Akademik SIAP sedang dalam kondisi DOWN, mohon untuk menginformasikan ke ADMIN dan tunggu')
    return msgreply

def run(data):
    data = data.split(';')
    npm = data[0]
    singkatan = data[1].lower()
    email = data[2]
    idSurat = data[3]
    
    year = datetime.datetime.now().year
    
    df = pd.read_excel(f"./skp/list-skpi/{singkatan}-{year}.xlsx")
    listColumn = ["Nama Lengkap","Tempat, Tanggal Lahir", "NPM", "Tahun Masuk", "Tahun Lulus", "No. Ijazah", "Gelar"]
    dfIdentitas = df.loc[:, listColumn]
    identitas = dfIdentitas.loc[dfIdentitas["NPM"] == int(npm)].replace(np.NaN, "-").values.tolist()[0]
    
    listColumn = ["Penghargaan", "Pengalaman Organisasi", "Judul Skripsi", "Bahasa Internasional", "Magang Industri", "Pendidikan Karakter", "Sertifikat", "NPM"]
    dfCapaian = df.loc[:, listColumn]
    capaian = dfCapaian.loc[dfCapaian["NPM"] == int(npm)].replace(np.NaN, "-").values.tolist()[0]
    
    makePage(npm, singkatan, email, identitas, capaian, idSurat)

colorTitle = colors.Color(red=(0/255),green=(112/255),blue=(192/255))
colorHeader = colors.Color(red=(247/255),green=(150/255),blue=(70/255))
colorSubHeader = colors.Color(red=(155/255),green=(187/255),blue=(89/255))

pdfmetrics.registerFont(TTFont('Arial', './skp/ARIAL.TTF'))

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=8, leading=10))

styles.add(ParagraphStyle(name='Header', alignment=TA_CENTER, textColor=colorHeader))

styleWrap = styles["Normal"]
styleWrap.alignment = TA_JUSTIFY
# styleWrap.fontName = 'Arial'
styleWrap.fontSize = 8
styleWrap.leading = 9.5

def checkApproveMhs(npm):
    db=kelas.dbConnect()
    sql=f"select id from skp_data where (ajukan is not null and ajukan <> '-') and (wadir1 is not null and wadir1 <> '-') and (direktur is not null and direktur <> '-') and npm = '{npm}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return row[0]
    return False

def checkAjukanMhs(npm):
    db=kelas.dbConnect()
    sql=f"select npm, nama from skp_data where npm = '{npm}'"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row:
            return True
    return False

def ajukanSKPI(npm):
    db=kelas.dbConnect()
    sql=f"update skp_data set ajukan = 'TRUE' where npm = '{npm}'"
    # print(sql)
    with db:
        cur=db.cursor()
        cur.execute(sql)

def convertMonth(month):
    months = {
        '01': 'Januari',
        '02': 'Februari',
        '03': 'Maret',
        '04': 'April',
        '05': 'Mei',
        '06': 'Juni',
        '07': 'Juli',
        '08': 'Agustus',
        '09': 'September',
        '10': 'Oktober',
        '11': 'November',
        '12': 'Desember',
    }
    return months.get(str(month), "-")

def convertDate(date):
    data = date.strftime('%d-%m-%Y').split("-")
    return f"{data[0]} {convertMonth(data[1])} {data[2]}"

tglTTD = convertDate(datetime.datetime.date(datetime.datetime.now()))

def getInstitutionInformation(prodi):
    data = {
        'd4ti': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D IV Informatics Engineering</i><br />D IV Teknik Informatika',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma IV</i><br />Diploma IV',
            '<i>Level 6</i><br />Level 6',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>4 Years</i><br />4 Tahun',
            '<i>Post Graduate</i><br />Pasca Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
        'd4lb': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D IV Business Logistics</i><br />D IV Logistik Bisnis',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma IV</i><br />Diploma IV',
            '<i>Level 6</i><br />Level 6',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>4 Years</i><br />4 Tahun',
            '<i>Post Graduate</i><br />Pasca Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
        'd4mb': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D IV Corporate Management</i><br />D IV Manajemen Perusahaan',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma IV</i><br />Diploma IV',
            '<i>Level 6</i><br />Level 6',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>4 Years</i><br />4 Tahun',
            '<i>Post Graduate</i><br />Pasca Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
        'd4ak': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D IV Financial Accounting</i><br />D IV Akuntansi Keuangan',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma IV</i><br />Diploma IV',
            '<i>Level 6</i><br />Level 6',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>4 Years</i><br />4 Tahun',
            '<i>Post Graduate</i><br />Pasca Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
        'd3ti': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D III Informatics Engineering</i><br />D III Teknik Informatika',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma III</i><br />Diploma III',
            '<i>Level 5</i><br />Level 5',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>3 Years</i><br />3 Tahun',
            '<i>Bachelor</i><br />Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
        'd3mi': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D III Informatics Management</i><br />D III Manajemen Informatika',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma III</i><br />Diploma III',
            '<i>Level 5</i><br />Level 5',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>3 Years</i><br />3 Tahun',
            '<i>Bachelor</i><br />Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
        'd3mb': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D III Marketing Management</i><br />D III Manajemen Pemasaran',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma III</i><br />Diploma III',
            '<i>Level 5</i><br />Level 5',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>3 Years</i><br />3 Tahun',
            '<i>Bachelor</i><br />Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
        'd3lb': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D III Logistics Administration</i><br />D III Administrasi Logistik',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma III</i><br />Diploma III',
            '<i>Level 5</i><br />Level 5',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>3 Years</i><br />3 Tahun',
            '<i>Bachelor</i><br />Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
        'd3ak': [
            '<i>Act of National Educaton Minister of Indonesia Republic No. 56/D/O/2001</i><br />SK Menteri Pendidikan Nasional Republik Indonesia nomor : 56/D/O/2001',
            'Pos Indonesia <i>Polytechnic</i><br />Politeknik Pos Indonesia',
            '<i>D III Accounting</i><br />D III Akuntansi',
            '<i>Polytechnic</i><br />Politeknik',
            '<i>Diploma III</i><br />Diploma III',
            '<i>Level 5</i><br />Level 5',
            '<i>Graduated from high school and Passed the new student selection</i><br />Lulus SMA dan Lulus Seleksi Mahasiswa Baru',
            '<i>Bahasa Indonesia</i><br />Bahasa Indonesia',
            '<i>Grading Scheme</i><br />A = 4 ; B = 3 ; C = 2 ; D = 1 ; E = 0',
            '<i>3 Years</i><br />3 Tahun',
            '<i>Bachelor</i><br />Sarjana',
            '<i>None</i><br />Belum ada keanggotaan profesi'
        ],
    }
    return data.get(prodi, [])

def getLearningOutcome(prodi):
    data = {
        'd4ti': [
            ['3.A.1', Paragraph('<i>The common understanding of the process and the main functions in the field of information technology, information technology implementation, and the basic design  of information technology implementation.</i><br />Pemahaman umum terhadap proses dan fungsi-fungsi utama di bidang teknologi informasi, implementasi Teknologi  informasi, dan dasar perancangan implementasi teknologi informasi', styleWrap)],
            ['3.A.2', Paragraph('<i>Understand the development of technologies relevant to the implementation, development of applications applied.</i><br />Memahami  perkembangan teknologi yang sesuai dengan implementasinya, perkembangan aplikasi-aplikasi terapan.', styleWrap)],
            ['3.A.3', Paragraph('<i>Able to build systems / applications to support operations in the field of post and telecommunications and logistics.</i><br />Mampu membangun sistem /aplikasi untuk mendukung operasional di bidang postal dan logistik.', styleWrap)],
            ['3.A.4', Paragraph('<i>Understand the development of technologies relevant to the implementation, development of applied applications.</i><br />Memahami  perkembangan teknologi yang sesuai dengan implementasinya, perkembangan aplikasi-aplikasi terapan.', styleWrap)],
            ['3.A.5', Paragraph('<i>Have knowledge of operational support software application development Understand, understand the programming language, supporting software implementation in accordance with their needs.</i><br />Memiliki pengetahuan tentang software pendukung operasioanl  Memahami pengembangan aplikasi, memahami bahasa pemrograman, implementasi software pendukung sesuai dengan kebutuhannya.', styleWrap)],
            ['3.A.6', Paragraph('<i>Understand how to install supporting software, network troubleshooting understand, build and manage computer networks.</i><br />Memahami cara instalasi software pendukung, memahami trouble shooting jaringan, membangun dan mengelola jaringan komputer.', styleWrap)],
            ['3.A.7', Paragraph('<i>Understand how to install supporting software, network troubleshooting understand, build and manage computer networks.</i><br />Memahami cara instalasi software pendukung, memahami trouble shooting jaringan, membangun dan mengelola jaringan komputer.', styleWrap)],
            ['3.A.8', Paragraph('<i>Understand the hardware and software required by the type of work.</i><br />Memahami perangkat keras dan perangkat lunak yang di perlukan sesuai dengan jenis pekerjaan.', styleWrap)],
            ['3.A.9', Paragraph('<i>Understand the concept of LAN, MAN and WAN.</i><br />Memahami konsep LAN, MAN dan WAN.', styleWrap)],
            ['3.A.10', Paragraph('<i>Understand the DNS configuration, and WEB SERVER MAIL SERVER.</i><br />Memahami konfigurasi  DNS, MAIL SERVER dan WEB SERVER.', styleWrap)],
        ],
        'd4lb': [
            ['3.A.1', Paragraph('<i>Having the ability and understanding the administrative tasks of logistics, like having the ability to understand the types of forms and documents that are used as well as the corresponding documentation system established procedure.</i><br />Memiliki kemampuan dan memahami tugas-tugas administrasi logistik, seperti memiliki kemampuan memahami jenis formulir dan dokumen yang dipergunakan serta sistem dokumentasi sesuai prosedur yang ditetapkan.', styleWrap)],
            ['3.A.2', Paragraph('<i>Having the ability to analyze and handle cargo surveyors, and containers.</i><br />Memiliki kemampuan menganalisa dan menangani cargo surveyor dan kontainer.', styleWrap)],
            ['3.A.3', Paragraph('<i>Having the ability in terms of service to customers . Having knowledge and able to understand the use of work tools in accordance with the procedures and kselamatan health (K3).</i><br />Memiliki kemampuan dalam  hal pelayanan kepada pelanggan. Memiliki pengetahuan dan mampu memahami penggunaan alat kerja sesuai dengan prosedur kesehatan dan keselamatan kerja (K3).', styleWrap)],
            ['3.A.4', Paragraph('<i>Having knowledge about the dangerous goods , and government regulations relating to the handling of dangerous goods.</i><br />Memiliki pengetahuan mengenai dangerous goods, dan peraturan pemerintah berkaitan dengan penanganan barang barang berbahaya.', styleWrap)],
            ['3.A.5', Paragraph('<i>Having knowledge about the type, model and the transport system. Having the ability to plan and analyze multimodal cost structure that will be used. Having the ability to understand the management of land transportation, sea, air, including the characteristics of transport equipment, conveyance route selection, and arrange the schedule departure / arrival conveyance. Having the ability to compose on the types of tariff applicable to each mode of transport, as well as analyzing the cost structure determination procedures.</i><br />Memiliki pengetahuan tentang jenis, model dan system pengangkutan. Memiliki kemampuan merencanakan dan menganalisa struktur biaya multimoda yg akan digunakan. Memiliki kemampuan memahami tata laksana pengangkutan darat, laut, udara, termasuk karakteristik alat angkutan, pemilihan rute alat angkut, serta menyusun jadual keberangkatan/kedatangan alat angkut. Memiliki kemampuan menyusun mengenai jenis-jenis pentarifan yang berlaku   bagi masing-masing moda transpor, serta menganalisa tatacara penetapan struktur biaya.', styleWrap)],
            ['3.A.6', Paragraph('<i>Having the ability to understand insurance issues in terms of risk calculations, comprehensive warranty and claims handling.</i><br />Memiliki kemampuan memahami masalah asuransi dalam hal  perhitungan resiko, luas jaminan, dan penanganan klaim.', styleWrap)],
            ['3.A.7', Paragraph('<i>Have knowledge of inventory so that they can perform calculations Economical Order Quantity (EOQ), Just In Time (JIT) and quantitative techniques in inventory handling.</i><br />Memiliki   pengetahuan   tentang   persediaan   sehingga   mampu   melakukan perhitungan Economical Order Quantity (EOQ), Just In Time (JIT) serta teknik kuantitatif dalam penanganan persediaan.', styleWrap)],
        ],
        'd4mb': [
            ['3.A.1', Paragraph('<i>Able to work productively, adaptably and to act out his function and contribute in solving business problems, particularly in the scope of the logistics industry handled.</i><br />Mampu bekerja secara produktif, beradaptasi dan memerankan fungsinya dan memberikan konstribusi dalam penyelesaian permasalahan bisnis khususnya yang terjadi di lingkup industri logistik yang ditanganinya.', styleWrap)],
            ['3.A.2', Paragraph('<i>Able to work productively, adaptably and to act out their functions in accordance with the technical skills possessed in a creative and innovative multidisciplinary team work.</i><br />Mampu bekerja secara produktif, mudah beradaptasi dan memerankan fungsinya sesuai dengan disiplin ketrampilan teknis yang dimiliki dalam kerja tim multidisiplin ilmu secara kreatif dan inovatif.', styleWrap)],
            ['3.A.3', Paragraph('<i>Able to perform business planning.</i><br />Mampu melakukan perancangan bisnis.', styleWrap)],
            ['3.A.4', Paragraph('<i>Able to utilize, and make strategic decisions and to recommend strategic business to consumers.</i><br />Mampu memanfaatkan, dan membuat keputusan serta rekomendasi produk bisnis yang tepat kepada konsumen.', styleWrap)],
            ['3.A.5', Paragraph('<i>Able to utilize, and make strategic decisions and give strategic recommendations in the field of business.</i><br />Mampu memanfaatkan, dan membuat keputusan serta rekomendasi yang strategis dibidang bisnis.', styleWrap)],
            ['3.A.6', Paragraph('<i>Able to set or to choose the right method according to the various methods available for promotional activities.</i><br />Mampu menetapkan atau memilih metode yang tepat dan sesuai dari beragam metode yang ada untuk kegiatan promosi.', styleWrap)],
            ['3.A.7', Paragraph('<i>Able to take decisions within the scope of procedural completion of the logistics industry in accordance with the level of its authority.</i><br />Mampu mengambil keputusan penyelesaian prosedural dalam lingkup industri logistik sesuai dengan tingkat kewenangan yang dimilikinya.', styleWrap)],
            ['3.A.8', Paragraph('<i>Able to take decisions relating to the operational performance of the business processes in the logistics industry.</i><br />Mampu mengambil keputusan yang bersifat operasional terkait dengan kinerja proses bisnis di industri logistik.', styleWrap)],
            ['3.A.9', Paragraph('<i>UAble to take decisions operationally linked to the performance of the production process in the logistics industry.</i><br />Mampu mengambil keputusan yang bersifat operasional terkait dengan kinerja proses produksi pada industri logistik.', styleWrap)],
            ['3.A.10', Paragraph('<i>Able to maintain discipline labor, and be able to assess the performance of a group / subordinates in accordance with the applicable standards.</i><br />Mampu menjaga disiplin kerja, serta mampu menilai prestasi kerja kelompok/bawahannya sesuai dengan standar yang berlaku.', styleWrap)],
        ],
        'd4ak': [
            ['3.A.1', Paragraph('<i>Able to apply his expertise and to make use knowledge in solving problems in the areas of Financial Accounting, and is able to adapt to various situations faced.</i><br />Mampu menerapkan keahliannya dan memanfaatkan pengetahuan dalam memecahkan masalah di bidang Akuntansi Keuangan, dan mampu beradaptasi dengan berbagai situasi yang dihadapi.', styleWrap)],
            ['3.A.2', Paragraph('<i>Know the theoretical concepts in depth in the field of Financial Accounting.</i><br />Mengetahui konsep teoritis secara mendalam di bidang Akuntansi Keuangan.', styleWrap)],
            ['3.A.3', Paragraph('<i>Able to resolve business issues procedurally, independently, or in groups by providing various alternative solutions.</i><br />Mampu menyelesaikan permasalahan bisnis secara prosedural, mandiri, maupun kelompok dengan memberikan berbagai alternatif solusi.', styleWrap)],
            ['3.A.4', Paragraph('<i>Able to make decisions based on data analysis and information.</i><br />Mampu mengambil keputusan berdasarkan hasil analisis data dan informasi.', styleWrap)],
            ['3.A.5', Paragraph('<i>Have a professional attitude, integrity and responsibility in completing the work.</i><br />Memiliki sikap profesional, integritas dan tanggung jawab dalam menyelesaikan pekerjaan.', styleWrap)],
            ['3.A.6', Paragraph('<i>Have the ability to conductbusiness communications. Capable of analyzing the feasibility of a business/ enterprise.</i><br />Memiliki kemampuan dalam melakukan komunikasi bisnis. Mampu melakukan analisis kelayakan bisnis/usaha.', styleWrap)],
        ],
        'd3ti': [
            ['3.A.1', Paragraph('<i>Able to develop the system using predetermined software design methods and refer to the IEEE 29148: 2011 SRS standard, and can provide results in the design of the system according to the needs that have been defined.</i><br />Mampu mengembangkan sistem dengan menggunakan metode  desain perangkat lunak yang telah ditentukan dan mengacu standar SRS IEEE 29148:2011, dan dapat memberikan hasil berupa desain sistem sesuai kebutuhan yang sudah terdefinisi.', styleWrap)],
            ['3.A.2', Paragraph('<i>Able to develop enterprise-based enterprise software (ERP) by implementing predetermined software development methodologies to produce software that suits the needs of users.</i><br />Mampu mengembangkan perangkat lunak berbasis bisnis enterprise (ERP) dengan menerapkan metodologi pengembangan perangkat lunak yang telah ditentukan agar menghasilkan perangkat lunak yang sesuai dengan kebutuhan pengguna.', styleWrap)],
            ['3.A.3', Paragraph('<i>Able to perform software testing using black box and or white box method as needed, with documentation that meets SRS standard IEEE 29148: 2011.</i><br />Mampu melakukan pengujian perangkat lunak menggunakan metode black box dan atau white box sesuai kebutuhan, dengan dokumentasi yang mangacu standar SRS IEEE 29148:2011.', styleWrap)],
            ['3.A.4', Paragraph('<i>Able to develop database system according to user requirement by utilizing DBMS technology, and produce appropriate database system.</i><br />Mampu mengembangkan sistem basis data sesuai kebutuhan pengguna dengan memanfaatkan teknologi DBMS, dan menghasilkan sistem basis data yang tepat guna.', styleWrap)],
            ['3.A.5', Paragraph('<i>Able to design and develop web-based system by utilizing the web development method that has been determined, and produce the system as needed.</i><br />Mampu merancang dan mengembangkan sistem berbasis web dengan memanfaatkan metode pengembangan web yang telah ditentukan, dan menghasilkan sistem sesuai kebutuhan.', styleWrap)],
            ['3.A.6', Paragraph('<i>Able to design and manage computer network system based on predetermined operating system to produce appropriate network system.</i><br />Mampu merancang dan mengelola sistem jaringan komputer berdasarkan sistem operasi yang telah ditentukan agar menghasilkan sistem jaringan tepat guna.', styleWrap)],
        ],
        'd3mi': [
            ['3.A.1', Paragraph('<i>Should understand the business functions and organization of the company and general.</i><br />Harus memahami fungsi bisnis dan organisasi Perusahaan secara umum.', styleWrap)],
            ['3.A.2', Paragraph('<i>Must have the ability of critical, analitycal ability and innovation.</i><br />Harus memiliki kemampuan kritis, kemampuan analitis dan inovasi.', styleWrap)],
            ['3.A.3', Paragraph('<i>Must have profession ethics soft skill and ability in collaboration within the team.</i><br />Harus memiliki etika profesional soft skill dan kemampuan bekerjasama dalam tim.', styleWrap)],
            ['3.A.4', Paragraph('<i>Able to design and implement information tecnology solutions that are able to improve the performance of organizations bisinesses.</i><br />Mampu merancang dan mengimplementasikan solusi teknologi informasi yang dapat meningkatkan kinerja organisasi dan bisnis.', styleWrap)],
            ['3.A.5', Paragraph('<i>Must have emotional intelligence, spiritual and passion of fighting countries.</i><br />Memiliki kecerdasan emosional, spiritual dan semangat bela negara.', styleWrap)],
            ['3.A.6', Paragraph('<i>Mastering knowledge about codes and standards in the preparation of software development documentation (IEEE Std 830-1998 and IEEE Std 1016TM-2009)</i><br />Menguasai pengetahuan tentang codes dan standard dalam penyusunan dokumentasi pengembangan perangkat lunak (IEEE Std 830-1998 dan IEEE Std 1016TM-2009)', styleWrap)],
        ],
        'd3mb': [
            ['3.A.1', Paragraph('<i>Able to apply logical thinking, critical, innovative, quality, and measurable in doing specific work in the field of software development and in accordance with the competency standards of the field concerned.</i><br />Mampu menerapkan pemikiran logis, kritis, inovatif, bermutu, dan terukur dalam melakukan pekerjaan yang spesifik di bidang pengembangan perangkat lunak serta sesuai dengan standar kompetensi kerja bidang yang bersangkutan.', styleWrap)],
            ['3.A.2', Paragraph('<i>Identify the marketing elements of a company.</i><br />Mengidentifikasi elemen pemasaran perusahaan.', styleWrap)],
            ['3.A.3', Paragraph('<i>Implement effective communication.</i><br />Melaksanakan komunikasi efektif.', styleWrap)],
            ['3.A.4', Paragraph('<i>Implementing business writing.</i><br />Melaksanakan penulisan bisnis.', styleWrap)],
            ['3.A.5', Paragraph('<i>Master the theory, STP method (Segmenting, Targeting, Positioning).</i><br />Menguasai teori, metode STP (Segmenting, Targeting, Positioning).', styleWrap)],
            ['3.A.6', Paragraph('<i>Mastering Knowledge of concept, theory, and applied Personal Selling.</i><br />Menguasai Pengetahuan konsep, teori, dan terapan Personal Selling.', styleWrap)],
            ['3.A.7', Paragraph('<i>Mastering the principles of advertising management, sales promotion and public relations marketing.</i><br />Menguasai prinsip-prinsip manajemen periklanan, promosi penjualan dan marketing public relation.', styleWrap)],
            ['3.A.8', Paragraph('<i>Mastering the concept of applied e-marketing.</i><br />Menguasai konsep terapan e-marketing.', styleWrap)],
        ],
        'd3lb': [
            ['3.A.1', Paragraph('<i>Able to formulate the planning, organizing, directing, controlling and evaluating the organization of logistics.</i><br />Mampu merumuskan perencanaan, pengorganisasian, pengarahan, dan pengendalian serta evaluasi tingkat operasional pada organisasi logistik.', styleWrap)],
            ['3.A.2', Paragraph('<i>Able to perform the planning of product demand and/or logistics services with forcsting mode in logistics industry.</i><br />Mampu melakukan perencanaan permintaan produk dan/atau jasa logistik dengan model forecashting pada industri logistik.', styleWrap)],
            ['3.A.3', Paragraph('<i>Able to plan and to manage inventory in the logistics warehouse inventory activity.</i><br />Mampu melakukan perencanaan dan pengelolaan persediaan pada aktivitas persediaan gudang logistik.', styleWrap)],
            ['3.A.4', Paragraph('<i>Able to do distribution planning by applying minimum of one method and able to show the result in the form of matrix distribution planning.</i><br />Mampu melakukan Perencanaan Distribusi dengan penerapan minimum satu metode dan dapat menunjukkan hasil berupa matriks perencanaan distribusi.', styleWrap)],
            ['3.A.5', Paragraph('<i>Able to carry out the activities of warehousing operations.</i><br />Mampu melaksanakan kegiatan operasional  pergudangan dengan kemampuan mengaplikasikan sistem penerimaan, penyimpanan dan pengiriman barang.', styleWrap)],
            ['3.A.6', Paragraph('<i>Able to carry out operations of transportation with the ability to apply more than one method of transportation.</i><br />Mampu melaksanakan kegiatan operasional  transportasi dengan kemampuan mengaplikasikan lebih dari satu metode transportasi.', styleWrap)],
        ],
        'd3ak': [
            ['3.A.1', Paragraph('<i>Able to apply his expertise and to make use of knowledge in solving problems in the areas of Financial Accounting, and able to adapt to various situations faced.</i><br />Mampu menerapkan keahliannya dan memanfaatkan pengetahuan dalam memecahkan masalah di bidang Akuntansi Keuangan dan mampu beradaptasi dengan berbagai situasi yang dihadapi.', styleWrap)],
            ['3.A.2', Paragraph('<i>Know the theoretical concepts in depth in the field of Financial Accounting.</i><br />Mengetahui konsep teoritis secara mendalam di bidang Akuntansi Keuangan.', styleWrap)],
            ['3.A.3', Paragraph('<i>Able to resolve business issues procedurally, independently, or in groups by providing various alternative solutions.</i><br />Mampu menyelesaikan masalah bisnis secara prosedural, mandiri, atau dalam kelompok dengan menyediakan berbagai solusi alternatif.', styleWrap)],
            ['3.A.4', Paragraph('<i>Able to make decisions based on data analysis and information.</i><br />Mampu membuat keputusan berdasarkan analisis data dan informasi.', styleWrap)],
            ['3.A.5', Paragraph('<i>Have a professional attitude , integrity and responsibility in completing the work.</i><br />Memiliki sikap profesional, integritas dan tanggung jawab dalam menyelesaikan pekerjaan.', styleWrap)],
            ['3.A.6', Paragraph('<i>Have the ability to conduct business communication. Capable of analyzing the feasibility of a business / enterprise.</i><br />Memiliki kemampuan untuk melakukan komunikasi bisnis. Mampu menganalisis kelayakan bisnis / perusahaan.', styleWrap)],
        ],
    }
    
    return data.get(prodi, [])

def getDirekturData():
    return ["Dr. Ir. Agus Purnomo, MT.","118.64.237"]

def getWadirIData():
    return ["Dodi Permadi, ST., MT.","107.77.117"]

def pageSetup(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.drawImage('./skp/background.png', 0, -height/2.82, width*1.415, height*1.415, preserveAspectRatio=True, anchor='c')

    canvas.restoreState()


def noSurat(npm, noIjazah, idSurat):
    return Paragraph(f'<font size="10" color="{colorTitle}">Nomor : {idSurat.zfill(3)}-{npm}/{noIjazah}</font>', styles["Center"])

def keteranganSurat():
    ptext = """
    <font size="8"><i>The Diploma Supplement accompanies a higher education certificate providing a standardized description of the nature, level, context, content and status of the studies completed by its holder</i></font>
    <br />
    <font size="9">Surat Keterangan Pendamping Ijazah sebagai pelengkap Ijazah yang menerangkan capaian pembelajaran dan prestasi dari pemegang Ijazah selama masa studi</font>
    """
    return Paragraph(ptext, styles["Center"])

def personalInformation(nama, ttl, npm, thnMasuk, thnLulus, noIjazah, gelar):
    data = [
        [Paragraph('<b>I.</b>', styles["Center"]), Paragraph('<b><i>INFORMATION IDENTIFYING PERSONAL INFORMATION OF DIPLOMA SUPPLEMENT HOLDER</i></b><br /><b>INFORMASI TETANG IDENTITAS DIRI PEMEGANG SKPI</b>', styleWrap)],
        ['1.1', Paragraph('<i>Full Name</i><br />Nama Lengkap', styleWrap), Paragraph(f'<b><i>{nama}</i></b>', styleWrap)],
        ['1.2', Paragraph('<i>Place and Date of Birth</i><br />Tempat dan Tanggal Lahir', styleWrap), f'{ttl}'],
        ['1.3', Paragraph('<i>Student Identification Number</i><br />Nomor Pokok Mahasiswa', styleWrap), f'{npm}'],
        ['1.4', Paragraph('<i>Admission Year</i><br />Tahun Masuk', styleWrap), f'{thnMasuk}'],
        ['1.5', Paragraph('<i>Graduation Year</i><br />Tahun Lulus', styleWrap), f'{thnLulus}'],
        ['1.6', Paragraph('<i>Number of Certification</i><br />Nomor Ijazah', styleWrap), f'{noIjazah}'],
        ['1.7', Paragraph('<i>Title</i><br />Gelar', styleWrap), f'{gelar}'],
    ]
    
    table = Table(data, [1.2*cm, 4.3*cm, 6.7*cm], None)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colorHeader),
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        ('INNERGRID', (0,0), (-1,-1), 2, colors.grey),
        ('BOX', (0,0), (-1,-1), 2, colors.grey),         
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'), 
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN',(0,1),(0,-1),'TOP'),
        ('SPAN', (1, 0), (2, 0))
    ]))
    return table

def institutionInformation1(param21, param22, param23, param24):
    data = [
        [Paragraph('<b>II.</b>', styles["Center"]), Paragraph('<b><i>INFORMATION IDENTIFYING HIGHER EDUCATION INSTITUTION</i><br />INFORMASI TENTANG IDENTITAS PENYELENGGARA PROGRAM</b>', styleWrap)],
        ['2.1', Paragraph('<i>Certificate of Establishment</i><br />Surat Keterangan Pendirian', styleWrap), Paragraph(param21, styleWrap)],
        ['2.2', Paragraph('<i>Name of Higher Education</i><br />Nama Perguruan Tinggi', styleWrap), Paragraph(param22, styleWrap)],
        ['2.3', Paragraph('<i>Study Program</i><br />Nama Program Studi', styleWrap), Paragraph(param23, styleWrap)],
        ['2.4', Paragraph('<i>Classification of Study</i><br />Jenis Pendidikan', styleWrap), Paragraph(param24, styleWrap)]
    ]
    table = Table(data, [1.2*cm, 4.7*cm, 6.3*cm], None)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colorHeader),
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        ('INNERGRID', (0,0), (-1,-1), 2, colors.grey),
        ('BOX', (0,0), (-1,-1), 2, colors.grey),           
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'), 
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN',(0,1),(1,-1),'TOP'),
        ('SPAN', (1, 0), (2, 0))
    ]))
    return table

def institutionInformation2(param25, param26, param27, param28, param29, param210, param211, param212):
    data = [
        ['2.5', Paragraph('<i>Education Level</i><br />Jenjang Pendidikan', styleWrap), Paragraph(param25, styleWrap)],
        ['2.6', Paragraph('<i>Appropriate Level of Qualification KKNI</i><br />Jenjang kualifikasi Sesuai KKNI', styleWrap), Paragraph(param26, styleWrap)],
        ['2.7', Paragraph('<i>Qualification Requirements</i><br />Persyaratan Penerimaan', styleWrap), Paragraph(param27, styleWrap)],
        ['2.8', Paragraph('<i>Language Instruction</i><br />Bahasa Pengantar Kuliah', styleWrap), Paragraph(param28, styleWrap)],
        ['2.9', Paragraph('<i>Grading System</i><br />Sistem Penilaian', styleWrap), Paragraph(param29, styleWrap)],
        ['2.10', Paragraph('<i>Period of Regular Study</i><br />Lama Studi Reguler', styleWrap), Paragraph(param210, styleWrap)],
        ['2.11', Paragraph('<i>Access to Further Study</i><br />Jenis dan Jenjang Pendidikan Lanjutan', styleWrap), Paragraph(param211, styleWrap)],
        ['2.12', Paragraph('<i>Professional Status</i><br />Status Profesi', styleWrap), Paragraph(param212, styleWrap)]
    ]
    table = Table(data, [1.2*cm, 4.7*cm, 6.3*cm], None)
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        ('INNERGRID', (0,0), (-1,-1), 2, colors.grey),
        ('BOX', (0,0), (-1,-1), 2, colors.grey),         
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'), 
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN',(0,1),(1,-1),'TOP'),
    ]))
    return table

def learningOutcome(prodi):
    data = [
        [Paragraph('<b>III.</b>', styles["Center"]), Paragraph('<b><i>INFORMATION OF QUALIFICATION AND LEARNING OUTCOME</i><br />INFORMASI TENTANG KUALIFIKASI DAN HASIL YANG DICAPAI</b>', styleWrap)],
        [Paragraph('<b>A.</b>', styles["Center"]), Paragraph('<b><i>Learning Outcome</i><br />Capaian Pembelajaran</b>', styleWrap)],
    ]
    
    data.extend(getLearningOutcome(prodi))
    
    table = Table(data, [1.2*cm, 11*cm], None)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colorHeader),
        ('BACKGROUND', (0, 1), (-1, 1), colorSubHeader),
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        ('INNERGRID', (0,0), (-1,-1), 2, colors.grey),
        ('BOX', (0,0), (-1,-1), 2, colors.grey),           
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'), 
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN',(0,1),(1,-1),'TOP'),
    ]))
    return table

def additionalInformation(param3b1, param3b2, param3b3, param3b4, param3b5, param3b6, param3b7):
    # print(param3b1, param3b2, param3b3, param3b4, param3b5, param3b6, param3b7)
    data = [
        [Paragraph('<b>B.</b>', styles["Center"]), Paragraph('<b><i>Learning Outcome</i><br />Capaian Pembelajaran</b>', styleWrap)],        
        ['3.B.1', Paragraph('<i>Honors and Awards</i><br />Penghargaan dan Pemenang Kejuaraan', styleWrap), Paragraph(str(param3b1), styleWrap)],
        ['3.B.2', Paragraph('<i>Organizational Experiences</i><br />Pengalaman Berorganisasi', styleWrap), Paragraph(param3b2, styleWrap)],
        ['3.B.3', Paragraph('<i>Spessification of The Final Project</i><br />Spesifikasi Tugas Akhir', styleWrap), Paragraph(param3b3, styleWrap)],
        ['3.B.4', Paragraph('<i>International Language</i><br />Bahasa Internasional', styleWrap), Paragraph(param3b4, styleWrap)],
        ['3.B.5', Paragraph('<i>Internship</i><br />Magang Industri', styleWrap), Paragraph(param3b5, styleWrap)],
        ['3.B.6', Paragraph('<i>Soft Skill Training</i><br />Pendidikan Karakter', styleWrap), Paragraph(param3b6, styleWrap)],
        ['3.B.7', Paragraph('<i>Certification</i><br />Sertifikat', styleWrap), Paragraph(param3b7, styleWrap)],
    ]
    table = Table(data, [1.2*cm, 4.7*cm, 6.3*cm], None)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colorSubHeader),
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        ('INNERGRID', (0,0), (-1,-1), 2, colors.grey),
        ('BOX', (0,0), (-1,-1), 2, colors.grey),           
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'), 
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN',(0,1),(1,-1),'TOP'),
        ('SPAN', (1, 0), (2, 0)),
    ]))
    return table

def ttdSurat(data):
    
    table = Table(data, [5.6*cm, 6.6*cm], [None, 3.2*cm, None])
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        # ('INNERGRID', (0,0), (-1,-1), 2, colors.grey),
        # ('BOX', (0,0), (-1,-1), 2, colors.grey),         
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'), 
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
    ]))
    return table

def columnTwoFirst(dataMhs, prodi, pathTTD):
    nama, ttl, npm, thnMasuk, thnLulus, noIjazah, gelar = dataMhs
    
    dirNama, dirNik = getDirekturData()
    
    param21, param22, param23, param24, param25, param26, param27, param28, param29, param210, param211, param212 = getInstitutionInformation(prodi)
    
    dataTTDDirektur = [
        ['', Paragraph(f'<font size="10">Bandung, {tglTTD}</font><br /><font size="10">Direktur Politeknik Pos Indonesia,</font>', styles["Center"])],
        [Image(pathTTD, 3.2 * cm, 3.2 * cm),
         Image("./skp/direktur.png", 5.2 * cm, 3.2 * cm)],
        ['', Paragraph(f'<font size="10"><b>{dirNama}</b></font><br /><font size="10"><b>NIK: {dirNik}</b></font>', styles["Center"])],
    ]
        
    dataColumn1 = [
        [personalInformation(nama, ttl, npm, thnMasuk, thnLulus, noIjazah, gelar)],
        # [''],
        [institutionInformation1(param21, param22, param23, param24)],
    ]
    
    tableColumn1 = Table(dataColumn1, [12.3*cm], None)
    tableColumn1.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        # ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        # ('BOX', (0,0), (-1,-1), 1, colors.black), 
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    
    dataColumn2 = [
        [institutionInformation2(param25, param26, param27, param28, param29, param210, param211, param212)],
        [ttdSurat(dataTTDDirektur)]
    ]
    
    tableColumn2 = Table(dataColumn2, [12.3*cm], None)
    tableColumn2.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        # ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        # ('BOX', (0,0), (-1,-1), 1, colors.black), 
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    
    data = [
        [tableColumn1, '', tableColumn2],
    ]
    
    table = Table(data, [12.3*cm, 1.2*cm, 12.3*cm], None)
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        # ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        # ('BOX', (0,0), (-1,-1), 1, colors.black), 
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    return table

def getMahasiswaByNpm(npm):
    db = kelas.dbConnectSiap()
    sql = f"select smm.Nama, smp.Nama, smp.Singkatan, smm.ProdiID, smm.Email from simak_mst_mahasiswa as smm, simak_mst_prodi as smp where smm.ProdiID=smp.ProdiID and smm.MhswID = '{npm}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return [row[0], row[1], row[2], row[3], row[4]]
    return False

def getNamaDosen(kodeDosen):
    db = kelas.dbConnectSiap()
    sql = f"select Nama, Gelar from simak_mst_dosen where Login = '{kodeDosen}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return f"{row[0].title()}, {row[1]}"
    return False

def checkDir(dir_path):
    if path.exists(dir_path):
        pass
    else:
        os.mkdir(dir_path)

def makeLinkVerifiy(kodeDosen, npm, role):
    datenow = datetime.datetime.date(datetime.datetime.now()).strftime('%d-%m-%Y')
    timenow = datetime.datetime.now().time().strftime('%H:%M:%S')
    module_name="skp"
    data = f'{module_name};{datenow};{timenow};{kodeDosen};{npm};{role};'
    makeit64 = f'{data}{bkd.randomString(64 - len(data))}'
    obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode('utf8'))
    cp = obj.encrypt(makeit64.encode("utf8"))
    passcode = cp.hex()
    space = '%20'
    link = f'https://api.whatsapp.com/send?phone={config.nomor_iteung}&text=iteung{space}tanda{space}tangan{space}{passcode}'
    return link

def makeQrcodeLinkVerifySign(link, npm, prodi):
    checkDir(f"./skp/qrcode-{prodi}/")
    img = qrcode.make(link)
    filepath = f'./skp/qrcode-{prodi}/qrcode-{npm}.png'
    img.save(filepath)
    return filepath

def verifyDigitalSign(resultpasscode):
    data = resultpasscode.split(';')
    tanggal = data[1]
    waktu = data[2]
    namaMhs, prodiMhs, singkatan, prodiID, email = getMahasiswaByNpm(data[4])
    namaDosen = getNamaDosen(data[3])
    role = 'Direktur' if data[5] == 'dir' else 'Wakil Direktur I'
    
    msgreply = f'Surat Keterangan Pendampin Ijazah {namaMhs} dari prodi {prodiMhs} telah ditandatangani oleh {namaDosen} sebagai {role} Politeknik Pos Indonesia, penerbitan tanda tangan pada {tanggal} jam {waktu}.'
    return msgreply

def columnTwoSecond(param3b, prodi, pathTTD):
    wadirNama, wadirNik = getWadirIData()
    
    dataTTDWadir1 = [
        ['', Paragraph(f'<font size="10">Bandung, {tglTTD}</font><br /><font size="10">Wadir 1 Bidang Akademik,</font>', styles["Center"])],
        [Image(pathTTD, 3.2 * cm, 3.2 * cm),
         Image("./skp/wadir1.png", 5.2 * cm, 2.3 * cm)],
        ['', Paragraph(f'<font size="10"><b>{wadirNama}</b></font><br /><font size="10"><b>NIK: {wadirNik}</b></font>', styles["Center"])],
    ]
        
    dataColumn1 = [
        [learningOutcome(prodi)],
    ]
    
    tableColumn1 = Table(dataColumn1, [12.3*cm], None)
    tableColumn1.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        # ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        # ('BOX', (0,0), (-1,-1), 1, colors.black), 
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    
    param3b1, param3b2, param3b3, param3b4, param3b5, param3b6, param3b7, npm = param3b
    
    dataColumn2 = [
        [additionalInformation(param3b1, param3b2, param3b3, param3b4, param3b5, param3b6, param3b7)],
        # [''],
        [ttdSurat(dataTTDWadir1)]
    ]
    
    tableColumn2 = Table(dataColumn2, [12.3*cm], None)
    tableColumn2.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        # ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        # ('BOX', (0,0), (-1,-1), 1, colors.black), 
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    
    data = [
        [tableColumn1, '', tableColumn2],
    ]
    
    table = Table(data, [12.3*cm, 1.2*cm, 12.3*cm], None)
    table.setStyle(TableStyle([
        ('FONT',(0,0),(-1,-1),'Arial', 8),
        # ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        # ('BOX', (0,0), (-1,-1), 1, colors.black), 
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    
    return table

def getWadir1():
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY FROM simak_mst_pejabat WHERE JenisJabatanID='2'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

def getDirektur():
    db = kelas.dbConnectSiap()
    sql = f"SELECT NIPY FROM simak_mst_pejabat WHERE JenisJabatanID='1'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None
    
def getKodeDosen(nik):
    db = kelas.dbConnectSiap()
    sql = f'select Login from simak_mst_dosen where NIPY="{nik}"'
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return row[0]
        else:
            return None

def sendEmail(email, fileName, path, mhs):
    try:
        subject = f"Surat Keterangan Pendamping Ijazah {mhs}"
        body = f"Berikut ini saya lampirkan surat keterangan pendamping ijazah {mhs}. Harap pergunakan surat ini dengan sebaik-baiknya."

        sender_email = config.email_iteung
        receiver_email = email
        # print(email)
        # receiver_email = 'divakrishnam@yahoo.com'
        password = config.pass_iteung

        message = MIMEMultipart()
        message["From"] = f'ITeung <{config.email_iteung}>'
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        with open(path+fileName, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            "attachment; filename= %s " % fileName,
        )

        message.attach(part)
        
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

        print(f'File {fileName} berhasil dikirim ke {email}')
    except FileNotFoundError:
        print("File tidak ditemukan")
    except Exception as e: 
        print(str(e))

def makeHeader(contain):
    contain.append(Image("./skp/logo.png", 1.6 * cm, 1.5 * cm))
    contain.append(Spacer(1, .1*cm))
    contain.append(Paragraph(f'<font size="13">POLITEKNIK POS INDONESIA</font>', styles["Center"]))
    contain.append(Spacer(1, .4*cm))
    contain.append(Paragraph(f'<font size="9"><b>Diploma Supplement</b></font>', styles["Center"]))
    contain.append(Spacer(1, 0.05*cm))
    contain.append(Paragraph(f'<font size="9">Surat Keterangan Pendamping Ijazah</font>', styles["Header"]))
    contain.append(Spacer(1, .1*cm))
    

def makePage(npm, prodi, email, dataMhs, param3b, idSurat):
    
    filepath = f"./skp/skp-{prodi}/"
    filename = f"{npm}.pdf"
    
    checkDir(filepath)
    
    fullfilename = filepath+filename
  
    doc = SimpleDocTemplate(fullfilename, 
                        pagesize=landscape(A4),
                        rightMargin=0*cm,
                        leftMargin=0*cm,
                        topMargin=0*cm,
                        bottomMargin=0*cm)

    contain=[]
    
    contain.append(Spacer(1, 1.4*cm))
    makeHeader(contain)
    
    contain.append(noSurat(npm, dataMhs[5], idSurat))
    contain.append(Spacer(1, .1*cm))

    contain.append(keteranganSurat())
    contain.append(Spacer(1, .1*cm))

    nipyDirektur = getDirektur()
    linkDir = makeLinkVerifiy(getKodeDosen(nipyDirektur), npm, "dir")
    pathTTDDir = makeQrcodeLinkVerifySign(linkDir, npm, prodi)

    contain.append(columnTwoFirst(dataMhs, prodi, pathTTDDir))
    contain.append(PageBreak())
    
    nipyWadir1 = getWadir1()
    linkWadir1 = makeLinkVerifiy(getKodeDosen(nipyWadir1), npm, "wadir1")
    pathTTDWadir1 = makeQrcodeLinkVerifySign(linkWadir1, npm, prodi)

    contain.append(Spacer(1, 1.5*cm))
    contain.append(columnTwoSecond(param3b, prodi, pathTTDWadir1))

    doc.build(contain, onFirstPage=pageSetup, onLaterPages=pageSetup)
    
    sendEmail(email, filename, filepath, npm)
