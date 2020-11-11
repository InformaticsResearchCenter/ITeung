from lib import message
from lib import numbers

from module import kelas

import config

def auth(data):
    return True

def replymsg(driver, data):
    msg = message.normalize(data[3])
    num = numbers.normalize(data[0])
    try:
        nama_lengkap=msg.split(' nama lengkap ')[1].split(' email ')[0]
        email=data[3].lower().replace(':', '').replace(',', '').replace('\n', '').split(' email ')[1].split(' alamat lengkap ')[0]
        alamat_lengkap=data[3].lower().replace(':', '').replace(',', '').replace('\n', '').split(' alamat lengkap ')[1]
    except:
        return 'salah keywordnya nihhh, formatnya seperti ini yaaa.' \
               '\n*iteung daftar seminar nama lengkap: tri angga dio Simamora, email: trianggadio@gmail.com, alamat lengkap: JL. SariAsih No. 54, Kota Bandung*'
    if isTerdaftar(num):
        updateDataSeminar(nama_lengkap, email, num, alamat_lengkap)
        return f'Nomor anda ({num}) sudah terdaftar sebagai peserta dan sudah {config.bot_name} update untuk datanya sebagai berikut.\n\n' \
               f'Nama Lengkap: {nama_lengkap}\n' \
               f'No. Handphone: {num}\n' \
               f'E-Mail: {email}\n' \
               f'Alamat Lengkap: {alamat_lengkap}\n\n' \
               f'Mohon kehadirannya tepat waktu, {config.bot_name} ucapkan Terima Kasih.'
    daftarSeminar(nama_lengkap, email, num, alamat_lengkap)
    return f'oke sudah {config.bot_name} daftarin ya berikut datanya.\n\n' \
           f'Nama Lengkap: {nama_lengkap}\n' \
           f'No. Handphone: {num}\n' \
           f'E-Mail: {email}\n' \
           f'Alamat Lengkap: {alamat_lengkap}\n\n' \
           f'Mohon kehadirannya tepat waktu yaaa, {config.bot_name} ucapkan Terima Kasih'



def isTerdaftar(phone_number):
    db=kelas.dbConnect()
    sql=f'select * from seminar_iteung where nomor_hp = "{phone_number}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        if cur.fetchone():
            return True
        return False

def daftarSeminar(nama_lengkap, email, nomor_hp, alamat_lengkap):
    db=kelas.dbConnect()
    sql=f'INSERT INTO `wanda`.`seminar_iteung`' \
        f'(`id`, `nama_lengkap`, `email`, `nomor_hp`, `alamat_lengkap`) ' \
        f'VALUES ' \
        f'(DEFAULT, "{nama_lengkap}", "{email}", "{nomor_hp}", "{alamat_lengkap}");'
    with db:
        cur=db.cursor()
        cur.execute(sql)

def updateDataSeminar(nama_lengkap, email, nomor_hp, alamat_lengkap):
    db=kelas.dbConnect()
    sql=f'UPDATE `wanda`.`seminar_iteung` ' \
        f'SET ' \
        f'`nama_lengkap` = "{nama_lengkap}", ' \
        f'`email` = "{email}", ' \
        f'`alamat_lengkap` = "{alamat_lengkap}" ' \
        f'WHERE ' \
        f'`nomor_hp` = "{nomor_hp}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)