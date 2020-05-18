from lib import wa, numbers
from datetime import datetime
from time import sleep

import config
import pymysql
import requests


# def replymsg(driver, data):
#     log.logSaveIteungStart(data)
#     msg = data[3]
#     grp = data[1]
#     num = data[0]
#     msg = message.normalize(msg)
#     msgs = list(msg.split(" "))
#     coursename=getDataMatkul(grp.split('-')[0], kodeKelas(grp.split('-')[1]), num)[1]
#     starttimeclass=getDataMatkul(grp.split('-')[0], kodeKelas(grp.split('-')[1]), num)[3]
#     endtimeclass=getDataMatkul(grp.split('-')[0], kodeKelas(grp.split('-')[1]), num)[4]
#     if msgs[-1] == 'mulai':
#         if sudahinput(wa.getGroupName(driver)) == True:
#             msgreply = "mohon maaf matakuliah ini tidak bisa dimulai, mohon menunggu hingga minggu depan... terima kasih"
#         else:
#             if isMatkul(grp.split('-')[0], kodeKelas(grp.split('-')[1]), num):
#                 messages=getAwaitingMessageKelasStart('kelas')
#                 messages=messages.replace('#MATKUL#', coursename)
#                 messages=messages.replace('#BOTNAME#', config.bot_name)
#                 msgreply=messages
#             else:
#                 msgreply='mohon maaf kode dosen bapak/ibu dengan kode matkul ini tidak ditemukan'
#     else:
#         msgreply='oke selesai crot!'
#         beritaAcara(driver, num, coursename, starttimeclass, endtimeclass, grp)
#     return msgreply

def dbConnect():
    db = pymysql.connect(config.db_host, config.db_username, config.db_password, config.db_name)
    return db


def dbConnectSiap():
    db = pymysql.connect(config.db_host_siap, config.db_username_siap, config.db_password_siap, config.db_name_siap)
    return db

def switcherJurusan(kode):
    switcher = {
        '.13.': 'D3 Teknik Informatika',
        '.14.': 'D4 Teknik Informatika',
        '.23.': 'D3 Manajemen Informatika',
        '.33.': 'D3 Akuntansi',
        '.34.': 'D4 Akuntansi',
        '.43.': 'D3 Manajemen Bisnis',
        '.44.': 'D4 Manajemen Bisnis',
        '.53.': 'D3 Logistik Bisnis',
        '.54.': 'D4 Logistik Bisnis',
    }
    return switcher.get(kode, "Not Found!")

def kodeKelas(kode):
    switcher = {
        'A': '01',
        'B': '02',
        'C': '03',
        'D': '04',
        'E': '05',
        'F': '06',
        'G': '07',
        'H': '08',
        'I': '09',
        'J': '10',
        'RPL': '20'
    }
    return switcher.get(kode, "Not Found!")


def toKelas(kode):
    switcher = {
        '01': 'A',
        '02': 'B',
        '03': 'C',
        '04': 'D',
        '05': 'E',
        '06': 'F',
        '07': 'G',
        '08': 'H',
        '09': 'I',
        '10': 'J',
        '20': 'RPL'
    }
    return switcher.get(kode, "Not Found!")


def toHari(kode):
    switcher = {
        '1': 'Senin',
        '2': 'Selasa',
        '3': 'Rabu',
        '4': 'Kamis',
        '5': 'Jumat',
        '6': 'Sabtu',
        '7': 'Minggu',
    }
    return switcher.get(kode, "Not Found!")


def getnumonly(groupname):
    db = dbConnect()
    sql = "select distinct number from log where DATE_FORMAT(timestamps, '%Y-%m-%d') = CURDATE() and groupname = '{0}'".format(
        groupname)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        if rows is not None:
            return rows
        else:
            return ''


def getNpmandNameMahasiswa(num):
    num = numbers.normalize(num)
    db = dbConnectSiap()
    sql = "select MhswID, Nama from simak_mst_mahasiswa where Handphone = '{0}'".format(num)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            return rows


def getStudentNameOnly(npm):
    db = dbConnectSiap()
    sql = "select Nama from simak_mst_mahasiswa where MhswID = '{0}'".format(npm)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
    return rows[0]

def getStudentIDOnly(npm):
    db = dbConnectSiap()
    sql = "select MhswID from simak_mst_mahasiswa where MhswID = '{0}'".format(npm)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
    return rows[0]

def isParent(num):
    db=dbConnectSiap()
    num=numbers.normalize(num)
    sql="select * from simak_mst_mahasiswa where HandphoneOrtu='{parentnumberphone}'".format(parentnumberphone=num)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            ret=True
        else:
            ret=False
    return ret

def getHandphoneMahasiswa(npm):
    db = dbConnectSiap()
    sql = "select Handphone from simak_mst_mahasiswa where MhswID = '{0}'".format(npm)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            return rows[0]


def isMatkul(jadwalid):
    db = dbConnectSiap()
    sql = "select MKKode, Nama, HariID, JamMulai, JamSelesai, NamaKelas from simak_trn_jadwal where JadwalID={jadwalid}".format(jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            return True
        else:
            return False

def getListMK(kodedosen):
    listMK = 'Jadwal ID | Mata Kuliah | Kelas | Hari | Jam | Ruangan | Pertemuan\n '
    db = dbConnectSiap()
    sql = "select JadwalID, Nama, NamaKelas, HariID, JamMulai, JamSelesai, RuangID, Kehadiran from simak_trn_jadwal where DosenID = '{0}' and TahunID = '{1}'".format(kodedosen, config.siap_tahun_id)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        records = cur.fetchall()
        for row in records:
            listMK = listMK + str(row[0]) + ' | ' + str(row[1]) + ' | ' + toKelas(str(row[2])) + ' | ' + toHari(str(row[3])) + ' | ' + str(row[4])[:-3] + '-' + str(row[5])[:-3] + ' | ' + str(row[6]) + ' | ' +str(row[7]) +'\n '
    return listMK

def getMkDetails(jadwalid):
    db=dbConnectSiap()
    sql="select ProdiID, MKKode, Nama, JamMulai, JamSelesai, RuangID, NamaKelas from simak_trn_jadwal where JadwalID={jadwalid}".format(jadwalid=jadwalid)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
    return row

def getDataMatkul(jadwalid):
    db = dbConnectSiap()
    sql = "select MKKode, Nama, HariID, DATE_FORMAT(JamMulai, '%H:%i:%s'), DATE_FORMAT(JamSelesai, '%H:%i:%s'), NamaKelas from simak_trn_jadwal where JadwalID={jadwalid}".format(jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            return rows
        else:
            return ''

def getKehadiranMahasiswa(jadwalid, studentid):
    db=dbConnectSiap()
    sql="select COUNT(MhswID) from simak_trn_presensi_mahasiswa where JadwalID={jadwalid} and MhswID={studentid} and JenisPresensiID='{attentdancetype}'".format(jadwalid=jadwalid, studentid=studentid, attentdancetype='H')
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            return rows[0]
        else:
            return ''
def getDataMahasiswa(studentid):
    db=dbConnectSiap()
    sql="select MhswID, Nama, Handphone, Email from simak_mst_mahasiswa where MhswID={studentid}".format(studentid=studentid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        return rows

def getAllDataMahasiswa(studentid):
    db = dbConnectSiap()
    sql = "select * from simak_mst_mahasiswa where MhswID={studentid}".format(studentid=studentid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            ret=rows
        else:
            ret=''
    return ret

def getKodeDosen(num):
    num = numbers.normalize(num)
    kodedosen = ''
    db = dbConnectSiap()
    sql = "select Login from simak_mst_dosen where Handphone = '{0}'".format(num)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            kodedosen = rows[0]
    return kodedosen


def getAwaitingMessageKelasStart(module):
    db = dbConnect()
    content = ''
    sql = "SELECT content FROM waiting_message WHERE module_name = '{0}' AND content LIKE '%mulai%' ORDER BY RAND() LIMIT 1".format(
        module)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            content = rows[0]
    return content


def sudahinput(groupname):
    db = dbConnect()
    sql = "SELECT * from log WHERE DATE_FORMAT(timestamps, '%Y-%m-%d') = CURDATE() and groupname = '{0}' and message LIKE '%teung kelas mulai%'".format(
        groupname)
    status = False
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            status = True
    return status


def getJamTerakhir():
    db = dbConnect()
    tanggal = ''
    sql = "SELECT DATE_FORMAT(date_time, '%H:%i:%s') FROM d4ti_2b ORDER BY date_time DESC LIMIT 1"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            tanggal = rows[0]
    return tanggal


def getNamaDosen(kodedosen):
    db = dbConnectSiap()
    sql = "select Nama, Gelar from simak_mst_dosen where Login = '{0}'".format(kodedosen)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            namadosen = rows[0]
            gelar = rows[1]
            if gelar[0] == 'D' or gelar[0] == "I" or gelar[0] == 'i':
                return gelar + namadosen
            else:
                return namadosen + ' ' + gelar


def getHadirAlias(time):
    db = dbConnect()
    sql = "SELECT DISTINCT alias from d4ti_2b WHERE date_time > '{0}'".format(time)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

def getJadwalSerial(jadwalid):
    db=dbConnectSiap()
    sql="select JadwalSer from simak_trn_jadwal where JadwalID={jadwalid}".format(jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            ret=str(rows[0])
        else:
            ret=''
    return ret

def pesertaAbsensi(jadwalid):
    db = dbConnectSiap()
    sql = "select j.JadwalID, j.TahunID, j.MKKode, j.Nama, j.DosenID, krs.MhswID from simak_trn_jadwal as j join simak_trn_krs as krs where j.jadwalid = krs.jadwalid and j.tahunid=" + config.siap_tahun_id + " and j.JadwalID = '{0}'".format(
        jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    return rows


def getJadwalId(kelas, mkkode):
    db = dbConnectSiap()
    sql = "select JadwalID from simak_trn_jadwal where TahunID={0} and NamaKelas='{1}' and MKKode='{2}'".format(
        config.siap_tahun_id, kelas, mkkode)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        return rows[0]


def getLastpertemuan(kodedosen, jadwalid):
    db = dbConnectSiap()
    sql = "select Pertemuan from simak_trn_presensi_dosen where DosenID = '{0}' and TahunID = {1} and JadwalID = {2} GROUP BY Pertemuan DESC LIMIT 1".format(kodedosen, config.siap_tahun_id, jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            return rows[0]
        else:
            return ''


def getJamMulai(kodedosen, kodekelas):
    db = dbConnectSiap()
    sql = "select JamMulai from simak_trn_presensi_dosen where DosenID = '{0}' and TahunID = '{1}' and JadwalID = '{2}' order by Pertemuan DESC LIMIT 1".format(
        kodedosen, config.siap_tahun_id, kodekelas)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        return rows


def getJamSelesai(kodedosen, kodekelas):
    db = dbConnectSiap()
    sql = "select JamSelesai from simak_trn_presensi_dosen where DosenID = '{0}' and TahunID = '{1}' and JadwalID = '{2}' order by Pertemuan DESC LIMIT 1".format(
        kodedosen, config.siap_tahun_id, kodekelas)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        return rows


def getLastPresensiID(kodedosen, jadwalid):
    db = dbConnectSiap()
    sql = "select PresensiID from simak_trn_presensi_dosen where TahunID={tahunid} and DosenID='{kodedosen}' and JadwalID={jadwalid} ORDER BY Pertemuan DESC LIMIT 1".format(
        tahunid=config.siap_tahun_id, kodedosen=kodedosen, jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        return rows[0]


def getListNpm(num):
    studentnumber = num
    dataList = []
    for studentnum in studentnumber:
        if studentnum[0] != '' and getNpmandNameMahasiswa(studentnum[0]) != None:
            studentid = getNpmandNameMahasiswa(studentnum[0])[0]
            dataList.append(studentid)
    return dataList


def getDataKrs(studentid, mkkode):
    db = dbConnectSiap()
    sql = "select KRSID from simak_trn_krs where MhswID = '{studentid}' and TahunID = '{tahunid}' and MKKode = '{mkkode}'".format(
        studentid=studentid, tahunid=config.siap_tahun_id, mkkode=mkkode)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        return rows[0]


def getHadirNpm(time):
    db = dbConnect()
    sql = "SELECT DISTINCT npm from d4ti_2b WHERE date_time > '{0}'".format(time)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
    return rows

def RuangID(lecturercode, jadwalid):
    db = dbConnectSiap()
    sql = "select RuangID from simak_trn_jadwal WHERE TahunID={tahunid} and DosenID='{lecturercode}' and JadwalID={jadwalid}".format(tahunid=config.siap_tahun_id, lecturercode=lecturercode, jadwalid=jadwalid)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows[0].lower()[0] == 'l':
            return "(Praktek dan Teori)"
        else:
            return "(Teori)"

def prodiID(lecturercode, jadwalid):
    db = dbConnectSiap()
    sql="select ProdiID from simak_trn_jadwal WHERE TahunID={tahunid} and DosenID='{lecturercode}' and JadwalID={jadwalid}".format(tahunid=config.siap_tahun_id, lecturercode=lecturercode, jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        return switcherJurusan(rows[0])

def beritaAcara(driver, num, groupname, data, msg):
    coursename = getDataMatkul(groupname.split('-')[0])[1]
    starttimeclass = getDataMatkul(groupname.split('-')[0])[3]
    endtimeclass = getDataMatkul(groupname.split('-')[0])[4]
    lecturername=getNamaDosen(getKodeDosen(num))
    lecturercode=getKodeDosen(num)
    materi=msg.lower()
    materi=materi.split('materi')
    tanggal=datetime.now().strftime("%d-%m-%Y")
    kodekelas=kodeKelas(groupname.split('-')[1])
    jadwalid=groupname.split('-')[0]
    praktekteori=RuangID(lecturercode=lecturercode, jadwalid=jadwalid)
    homebase=prodiID(lecturercode=lecturercode, jadwalid=jadwalid)
    studentgrade=getTingkat(pesertaAbsensi(jadwalid=jadwalid))
    messages = "*(Sudah di input Iteung)*" + \
               "\nNama Dosen: " + str(lecturername) + \
               "\nMata Kuliah: " +str(coursename)+' '+str(praktekteori)+ \
               "\nMateri:" +str(materi[1]) + \
               "\nKelas: " +str(studentgrade)+''+str(toKelas(kodekelas)) + \
               "\nJurusan: " + str(homebase)+ \
               "\nTanggal: " + str(tanggal) + \
               "\nWaktu Mulai: " + str(starttimeclass) + \
               "\nWaktu Selesai: " + str(endtimeclass) + \
               "\nPertemuan ke: " + str(getLastpertemuan(kodedosen=lecturercode, jadwalid=jadwalid))
    messages = messages.split("\n")
    messages_top=""
    for msg in messages:
        messages_top+=msg+"\n"
    messages_bot=""
    number = 1
    studentidlist = data
    for studentid in studentidlist:
        if studentid != '' and studentid != None:
            studentname = getStudentNameOnly(studentid)
            messages_bot+=str(number) + ". " + studentid + " " + studentname + "\n"
            number = int(number) + 1
    message=messages_top+messages_bot
    wa.copyToClipboard(message)
    wa.pasteMessage(driver)
    wa.sendMessage(driver)
    #commit
    msgreply = "Oke teman-teman Matakuliah " + coursename + " sudah selesai dan telah berhasil diinputkan absensinya, mohon jaga kesehatan teman-teman yaaaa.... selalu cuci tangan teman-teman, dadaaaahhhhhh <3"
    return msgreply


def getTingkat(data):
    studentid=[]
    for i in data:
        npm=i[-1]
        studentid.append(npm)
    median = len(studentid) // 2
    print('median: ' + str(median))
    if median != 0:
        studentid = studentid[median - 1]
        print('studentnum: ' + str(studentid))
        npm = getStudentIDOnly(studentid)
        print('npm: ' + str(npm))
        thn2 = npm[1:3]
        selisih = int(config.siap_tahun_id[2:4]) - int(thn2)
        tingkat = str(selisih + 1)
    else:
        tingkat = ''
    return tingkat


def insertAbsenSiapDosen(jadwalid, pertemuan, lecturercode, tanggalinsert, jammulai, jamselesai, jamupdate, materi):
    db = dbConnectSiap()
    sql = "INSERT INTO `simak_trn_presensi_dosen`(`PresensiID`, `HonorDosenID`, `TahunID`, `JadwalID`, `Pertemuan`, `DosenID`, `Tanggal`, `JamMulai`, `JamSelesai`, `Durasi`, `Durasi_terlambat`, `Hitung`, `BAPID`, `Catatan`, `TunjanganSKS`, `TunjanganTransport`, `TunjanganTetap`, `NA`, `LoginBuat`, `TanggalBuat`, `LoginEdit`, `RuangID`, `TanggalEdit`, `status_bap`, `Jam_TapMasuk`, `Jam_TapKeluar`, `MP`) VALUES (DEFAULT, 0, '{tahunid}', {jadwalid}, {pertemuan}, '{kodedosen}', '{tanggalinsert}', '{jammulai}', '{jamselesai}', NULL, NULL, 'N', NULL, '', 0, 0, 0, 'N', 'ITeung', '{jamupdate}', NULL, '', '0000-00-00 00:00:00', 'BELUM', NULL, NULL, {materi})".format(
        tahunid=config.siap_tahun_id, jadwalid=jadwalid, pertemuan=pertemuan, kodedosen=lecturercode,
        tanggalinsert=tanggalinsert, jammulai=jammulai, jamselesai=jamselesai, jamupdate=jamupdate, materi=materi)
    with db:
        cur = db.cursor()
        cur.execute(sql)


def insertAbsenSiapMahasiswa(jadwalid, krsid, presensiid, studentid, attend, valueattend):
    db = dbConnectSiap()
    sql = "INSERT INTO `simak_trn_presensi_mahasiswa`(`PresensiMhswID`, `JadwalID`, `KRSID`, `PresensiID`, `MhswID`, `JenisPresensiID`, `Jam`, `Nilai`, `NA`, `Durasi_terlambat_mhs`) VALUES (DEFAULT, {jadwalid}, {krsid}, {presensiid}, '{studentid}', '{attend}', '00:00:00', {valueattend}, 'N', NULL)".format(
        jadwalid=jadwalid, krsid=krsid, presensiid=presensiid, studentid=studentid, attend=attend,
        valueattend=valueattend)
    with db:
        cur = db.cursor()
        cur.execute(sql)

def getKehadiran(jadwalid):
    db=dbConnectSiap()
    sql="SELECT Kehadiran from simak_trn_jadwal WHERE JadwalID={jadwalid}".format(jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            ret=int(rows[0])
        else:
            ret=''
    return ret

def updateKehadiran(jadwalid, pertemuan):
    db=dbConnectSiap()
    sql="UPDATE simak_trn_jadwal SET Kehadiran={pertemuan} WHERE JadwalID={jadwalid}".format(pertemuan=pertemuan, jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)

def updateAbsenSiapMahasiswa(presensiid, studentid, attend, valueattend):
    db = dbConnectSiap()
    sql = "UPDATE simak_trn_presensi_mahasiswa SET JenisPresensiID='{attend}', Nilai={valueattend} WHERE MhswID={studentid} and PresensiID={presensiid}".format(
        attend=attend, valueattend=valueattend, studentid=studentid, presensiid=presensiid)
    with db:
        cur = db.cursor()
        cur.execute(sql)

def getStudentIdFromParentPhoneNumber(num):
    num=numbers.normalize(num)
    db=dbConnectSiap()
    sql="select MhswID from simak_mst_mahasiswa where HandphoneOrtu='{parentnumberphone}'".format(parentnumberphone=num)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            ret=rows[0]
        else:
            ret=''
    return ret


def getStudentScores(studentid):
    db=dbConnectSiap()
    sql="select k.MhswID,m.Nama,k.JadwalID , mt.Nama as 'nama matkul',k.GradeNilai from simak_trn_krs as k,simak_mst_matakuliah as mt,simak_mst_mahasiswa as m where k.MKID=mt.MKID and k.MhswID=m.MhswID and k.TahunID={tahunid} and k.MhswID={npm}".format(tahunid=config.siap_tahun_id, npm=studentid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not None:
            ret=rows
        else:
            ret=''
    return ret

def studentattendance(grp, jadwalid):
    jadwalserial=getJadwalSerial(jadwalid=jadwalid)
    if jadwalserial == '0':
        jadwalid=jadwalid
    else:
        jadwalid=jadwalserial
    studentabsent = pesertaAbsensi(jadwalid=jadwalid)
    if studentabsent != ():
        datastudentabsenfromsiap = []
        for data in studentabsent:
            datastudentabsenfromsiap.append(data[-1])
        npmdata = []
        studentnumberphone = getnumonly(groupname=grp)
        for phonenumber in studentnumberphone:
            npm = getNpmandNameMahasiswa(numbers.normalize(phonenumber[0]))
            if npm is not None:
                npmdata.append(npm[0])
        attend = []
        for npm in npmdata:
            if npm in datastudentabsenfromsiap:
                index = datastudentabsenfromsiap.index(npm)
                attend.append(npm)
                datastudentabsenfromsiap.pop(index)
        notattend = []
        for notattendstudentid in datastudentabsenfromsiap:
            notattend.append(notattendstudentid)
        resultattend = []
        resultattend.append(attend)
        resultattend.append(notattend)
    else:
        resultattend=''
    return resultattend


def isSudahKelas(jadwalid, lecturercode):
    db = dbConnectSiap()
    sql = "select * from simak_trn_presensi_dosen where JadwalID={jadwalid} and DosenID='{lecturercode}' and Tanggal = CURRENT_DATE".format(
        jadwalid=jadwalid, lecturercode=lecturercode)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        if row is not None:
            return True
        else:
            return False

def getMkkode(jadwalid):
    db=dbConnectSiap()
    sql='select MKKode from simak_trn_jadwal WHERE JadwalID={jadwalid}'.format(jadwalid=jadwalid)
    with db:
        cur = db.cursor()
        cur.execute(sql)
        rows = cur.fetchone()
        if rows is not None:
            ret=rows[0]
        else:
            ret=''
    return ret

def getJumlahPertemuanMahasiswa(jadwalid, studentid, absentvalue):
    db=dbConnectSiap()
    sql="select COUNT(*) from simak_trn_presensi_mahasiswa where JadwalID={jadwalid} and MhswID={studentid} and JenisPresensiID='{absentvalue}'".format(jadwalid=jadwalid, studentid=studentid, absentvalue=absentvalue)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchone()
        if rows is not None:
            ret=rows[0]
    return ret

def updatePresensiKRS(presensi, jadwalid, studentid):
    db=dbConnectSiap()
    timenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql="UPDATE simak_trn_krs SET _Presensi={presensi}, TanggalEdit='{timeedit}' WHERE JadwalID={jadwalid} and MhswID={studentid}".format(presensi=presensi, timeedit=timenow, jadwalid=jadwalid, studentid=studentid)
    with db:
        cur=db.cursor()
        cur.execute(sql)

def cekSiap():
    req=requests.get(config.websiap)
    if req.status_code == 200:
        ret=True
    else:
        ret=False
    return ret

def siapabsensiwithsql(grp, num, materi):
    jadwalid = grp.split('-')[0]
    mkkode = getMkkode(jadwalid=jadwalid)
    lecturercode = getKodeDosen(num)
    resultattendance = studentattendance(grp=grp, jadwalid=jadwalid)
    if resultattendance != '':
        attend = resultattendance[0]
        notattend = resultattendance[1]
        if not isSudahKelas(jadwalid=jadwalid, lecturercode=lecturercode):
            lastpertemuan = getLastpertemuan(kodedosen=lecturercode, jadwalid=jadwalid)
            if lastpertemuan == '':
                lastpertemuan=0
            yearmonthdaynow = datetime.now().strftime("%Y-%m-%d")
            yearmonthdaytimenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            starttime = getDataMatkul(jadwalid=jadwalid)[3]
            endtime = getDataMatkul(jadwalid=jadwalid)[4]
            updateKehadiran(jadwalid=jadwalid, pertemuan=int(lastpertemuan)+1)
            insertAbsenSiapDosen(jadwalid=jadwalid, pertemuan=int(lastpertemuan) + 1, lecturercode=lecturercode,
                                 tanggalinsert=yearmonthdaynow, jammulai=starttime, jamselesai=endtime,
                                 jamupdate=yearmonthdaytimenow, materi=materi)
            presensiid = getLastPresensiID(kodedosen=lecturercode, jadwalid=jadwalid)
            for studentid in attend:
                krsid = getDataKrs(studentid=studentid, mkkode=mkkode)
                insertAbsenSiapMahasiswa(jadwalid=jadwalid, krsid=krsid, presensiid=presensiid, studentid=studentid,
                                         attend='H', valueattend=1)
                #ifx issues #29
                attendancestudent=getJumlahPertemuanMahasiswa(jadwalid=jadwalid, studentid=studentid, absentvalue='H')
                if attendancestudent is not None:
                    updatePresensiKRS(presensi=attendancestudent, jadwalid=jadwalid, studentid=studentid)
            for studentid in notattend:
                krsid = getDataKrs(studentid=studentid, mkkode=mkkode)
                insertAbsenSiapMahasiswa(jadwalid=jadwalid, krsid=krsid, presensiid=presensiid, studentid=studentid,
                                         attend='M', valueattend=0)
        else:
            presensiid = getLastPresensiID(kodedosen=lecturercode, jadwalid=jadwalid)
            for studentid in attend:
                updateAbsenSiapMahasiswa(presensiid=presensiid, studentid=studentid, attend='H', valueattend=1)
                attendancestudent = getJumlahPertemuanMahasiswa(jadwalid=jadwalid, studentid=studentid, absentvalue='H')
                if attendancestudent is not None:
                    updatePresensiKRS(presensi=attendancestudent, jadwalid=jadwalid, studentid=studentid)
    else:
        attend=''
    return attend


def siapabsensiwithweb(driver, num, namagroup):
    try:
        tanggalsekarang = datetime.now().strftime("%d/%m/%Y")
        namagroupsplit = namagroup.split("-")
        kodematkul = namagroupsplit[0]
        kodekelas = namagroupsplit[1]
        openSiapwithNewTab(driver)
        switchWindowsHandleto1(driver)
        try:
            loginSiap(driver)
        except:
            print("sudah login")
        sleep(1)
        openPresensi(driver)
        TahunAkad(driver)
        findLecturerCode(driver, getKodeDosen(num).lower())
        findMatkul(driver, kodematkul, kodekelas)
        gettanggalabsen = driver.find_elements_by_xpath(
            '/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr')
        gettanggalabsensiapterakhir = driver.find_element_by_xpath(
            '/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr[' + str(
                len(gettanggalabsen)) + ']/td[3]').text
        if tanggalsekarang == gettanggalabsensiapterakhir:
            AddMahasiswa(driver)
            hadir = Mahasiswa(driver, namagroup)
            Refresh(driver)
            closeTab(driver)
            switchWindowsHandleto0(driver)
        else:
            TambahPresensi(driver)
            simpan(driver)
            sleep(1)
            AddMahasiswa(driver)
            hadir = Mahasiswa(driver, namagroup)
            Refresh(driver)
            closeTab(driver)
            switchWindowsHandleto0(driver)
        msgreply = hadir
    except Exception as e:
        msgreply = "error: " + str(e)
        closeTab(driver)
        switchWindowsHandleto0(driver)
    return msgreply


def closeTab(driver):
    return driver.close()


def pertemuanke(driver):
    return driver.find_element_by_xpath(
        '/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr[1]/td[2]').text


def openSiapwithNewTab(driver):
    return driver.execute_script("window.open('http://siap.poltekpos.ac.id/siap/besan.depan.php');")


def switchWindowsHandleto1(driver):
    return driver.switch_to_window(driver.window_handles[1])


def switchWindowsHandleto0(driver):
    return driver.switch_to_window(driver.window_handles[0])


def loginSiap(driver):
    username = driver.find_elements_by_class_name("textbox")[0]
    username.send_keys(config.username_siap)

    sleep(1)

    password = driver.find_elements_by_class_name("textbox")[1]
    password.send_keys(config.password_siap)

    sleep(1)

    login = driver.find_element_by_class_name("button")
    login.click()


def openPresensi(driver):
    driver.get('http://siap.poltekpos.ac.id/siap/modul/simpati/index.php?mnux=jadwal.presensi&mdlid=63')


def findLecturerCode(driver, kodedosen):
    lecturercode = driver.find_elements_by_xpath(
        '/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p/table/tbody/tr[2]/td[2]/select/option')
    for i in lecturercode:
        kodesplit = i.text.split(" ")
        codeoflecturer = kodesplit[-1]
        codeoflecturer = codeoflecturer.lower()
        if kodedosen == codeoflecturer:
            i.click()
            break


def findMatkul(driver, matkul, kelas):
    listofmatkul = driver.find_elements_by_xpath(
        '/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p/table/tbody/tr[3]/td[2]/select/option')
    for data in listofmatkul:
        matkulsplit = data.text.split(" ")
        if matkulsplit[-1] == '---':
            kodematkul = ''
            kodekelas = ''
        else:
            kodematkul = matkulsplit[2]
            kodekelas = matkulsplit[-6]
        if kodematkul == matkul and kodekelas == kelas:
            data.click()
            break


def TambahPresensi(driver):
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[2]/table/tbody/tr[5]/td/input[2]").click()


def simpan(driver):
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr[7]/td/input[1]").click()


def AddMahasiswa(driver):
    jumTabel = driver.find_elements_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr")
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[3]/table/tbody/tr[" + str(
            len(jumTabel)) + "]/td[8]/a").click()


def Mahasiswa(driver, groupname):
    dataPhoneNumber = []
    jumMahasiswa = int(driver.find_elements_by_class_name("inp1")[-1].text)
    index = 1
    numberphone = getnumonly(groupname)
    data = []
    for number in numberphone:
        if getNpmandNameMahasiswa(number[0]) is not None:
            npmMahasiswa = getNpmandNameMahasiswa(number[0])[0]
            data.append(npmMahasiswa)
    for getNpm in range(jumMahasiswa):
        npm = driver.find_element_by_xpath(
            "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                index) + "]/td[2]").text
        if npm in data:
            driver.find_element_by_xpath(
                "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                    index) + "]/td[4]/select/option[1]").click()
            dataPhoneNumber.append(getHandphoneMahasiswa(npm))
        else:
            driver.find_element_by_xpath(
                "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[4]/table/tbody/tr[" + str(
                    index) + "]/td[4]/select/option[4]").click()
        index += 1
    dataPhoneNumber.append(pertemuanke(driver))
    return dataPhoneNumber


def Refresh(driver):
    driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[2]/table/tbody/tr[5]/td/input[3]").click()


def TahunAkad(driver):
    return driver.find_element_by_xpath(
        "/html/body/table/tbody/tr[5]/td/table[3]/tbody/tr[1]/td[2]/p[1]/table/tbody/tr[1]/td[3]/select/option[2]").click()
