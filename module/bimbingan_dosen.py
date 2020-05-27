from lib import wa, reply, message, numbers
from module import kelas
from datetime import datetime, timedelta
import os, config

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    num=data[0]
    msg=data[3]
    msg=message.normalize(msg)
    startdate=datetime.date(getStartDate(num))
    if startdate=='NULL' or startdate=='':
        msgreply='wahhh kayaknya jadwal start bimbingannya belum diset sama kaprodi kamu deehhhh, coba minta di setting dulu jadwalnya....'
    else:
        pertemuan=countPertemuan(startdate)
        if pertemuan==False:
            msgreply='yahhh pertemuannya udah kelewat batasss, yang sabar yaaaaaa..... :('
        else:
            studentid = msg.split('bimbingan ')[1].split(' ')[1]
            tipe=msg.split('bimbingan ')[1].split(' ')[0]
            topik=msg.split('topik ')[1].split(' nilai')[0]
            nilai=msg.split('nilai ')[1]
            if int(nilai) > 100:
                msgreply='buset nilainya kaga salah itu bos?? gede benerr......'
            else:
                if isSudahInputBimbingan(studentid, pertemuan):
                    updateNilaiBimbingan(studentid=studentid, nilai=nilai, topik=topik, pertemuan=pertemuan)
                    msgreply='oke sudah iteung update yaaa nilainya.....'
                    ##update
                else:
                    insertBimbingan(studentid=studentid, lecturerid=kelas.getKodeDosen(num), tipe=tipe, topik=topik, nilai=nilai, pertemuan=pertemuan, )
                    msgreply='oke sudah di input yaaa....'
    return msgreply

def countPertemuan(startdate):
    nowdate=datetime.date(datetime.now())
    countday = 7
    for i in range(10):
        if nowdate >= startdate and nowdate < startdate+timedelta(countday):
            pertemuan=i+1
            break
        else:
            pertemuan=False
        startdate+=timedelta(countday)
    return pertemuan

def getStartDate(num):
    num=numbers.normalize(num)
    db=kelas.dbConnectSiap()
    sql="select `Start` from simak_mst_prodi WHERE ProdiID=(select Homebase from simak_mst_dosen WHERE Handphone='{phonenumber}')".format(phonenumber=num)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            ret=row[0]
    return ret

def insertBimbingan(studentid, lecturerid, tipe, pertemuan, nilai, topik):
    db=kelas.dbConnectSiap()
    sql="INSERT INTO `simpati`.`simak_croot_bimbingan`(`kodepertemuan`, `MhswID`, `DosenID`, `TahunID`, `Tipe`, `Pertemuan_`, `Nilai`, `Topik`, `Tanggal`, `Penilai`) VALUES (DEFAULT, '{studentid}', '{lecturerid}', '{tahunid}', '{tipe}', {pertemuan}, {nilai}, '{topik}', '{tanggal}', '{penilai}')".format(
        studentid=studentid,
        lecturerid=lecturerid,
        penilai=lecturerid,
        tahunid=kelas.getTahunID(),
        tipe=tipe,
        nilai=nilai,
        topik=topik,
        tanggal=datetime.now(),
        pertemuan=pertemuan
    )
    with db:
        cur=db.cursor()
        cur.execute(sql)

def isSudahInputBimbingan(studentid, pertemuan):
    db=kelas.dbConnectSiap()
    sql="select * from simak_croot_bimbingan where `MhswID`={studentid} and `Pertemuan_`={pertemuan}".format(studentid=studentid, pertemuan=pertemuan)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return False
        else:
            return True

def updateNilaiBimbingan(studentid, pertemuan, nilai, topik):
    db=kelas.dbConnectSiap()
    sql="UPDATE `simpati`.`simak_croot_bimbingan` SET `Nilai` = {nilai}, `Topik` = '{topik}', `Tanggal` = '{datenow}' WHERE `MhswID` = {studentid} and `Pertemuan_`={pertemuanke}".format(
        nilai=nilai,
        topik=topik,
        datenow=datetime.now(),
        studentid=studentid,
        pertemuanke=pertemuan
    )
    with db:
        cur=db.cursor()
        cur.execute(sql)