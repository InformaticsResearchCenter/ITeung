from module import kelas
from lib import wa
from datetime import datetime
import app, config

def auth(data):
    if kelas.getKodeDosen(data[0]) == 'NN257L':
        return True
    else:
        return False


def cekIsNpmExist(npm):
    if kelas.getDataMahasiswa(npm):
        return True
    else:
        return False


def getProdiName(prodiid):
    db=kelas.dbConnectSiap()
    sql=f'select Nama from simak_mst_prodi where ProdiID={prodiid}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]

def getTahunID():
    db=kelas.dbConnectSiap()
    sql="SELECT TahunID FROM simpati.simak_mst_tahun where NA = 'N' group by TahunID order by TahunID DESC limit 1"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        return row[0]


def insertLogApproval(data):
    db=kelas.dbConnect()
    sql=f"INSERT INTO `wanda`.`log_approval_va`(`log_id`, `MhswID`, `DosenID`, `SessionApproval`, `SisaPembayaran`, `TahunID`) VALUES (DEFAULT, '{data['npm']}', '{data['dosen_id']}', '{data['session_approval']}', {data['sisa_pembayaran']}, {data['tahun_id']});"
    with db:
        cur=db.cursor()
        cur.execute(sql)


def validTahunID():
    yearnow = datetime.now().strftime('%Y')
    tahunid = getTahunID()
    if (yearnow != str(tahunid[:-1])) and tahunid[-1] == '3':
        tahun_id_valid_for_va = f'{yearnow}{1}'
    else:
        tahun_id_valid_for_va = tahunid
    return tahun_id_valid_for_va

def cekSudahApprove(npm, tahunid):
    db=kelas.dbConnect()
    sql=f'select * from log_approval_va where MhswID={npm} and TahunID={tahunid}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return row

def replymsg(driver, data):
    msgs=data[3].split(' ')
    npm=''
    for i in msgs:
        if cekIsNpmExist(i):
            npm=i
    if npm == '':
        msgreply='NPM tidak ada/Invalid'
    else:
        if 'catatan' in data[3]:
            sisa_biaya = data[3].split(' sisa pembayaran ')[1].split(' catatan ')[0].replace('.', '')
        else:
            sisa_biaya = data[3].split(' sisa pembayaran ')[1].replace('.', '')
        tipesemester = validTahunID()[-1]
        prodiid = f'{npm[0]}{npm[3]}'
        if app.cekSudahAdaKHS(npm, validTahunID(), 'A'):
            msgreply = f'Mahasiswa dengan,\n\nNPM: {npm}\nNama: {kelas.getStudentNameOnly(npm)}\nProdi: {getProdiName(prodiid)}\n\nSudah bisa ambil KRS'
            if cekSudahApprove(npm, validTahunID()):
                data_verif=cekSudahApprove(npm, validTahunID())
                msgreply+=f' dan Sudah diverifikasi oleh,\n\nNama: *{kelas.getNamaDosen(data_verif[2])}*\nTanggal/Waktu: {data_verif[3]}'
        else:
            data_log={}
            data_log['npm']=npm
            data_log['dosen_id']=kelas.getKodeDosen(data[0])
            data_log['session_approval']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_log['sisa_pembayaran']=sisa_biaya
            data_log['tahun_id']=validTahunID()
            if 'catatan' in data[3]:
                catatan=data[3].split(' catatan ')[1]
            else:
                catatan='-'
            insertLogApproval(data_log)
            app.insertnewKHS(npm, validTahunID(), prodiid, app.cekSesiSemester(tipesemester, npm), sisa_biaya)
            wa.setOutbox(kelas.getStudentPhoneNumberFromNPM(npm), f'hai haiiiiii kamu dengan,{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}NPM: {npm}{config.whatsapp_api_lineBreak}Nama: {kelas.getStudentNameOnly(npm)}{config.whatsapp_api_lineBreak}Sisa Pembayaran: {app.floatToRupiah(float(sisa_biaya))}{config.whatsapp_api_lineBreak}Catatan: {catatan}{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}Sudah diverifikasi ya data pembayaran VA kamu oleh,{config.whatsapp_api_lineBreak}Nama: *{kelas.getNamaDosen(kelas.getKodeDosen(data[0]))}*')
            msgreply=f'Sudah {config.bot_name} approve yaaa va dengan data berikut:\n\nNPM: {npm}\nNama: {kelas.getStudentNameOnly(npm)}\nProdi: {getProdiName(prodiid)}\nSisa Pembayaran: {app.floatToRupiah(float(sisa_biaya))}\nCatatan: {catatan}\n\nAkan {config.bot_name} langsung informasikan ke mahasiswanya langsung yaaa'
    return msgreply