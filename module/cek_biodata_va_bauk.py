from lib import numbers
from module import kelas, cek_biodata_va_mahasiswa
from datetime import datetime
import app, config

def auth(data):
    if numbers.normalize(data[0]) == config.nomor_kepalaBAUK or numbers.normalize(data[0] == config.nomor_staffBAUK):
        return True
    else:
        return False

def replymsg(driver, data):
    msgs=data[3].split(' ')
    npm, status=cekNPM(msgs)
    if status:
        studentphonenumber=kelas.getStudentPhoneNumberFromNPM(npm)
        npm, nama_mahasiswa, prodi_id, phonenumber, email, penasehat_akademik = cek_biodata_va_mahasiswa.getDataMahasiswa(studentphonenumber)
        virtual_account, customer_name, customer_email, customer_phone, trx_amount = cek_biodata_va_mahasiswa.getDataVaforMahasiswa(studentphonenumber)
        ws = app.openfile().active
        prodi_singkatan = app.getProdiSingkatanFromProdiID(kelas.getProdiIDwithStudentID(npm)).lower()
        tingkat = f"tk{int(datetime.now().strftime('%Y')) - int(kelas.getTahunAngkatanWithStudentID(npm)) + 1}"
        angkatan = kelas.getTahunAngkatanWithStudentID(npm)
        key = f'{prodi_singkatan}{tingkat}{angkatan}'
        biaya_pokok_spp = app.getDataDefault(key, ws)
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
                   f'No HP orang Tua/Wali: {handphoneortu}\n\n' \
                   f'*DATA VIRTUAL ACCOUNT BNI (Semester Ganjil 2020/2021)*\n' \
                   f'Virtual Account: {virtual_account}\n' \
                   f'Status Virtual Account: Aktif\n' \
                   f'Customer Name: {customer_name}\n' \
                   f'Customer Email: {customer_email}\n' \
                   f'Customer Phone Number: {customer_phone}\n' \
                   f'Biaya Paket SPP Per Semester: {app.floatToRupiah(float(biaya_pokok_spp))}\n' \
                   f'Biaya Tunggakan SPP: {app.floatToRupiah(tunggakan)}\n' \
                   f'Jumlah Tagihan: {app.floatToRupiah(float(trx_amount))}\n' \
                   f'Biaya Minimal Pembayaran: {app.floatToRupiah(float(trx_amount) / 2)}\n' \
                   f'Batas KRS: 12 Oktober 2020 - 16 Oktober 2020\n\n' \
                   f'*CATATAN:* Untuk mempercepat layanan KRS Realtime *(langsung bayar langsung aktif dan bisa isi KRS)* anda diwajibkan melakukan pembayaran SPP menggunakan account VA anda, apabila pembayaran SPP tidak menggunakan account VA atau menggunakan metode transfer ke rekening YPBPI atau Giro Pos maka pengisian KRS dan aktivasi membutuhkan waktu 2 s.d 4 hari untuk mengecek bukti validasi pembayaran anda. Mohon kerjasamanya.'
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