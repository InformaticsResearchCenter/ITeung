from module import kelas, approve_kambing, berita_acara_pitak
from lib import numbers, message

def auth(data):
    if kelas.getKodeDosen(numbers.normalize(data[0])) == 'NN056L':
        ret=True
    else:
        ret=False
    return ret

def replymsg(driver, data):
    kode_dosen_approve=message.normalize(data[3]).split(' ')[-1]
    if kelas.getNamaDosen(kode_dosen_approve):
        npm_mahasiswa_list=berita_acara_pitak.getListMahasiswa(kode_dosen_approve.upper())
        datamahasiswa = ''
        for npm in npm_mahasiswa_list:
            data = approve_kambing.getDataPembimbing(npm, kode_dosen_approve.upper())
            pembimbingke = approve_kambing.pembimbingPositionAs(data, kode_dosen_approve.upper())
            updateApprovalKoordinator(npm, pembimbingke, pembimbingke.replace('pembimbing', 'koordinator'), kode_dosen_approve.upper(), 'true')
            datamahasiswa+=f'NPM: {npm}\nNama: {kelas.getStudentNameOnly(npm)}\n\n'
        msgreply=f'sudah di approve yaaa dengan Dosen {kelas.getNamaDosen(kode_dosen_approve.upper())} dan ini daftar mahasiswa bimbingannya:\n\n{datamahasiswa}'
    else:
        msgreply=f'aduhhhh #BOTNAME# nggak tau nih kode dosen {kode_dosen_approve} ini siapa yaaa.... ga bisa nemuin nih #BOTNAME# coba yaaaa diperhatikan lagiii....'
    return msgreply

def updateApprovalKoordinator(npm, pembimbingke, koordinatorke, kodedosen, status):
    db=kelas.dbConnect()
    sql=f"UPDATE `wanda`.`bimbingan_data` SET `approval_{koordinatorke}` = '{status}' WHERE `npm` = {npm} and {pembimbingke} = '{kodedosen}' and `tahun_id` = '{kelas.getTahunID()}';"
    with db:
        cur=db.cursor()
        cur.execute(sql)