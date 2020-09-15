from module import va_parent, kelas
from lib import numbers
from datetime import datetime

import app

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]):
        return True
    else:
        return False

def replymsg(driver, data):
    npm, nama_mahasiswa, prodi_id, phonenumber, email, penasehat_akademik=getDataMahasiswa(data[0])
    ws=app.openfile().active
    prodi_singkatan = app.getProdiSingkatanFromProdiID(kelas.getProdiIDwithStudentID(npm)).lower()
    tingkat = f"tk{int(datetime.now().strftime('%Y')) - int(kelas.getTahunAngkatanWithStudentID(npm)) + 1}"
    angkatan = kelas.getTahunAngkatanWithStudentID(npm)
    key = f'{prodi_singkatan}{tingkat}{angkatan}'
    biaya_pokok_spp = app.getDataDefault(key, ws)

    payment_spp = getSPP(npm)
    payment_toefl = getTOEFL(npm)
    payment_ta = getTA(npm)
    payment_sp = getSP(npm)
    payment_ulang = getULANG(npm)
    payment_wisuda = getWISUDA(npm)

    if payment_spp['trx_amount'] > biaya_pokok_spp:
        tunggakan=float(int(payment_spp['trx_amount'])-int(biaya_pokok_spp))
    else:
        tunggakan=float(0)

    app.openfile().close()
    ayah, ibu, handphoneortu=getNamaOrangTua(npm)
    msgreply = f'*BIODATA MAHASISWA*\n' \
               f'NPM: {npm}\n' \
               f'Nama: {nama_mahasiswa}\n' \
               f'Prodi: {kelas.getProdiNameWithStudentID(npm)}\n' \
               f'Nomor Handphone: {phonenumber}\n' \
               f'E-mail: {email}\n' \
               f'Dosen Wali: {kelas.getNamaDosen(penasehat_akademik)}\n' \
               f'Nama Orang Tua/Wali: {ayah} (Ayah) | {ibu} (Ibu)\n' \
               f'No HP orang Tua/Wali: {handphoneortu}\n\n'
    if payment_spp:
        msgreply+=f'*DATA VIRTUAL ACCOUNT BNI SPP (Semester Ganjil 2020/2021)*\n' \
                  f'Kode Transaksi: {payment_spp["trx_id"]}\n' \
                  f'Virtual Account: {payment_spp["virtual_account"]}\n' \
                  f'Status Virtual Account: Aktif\n' \
                  f'Customer Name: {payment_spp["customer_name"]}\n' \
                  f'Customer Email: {payment_spp["customer_email"]}\n' \
                  f'Customer Phone Number: {payment_spp["customer_phone"]}\n' \
                  f'Biaya Paket SPP Per Semester: {app.floatToRupiah(float(biaya_pokok_spp))}\n' \
                  f'Biaya Tunggakan SPP: {app.floatToRupiah(tunggakan)}\n' \
                  f'Jumlah Tagihan: {app.floatToRupiah(float(payment_spp["trx_amount"]))}\n' \
                  f'Biaya Minimal Pembayaran: {app.floatToRupiah(float(payment_spp["trx_amount"]) / 2)}\n' \
                  f'Batas KRS: 12 Oktober 2020 - 16 Oktober 2020\n\n'
    if payment_toefl:
        msgreply+=f'*DATA VIRTUAL ACCOUNT BNI SPP (Semester Ganjil 2020/2021)*\n' \
                  f'Kode Transaksi: {payment_toefl["trx_id"]}\n\n'
    if payment_ta:
        msgreply+=f'*DATA VIRTUAL ACCOUNT BNI TA (Semester Ganjil 2020/2021)*\n' \
                  f'Kode Transaksi: {payment_ta["trx_id"]}\n\n'
    if payment_sp:
        msgreply += f'*DATA VIRTUAL ACCOUNT BNI SP (Semester Ganjil 2020/2021)*\n' \
                    f'Kode Transaksi: {payment_sp["trx_id"]}\n\n'
    if payment_ulang:
        msgreply += f'*DATA VIRTUAL ACCOUNT BNI ULANG (Semester Ganjil 2020/2021)*\n' \
                    f'Kode Transaksi: {payment_ulang["trx_id"]}\n\n'
    if payment_wisuda:
        msgreply += f'*DATA VIRTUAL ACCOUNT BNI WISUDA (Semester Ganjil 2020/2021)*\n' \
                    f'Kode Transaksi: {payment_wisuda["trx_id"]}\n\n'
    msgreply+=f'*CATATAN:* Untuk mempercepat layanan KRS Realtime *(langsung bayar langsung aktif dan bisa isi KRS)* anda diwajibkan melakukan pembayaran SPP menggunakan account VA anda, apabila pembayaran SPP tidak menggunakan account VA atau menggunakan metode transfer ke rekening YPBPI atau Giro Pos maka pengisian KRS dan aktivasi membutuhkan waktu 2 s.d 4 hari untuk mengecek bukti validasi pembayaran anda. Mohon kerjasamanya.'
    return msgreply

def getDataVaforMahasiswa(phonenumber):
    phonenumber = numbers.normalize(phonenumber)
    db=va_parent.dbConnectVA()
    sql=f"select virtual_account, customer_name, customer_email, customer_phone, trx_amount, trx_id from upload where customer_phone='{phonenumber}' ORDER BY upload_id DESC LIMIT 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row
        else:
            return None

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