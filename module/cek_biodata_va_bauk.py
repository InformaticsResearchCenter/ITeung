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
        studentphonenumber=kelas.getStudentPhoneNumberFromNPM(npm)
        npm, nama_mahasiswa, prodi_id, phonenumber, email, penasehat_akademik = cek_biodata_va_mahasiswa.getDataMahasiswa(studentphonenumber)
        virtual_account, customer_name, customer_email, customer_phone, trx_amount, trx_id = cek_biodata_va_mahasiswa.getDataVaforMahasiswa(studentphonenumber)
        ws = app.openfile().active
        prodi_singkatan = app.getProdiSingkatanFromProdiID(kelas.getProdiIDwithStudentID(npm)).lower()
        tingkat = f"tk{int(datetime.now().strftime('%Y')) - int(kelas.getTahunAngkatanWithStudentID(npm)) + 1}"
        angkatan = kelas.getTahunAngkatanWithStudentID(npm)
        key = f'{prodi_singkatan}{tingkat}{angkatan}'
        biaya_pokok_spp = app.getDataDefault(key, ws)

        payment_spp = cek_biodata_va_mahasiswa.getSPP(npm)
        payment_toefl = cek_biodata_va_mahasiswa.getTOEFL(npm)
        payment_ta = cek_biodata_va_mahasiswa.getTA(npm)
        payment_sp = cek_biodata_va_mahasiswa.getSP(npm)
        payment_ulang = cek_biodata_va_mahasiswa.getULANG(npm)
        payment_wisuda = cek_biodata_va_mahasiswa.getWISUDA(npm)

        if trx_amount > biaya_pokok_spp:
            tunggakan = float(int(trx_amount) - int(biaya_pokok_spp))
        else:
            tunggakan = float(0)

        app.openfile().close()
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
        if payment_spp:
            msgreply += f'*DATA VIRTUAL ACCOUNT BNI SPP (Semester Ganjil 2020/2021)*\n\n' \
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
        if payment_toefl:
            msgreply += f'*DATA VIRTUAL ACCOUNT BNI TOEFL*\n\n' \
                        f'*Kode Transaksi: {payment_toefl["trx_id"]}*\n' \
                        f'*Virtual Account: {payment_toefl["virtual_account"]}*\n' \
                        f'Customer Name: {payment_toefl["customer_name"]}\n' \
                        f'Customer Email: {payment_toefl["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_toefl["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_toefl["trx_amount"]))}\n\n'
        if payment_ta:
            msgreply += f'*DATA VIRTUAL ACCOUNT BNI TA*\n\n' \
                        f'*Kode Transaksi: {payment_ta["trx_id"]}*\n' \
                        f'Virtual Account: {payment_ta["virtual_account"]}\n' \
                        f'Customer Name: {payment_ta["customer_name"]}\n' \
                        f'Customer Email: {payment_ta["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_ta["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_ta["trx_amount"]))}\n\n'
        if payment_sp:
            msgreply += f'*DATA VIRTUAL ACCOUNT BNI SP*\n\n' \
                        f'*Kode Transaksi: {payment_sp["trx_id"]}*\n' \
                        f'*Virtual Account: {payment_sp["virtual_account"]}*\n' \
                        f'Customer Name: {payment_sp["customer_name"]}\n' \
                        f'Customer Email: {payment_sp["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_sp["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_sp["trx_amount"]))}\n\n'
        if payment_ulang:
            msgreply += f'*DATA VIRTUAL ACCOUNT BNI ULANG*\n\n' \
                        f'*Kode Transaksi: {payment_ulang["trx_id"]}*\n' \
                        f'Virtual Account: {payment_ulang["virtual_account"]}\n' \
                        f'Customer Name: {payment_ulang["customer_name"]}\n' \
                        f'Customer Email: {payment_ulang["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_ulang["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_ulang["trx_amount"]))}\n\n'
        if payment_wisuda:
            msgreply += f'*DATA VIRTUAL ACCOUNT BNI WISUDA*\n\n' \
                        f'*Kode Transaksi: {payment_wisuda["trx_id"]}*\n' \
                        f'*Virtual Account: {payment_wisuda["virtual_account"]}*\n' \
                        f'Customer Name: {payment_wisuda["customer_name"]}\n' \
                        f'Customer Email: {payment_wisuda["customer_email"]}\n' \
                        f'Customer Phone Number: {payment_wisuda["customer_phone"]}\n' \
                        f'Jumlah Tagihan: {app.floatToRupiah(float(payment_wisuda["trx_amount"]))}\n\n'
        msgreply += f'*CATATAN:* Untuk mempercepat layanan KRS Realtime *(langsung bayar langsung aktif dan bisa isi KRS)* anda diwajibkan melakukan pembayaran SPP menggunakan account VA anda, apabila pembayaran SPP tidak menggunakan account VA atau menggunakan metode transfer ke rekening YPBPI atau Giro Pos maka pengisian KRS dan aktivasi membutuhkan waktu 2 s.d 4 hari untuk mengecek bukti validasi pembayaran anda. Mohon kerjasamanya.'
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