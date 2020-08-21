from module import kelas

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) == None:
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    npm, nama=kelas.getNpmandNameMahasiswa(data[0])
    judul=data[3].split(' pitak ')[1]
    updateJudulPitak(npm, judul, kelas.getTahunID())
    msgreply=f'oke sudah #BOTNAME# update judulnya menjadi {judul}'
    return msgreply

def updateJudulPitak(npm, judul, tahunid):
    db=kelas.dbConnect()
    sql=f"UPDATE `wanda`.`bimbingan_data` SET `judul` = '{judul}' WHERE `npm` = {npm} and `tahun_id`={tahunid}"
    with db:
        cur=db.cursor()
        cur.execute(sql)