from module import va_parent, kelas
from lib import numbers
from datetime import datetime

import app, config

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]):
        return True
    else:
        return False

def replymsg(driver, data):
    npm, nama_mahasiswa, prodi_id, phonenumber, email, penasehat_akademik=getDataMahasiswa(data[0])
    ayah, ibu, handphoneortu = getNamaOrangTua(npm)
    msgreply = f'*BIODATA MAHASISWA*\n' \
               f'NPM: {npm}\n' \
               f'Nama: {nama_mahasiswa}\n' \
               f'Prodi: {kelas.getProdiNameWithStudentID(npm)}\n' \
               f'Nomor Handphone: {phonenumber}\n' \
               f'E-mail: {email}\n' \
               f'Dosen Wali: {kelas.getNamaDosen(penasehat_akademik)}\n' \
               f'Nama Orang Tua/Wali: {ayah} (Ayah) | {ibu} (Ibu)\n' \
               f'No HP orang Tua/Wali: {handphoneortu}\n\n'
    msgreply += paymentSpp(npm)
    msgreply += paymentSp(npm)
    msgreply += paymentTa(npm)
    msgreply += paymentUlang(npm)
    msgreply += paymentWisuda(npm)
    msgreply += paymentToefl(npm)
    msgreply += f'*CATATAN:* Untuk mempercepat layanan KRS Realtime *(langsung bayar langsung aktif dan bisa isi KRS)* anda diwajibkan melakukan pembayaran SPP menggunakan account VA anda, apabila pembayaran SPP tidak menggunakan account VA atau menggunakan metode transfer ke rekening YPBPI atau Giro Pos maka pengisian KRS dan aktivasi membutuhkan waktu 2 s.d 4 hari untuk mengecek bukti validasi pembayaran anda. Mohon kerjasamanya.'
    return msgreply

def getDataMahasiswa(phonenumber):
    phonenumber=numbers.normalize(phonenumber)
    db=kelas.dbConnectSiap()
    sql=f'select MhswID, Nama, ProdiID, Handphone, Email, PenasehatAkademik from simak_mst_mahasiswa where Handphone="{phonenumber}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row
        else:
            return None

def getNamaOrangTua(npm):
    db=kelas.dbConnectSiap()
    sql=f'select NamaAyah, NamaIbu, HandphoneOrtu from simak_mst_mahasiswa where MhswID={npm}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        return cur.fetchone()

def getSPP(npm):
    db=va_parent.dbConnectVA()
    sql=f"SELECT * FROM `upload` where trx_id like '%-SPP-%{npm}%' order by upload_id desc limit 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, data))
        else:
            result = None
        return result

def getTOEFL(npm):
    db=va_parent.dbConnectVA()
    sql=f"SELECT * FROM `upload` where trx_id like '%-TOEFL-%{npm}%' order by upload_id desc limit 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, data))
        else:
            result = None
        return result

def getSP(npm):
    db=va_parent.dbConnectVA()
    sql=f"SELECT * FROM `upload` where trx_id like '%-SP-%{npm}%' order by upload_id desc limit 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, data))
        else:
            result = None
        return result

def getULANG(npm):
    db=va_parent.dbConnectVA()
    sql=f"SELECT * FROM `upload` where trx_id like '%-ULANG-%{npm}%' order by upload_id desc limit 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, data))
        else:
            result = None
        return result

def getWISUDA(npm):
    db=va_parent.dbConnectVA()
    sql=f"SELECT * FROM `upload` where trx_id like '%-WISUDA-%{npm}%' order by upload_id desc limit 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, data))
        else:
            result = None
        return result

def getTA(npm):
    db=va_parent.dbConnectVA()
    sql=f"SELECT * FROM `upload` where trx_id like '%-TA-%{npm}%' order by upload_id desc limit 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, data))
        else:
            result = None
        return result

def paymentWisuda(npm):
    try:
        payment_wisuda = getWISUDA(npm)
        msgreply=''
        if datetime.now() < payment_wisuda['expired_date']:
            msgreply  = f'*DATA VIRTUAL ACCOUNT BNI WISUDA*\n\n' \
                        f'*Kode Transaksi: {payment_wisuda["trx_id"]}*\n' \
                        f'*Virtual Account: {payment_wisuda["virtual_account"]}*\n' \
                        f'Customer Name: {payment_wisuda["customer_name"]}\n' \
                        f'Customer Email: {payment_wisuda["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_wisuda["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_wisuda["trx_amount"]))}\n\n'
    except:
        msgreply=''
    return msgreply

def paymentUlang(npm):
    try:
        payment_ulang=getULANG(npm)
        msgreply = ''
        if datetime.now() < payment_ulang['expired_date']:
            msgreply = f'*DATA VIRTUAL ACCOUNT BNI ULANG*\n\n' \
                        f'*Kode Transaksi: {payment_ulang["trx_id"]}*\n' \
                        f'*Virtual Account: {payment_ulang["virtual_account"]}*\n' \
                        f'Customer Name: {payment_ulang["customer_name"]}\n' \
                        f'Customer Email: {payment_ulang["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_ulang["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_ulang["trx_amount"]))}\n\n'
    except:
        msgreply=''
    return msgreply

def paymentSp(npm):
    try:
        payment_sp=getSP(npm)
        msgreply = ''
        if datetime.now() < payment_sp['expired_date']:
            msgreply = f'*DATA VIRTUAL ACCOUNT BNI SP*\n\n' \
                       f'*Kode Transaksi: {payment_sp["trx_id"]}*\n' \
                       f'*Virtual Account: {payment_sp["virtual_account"]}*\n' \
                       f'Customer Name: {payment_sp["customer_name"]}\n' \
                       f'Customer Email: {payment_sp["customer_email"]}\n' \
                       f'Customer Phone Number: {payment_sp["customer_phone"]}\n' \
                       f'Jumlah Tagihan: {app.floatToRupiah(float(payment_sp["trx_amount"]))}\n\n'
    except:
        msgreply=''
    return msgreply

def paymentTa(npm):
    try:
        payment_ta=getTA(npm)
        msgreply = ''
        if datetime.now() < payment_ta['expired_date']:
            msgreply = f'*DATA VIRTUAL ACCOUNT BNI TA*\n\n' \
                        f'*Kode Transaksi: {payment_ta["trx_id"]}*\n' \
                        f'*Virtual Account: {payment_ta["virtual_account"]}*\n' \
                        f'Customer Name: {payment_ta["customer_name"]}\n' \
                        f'Customer Email: {payment_ta["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_ta["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_ta["trx_amount"]))}\n\n'
    except:
        msgreply=''
    return msgreply

def paymentToefl(npm):
    try:
        payment_toefl=getTOEFL(npm)
        msgreply = ''
        if datetime.now() < payment_toefl['expired_date']:
            msgreply = f'*DATA VIRTUAL ACCOUNT BNI TOEFL*\n\n' \
                        f'*Kode Transaksi: {payment_toefl["trx_id"]}*\n' \
                        f'*Virtual Account: {payment_toefl["virtual_account"]}*\n' \
                        f'Customer Name: {payment_toefl["customer_name"]}\n' \
                        f'Customer Email: {payment_toefl["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_toefl["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_toefl["trx_amount"]))}\n\n'
    except:
        msgreply=''
    return msgreply

def paymentSpp(npm):
    prodi_singkatan = app.getProdiSingkatanFromProdiID(kelas.getProdiIDwithStudentID(npm)).lower()
    tingkat = f"tk{int(kelas.getTahunID()[:-1]) - int(kelas.getTahunAngkatanWithStudentID(npm)) + 1}"
    angkatan = kelas.getTahunAngkatanWithStudentID(npm)
    payment_spp = getSPP(npm)
    if angkatan == '2020':
        return f'*DATA VIRTUAL ACCOUNT BNI SPP (Semester Ganjil 2020/2021)*\n\n' \
                   f'*Kode Transaksi: {payment_spp["trx_id"]}*\n' \
                   f'*Virtual Account: {payment_spp["virtual_account"]}*\n' \
                   f'Status Virtual Account: Aktif\n' \
                   f'Customer Name: {payment_spp["customer_name"]}\n' \
                   f'Customer Email: {payment_spp["customer_email"]}\n' \
                   f'Customer Phone Number: {payment_spp["customer_phone"]}\n' \
                   f'Jumlah Tagihan: {app.floatToRupiah(float(payment_spp["trx_amount"]))}\n'
    key = f'{prodi_singkatan}{tingkat}{angkatan}'
    ws = app.openfile().active
    biaya_pokok_spp = app.getDataDefault(key, ws)
    app.openfile().close()
    try:
        if biaya_pokok_spp:
            biaya_pokok_spp=int(biaya_pokok_spp)
        else:
            if prodi_singkatan[:2] == 'd4':
                biaya_pokok_spp = 2500000
            elif prodi_singkatan[:2] == 'd3':
                biaya_pokok_spp = 2000000
            else:
                biaya_pokok_spp = int(biaya_pokok_spp)
        if int(payment_spp['trx_amount']) > int(biaya_pokok_spp):
            tunggakan = float(int(payment_spp['trx_amount']) - int(biaya_pokok_spp))
            amount_tunggakan = int(payment_spp["trx_amount"]) - int(biaya_pokok_spp)
            fifty_percent_default_payment = int(biaya_pokok_spp) * (75/100)
            minimum_payment = int(amount_tunggakan) + int(fifty_percent_default_payment)
        else:
            tunggakan = float(0)
            potongan = int(biaya_pokok_spp) - int(payment_spp['trx_amount'])
            minimum_payment = (int(biaya_pokok_spp) - int(potongan)) * (75/100)
        if datetime.now() < payment_spp['expired_date']:
            msgreply = f'*DATA VIRTUAL ACCOUNT BNI SPP (Semester Genap 2020/2021)*\n\n' \
                       f'*Kode Transaksi: {payment_spp["trx_id"]}*\n' \
                       f'*Virtual Account: {payment_spp["virtual_account"]}*\n' \
                       f'Status Virtual Account: Aktif\n' \
                       f'Customer Name: {payment_spp["customer_name"]}\n' \
                       f'Customer Email: {payment_spp["customer_email"]}\n' \
                       f'Customer Phone Number: {payment_spp["customer_phone"]}\n' \
                       f'Biaya Paket SPP Per Semester: {app.floatToRupiah(float(biaya_pokok_spp))}\n' \
                       f'Biaya Tunggakan SPP: {app.floatToRupiah(tunggakan)}\n' \
                       f'Jumlah Tagihan: {app.floatToRupiah(float(payment_spp["trx_amount"]))}\n'
        else:
            msgreply = f'*DATA SPP TIDAK ADA*\n\n'
    except Exception as error:
        msgreply = f'Nomor Hp kamu Benerin dulu dongggg yang bener baru {config.bot_name} kasih liat datanya....\nATAU\nData kamu belum diupload..\n\n'
    return msgreply

def keyword_to_jenisBiaya(keyword_split, npm):
    for word in keyword_split:
        jenis_biaya=jenis_biaya_from_word(word, npm)
        if jenis_biaya:
            return jenis_biaya

def jenis_biaya_from_word(word, npm):
    switcher = {
        'spp': paymentSpp(npm),
        'toefl': paymentToefl(npm),
        'sp': paymentSp(npm),
        'wisuda': paymentWisuda(npm),
        'ulang': paymentUlang(npm),
        'ta': paymentTa(npm)
    }
    return switcher.get(word, False)