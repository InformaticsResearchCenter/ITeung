from module import kelas

from lib import message

import config

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]):
        return True
    else:
        return False

def replymsg(driver, data):
    npm, nama = kelas.getNpmandNameMahasiswa(data[0])
    msg=data[3]
    msg=message.normalize(msg)
    try:
        pembimbing_1 = msg.split(' pembimbing 1 ')[1].split(' pembimbing 2 ')[0]
        pembimbing_2 = msg.split(' pembimbing 2 ')[1].split(' judul ')[0]
        judul = data[3].split(' judul ')[1]
    except:
        return f'aduuuu salah keyword nih bro bro bri brii.... coba dicek lagi yaa keywordnyaa....'
    if cekBimbinganData(npm):
        updateBimbinganData(
            npm,
            pembimbing_1.upper(),
            pembimbing_2.upper(),
            judul
        )
        return f'okeee sudah {config.bot_name} update menjadi\n\nNPM: {npm}\nNama: {nama}\nPembimbing 1: {kelas.getNamaDosen(pembimbing_1)}\nPembimbing 2: {"-" if pembimbing_2 == "-" else kelas.getNamaDosen(pembimbing_2)}\nJudul: {judul}'
    else:
        insertNewBimbinganData(
            npm,
            pembimbing_1.upper(),
            pembimbing_2.upper(),
            judul
        )
        return f'okeee sudah {config.bot_name} masukin yaaa datanya\n\nNPM: {npm}\nNama: {nama}\nPembimbing 1: {kelas.getNamaDosen(pembimbing_1)}\nPembimbing 2: {"-" if pembimbing_2 == "-" else kelas.getNamaDosen(pembimbing_2)}\nJudul: {judul}'

def insertNewBimbinganData(npm, pembimbing1, pembimbing2, judul):
    db=kelas.dbConnect()
    sql=f"INSERT INTO `wanda`.`bimbingan_data`(`npm`, `pembimbing1`, `pembimbing2`, `tahun_id`, `approval_pembimbing1`, `approval_pembimbing2`, `approval_koordinator1`, `approval_koordinator2`, `judul`) VALUES ('{npm}', '{pembimbing1}', '{pembimbing2}', '{kelas.getTahunID()}', 'false', 'false', 'false', 'false', '{judul}');"
    with db:
        cur=db.cursor()
        cur.execute(sql)

def updateBimbinganData(npm, pembimbing1, pembimbing2, judul, tahun_id=kelas.getTahunID()):
    db=kelas.dbConnect()
    sql=f"UPDATE `wanda`.`bimbingan_data` SET `pembimbing1` = '{pembimbing1}', `pembimbing2` = '{pembimbing2}', `judul` = '{judul}' WHERE `npm` = '{npm}' and tahun_id = '{tahun_id}';"
    with db:
        cur=db.cursor()
        cur.execute(sql)

def cekBimbinganData(npm, tahun_id=kelas.getTahunID()):
    db=kelas.dbConnect()
    sql=f"select * from bimbingan_data where npm={npm} and tahun_id={tahun_id}"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        if cur.fetchone() is not None:
            return True
        else:
            return False