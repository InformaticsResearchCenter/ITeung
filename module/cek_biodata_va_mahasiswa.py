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
    virtual_account, customer_name, customer_email, customer_phone, trx_amount=getDataVaforMahasiswa(data[0])
    ws=app.openfile().active
    prodi_singkatan = app.getProdiSingkatanFromProdiID(kelas.getProdiIDwithStudentID(npm)).lower()
    tingkat = f"tk{int(datetime.now().strftime('%Y')) - int(kelas.getTahunAngkatanWithStudentID(npm)) + 1}"
    angkatan = kelas.getTahunAngkatanWithStudentID(npm)
    key = f'{prodi_singkatan}{tingkat}{angkatan}'
    biaya_pokok_spp = app.getDataDefault(key, ws)
    if trx_amount > biaya_pokok_spp:
        tunggakan=float(int(trx_amount)-int(biaya_pokok_spp))
        lima_puluh_persen_spp = int(biaya_pokok_spp / 2)
        minimum_pembayaran = tunggakan + lima_puluh_persen_spp
    else:
        tunggakan=float(0)
        minimum_pembayaran = int(biaya_pokok_spp / 2)
    app.openfile().close()
    ayah, ibu, handphoneortu=getNamaOrangTua(npm)
    msgreply=f'*BIODATA MAHASISWA*\n' \
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
             f'Biaya Pokok SPP: {app.floatToRupiah(float(biaya_pokok_spp))}\n' \
             f'Biaya Tunggakan SPP: {app.floatToRupiah(tunggakan)}\n' \
             f'Biaya Paket SPP Per Semester: {app.floatToRupiah(float(trx_amount))}\n' \
             f'Biaya Minimal Pembayaran: {app.floatToRupiah(float(trx_amount)/2)}\n' \
             f'Batas KRS: 12 Oktober 2020 - 16 Oktober 2020\n\n'\
             f'*CATATAN:* Untuk mempercepat layanan KRS Realtime *(langsung bayar langsung aktif dan bisa isi KRS)* anda diwajibkan melakukan pembayaran SPP menggunakan account VA anda, apabila pembayaran SPP tidak menggunakan account VA atau menggunakan metode transfer ke rekening YPBPI atau Giro Pos maka pengisian KRS dan aktivasi membutuhkan waktu 2 s.d 4 hari untuk mengecek bukti validasi pembayaran anda. Mohon kerjasamanya.'
    return msgreply

def getDataVaforMahasiswa(phonenumber):
    phonenumber = numbers.normalize(phonenumber)
    db=va_parent.dbConnectVA()
    sql=f"select virtual_account, customer_name, customer_email, customer_phone, trx_amount from upload where customer_phone='{phonenumber}' ORDER BY upload_id DESC LIMIT 1"
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