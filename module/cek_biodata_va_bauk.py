from lib import numbers
from module import kelas, cek_biodata_va_mahasiswa
from datetime import datetime
import app, config

def auth(data):
    if numbers.normalize(data[0]) == config.nomor_kepalaBAUK or numbers.normalize(data[0]) == config.nomor_staffBAUK or numbers.normalize(data[0]) == config.nomor_callcenterBAUK:
        return True
    else:
        return False

def replymsg(driver, data):
    msgs=data[3].split(' ')
    npm, status=cekNPM(msgs)
    if status:
        data_result=keyword_to_jenisBiaya(msgs, npm)
        if data_result:
            studentphonenumber=kelas.getStudentPhoneNumberFromNPM(npm)
            npm, nama_mahasiswa, prodi_id, phonenumber, email, penasehat_akademik = cek_biodata_va_mahasiswa.getDataMahasiswa(studentphonenumber)

            ayah, ibu, handphoneortu = cek_biodata_va_mahasiswa.getNamaOrangTua(npm)

            msgreply = f'*BIODATA MAHASISWA*\n' \
                       f'NPM: {npm}\n' \
                       f'Nama: {nama_mahasiswa}\n' \
                       f'Prodi: {kelas.getProdiNameWithStudentID(npm)}\n' \
                       f'Nomor Handphone: {phonenumber}\n' \
                       f'E-mail: {email}\n' \
                       f'Dosen Wali: {kelas.getNamaDosen(penasehat_akademik)}\n' \
                       f'Nama Orang Tua/Wali: {ayah} (Ayah) | {ibu} (Ibu)\n' \
                       f'No HP orang Tua/Wali: {handphoneortu}\n\n'

            msgreply += data_result

            msgreply += f'*CATATAN:* Untuk mempercepat layanan KRS Realtime *(langsung bayar langsung aktif dan bisa isi KRS)* anda diwajibkan melakukan pembayaran SPP menggunakan account VA anda, apabila pembayaran SPP tidak menggunakan account VA atau menggunakan metode transfer ke rekening YPBPI atau Giro Pos maka pengisian KRS dan aktivasi membutuhkan waktu 2 s.d 4 hari untuk mengecek bukti validasi pembayaran anda. Mohon kerjasamanya.'
        else:
            msgreply = f'jenis biaya tidak ditemukan atau tidak ada dalam keyword... tambahkan jenis biaya dikeywordnya yaa.. berikut jenis biayanya:\n1. spp\n2. toefl\n3. sp\n4. wisuda\n5. ulang\n6. ta'
    else:
        msgreply=f'npm tidak ditemukan/tidak valid'
    return msgreply

def cekNPM(msgs):
    for i in msgs:
        if kelas.getStudentNameOnly(i) != None:
            if kelas.getStudentNameOnly(i):
                return i, True
        else:
            continue

def paymentWisuda(npm):
    try:
        payment_wisuda = cek_biodata_va_mahasiswa.getWISUDA(npm)
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
        payment_ulang=cek_biodata_va_mahasiswa.getULANG(npm)
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
        payment_sp=cek_biodata_va_mahasiswa.getSP(npm)
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
        payment_ta=cek_biodata_va_mahasiswa.getTA(npm)
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
        payment_toefl=cek_biodata_va_mahasiswa.getTOEFL(npm)
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
    tingkat = f"tk{int(datetime.now().strftime('%Y')) - int(kelas.getTahunAngkatanWithStudentID(npm)) + 1}"
    angkatan = kelas.getTahunAngkatanWithStudentID(npm)
    key = f'{prodi_singkatan}{tingkat}{angkatan}'
    ws = app.openfile().active
    biaya_pokok_spp = app.getDataDefault(key, ws)
    app.openfile().close()
    payment_spp=cek_biodata_va_mahasiswa.getSPP(npm)
    try:
        if biaya_pokok_spp:
            biaya_pokok_spp=int(biaya_pokok_spp)
        else:
            biaya_pokok_spp=2500000
        if int(payment_spp['trx_amount']) > int(biaya_pokok_spp):
            tunggakan = float(int(payment_spp['trx_amount']) - int(biaya_pokok_spp))
        else:
            tunggakan = float(0)
        msgreply = f'*DATA VIRTUAL ACCOUNT BNI SPP (Semester Ganjil 2020/2021)*\n\n' \
                    f'*Kode Transaksi: {payment_spp["trx_id"]}*\n' \
                    f'*Virtual Account: {payment_spp["virtual_account"]}*\n' \
                    f'Status Virtual Account: Aktif\n' \
                    f'Customer Name: {payment_spp["customer_name"]}\n' \
                    f'Customer Email: {payment_spp["customer_email"]}\n' \
                    f'Customer Phone Number: {payment_spp["customer_phone"]}\n' \
                    f'Biaya Paket SPP Per Semester: {app.floatToRupiah(float(biaya_pokok_spp))}\n' \
                    f'Biaya Tunggakan SPP: {app.floatToRupiah(tunggakan)}\n' \
                    f'Jumlah Tagihan: {app.floatToRupiah(float(payment_spp["trx_amount"]))}\n' \
                    f'Biaya Minimal Pembayaran: {app.floatToRupiah(float(payment_spp["trx_amount"]) / 2)}\n' \
                    f'Batas KRS: 12 Oktober 2020 - 16 Oktober 2020\n\n'
    except:
        msgreply = f'Data untuk SPP dengan {npm} ini tidak memiliki biaya pokok\n\n'
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