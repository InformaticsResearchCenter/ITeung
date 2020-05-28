from lib import wa, reply, message, numbers
from module import kelas, bimbingan_mahasiswa
from datetime import datetime, timedelta
from Crypto.Cipher import AES
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
    datefromdatabasehomebase=getStartDate(num)
    if datefromdatabasehomebase is None:
        msgreply='wahhh kayaknya jadwal start bimbingannya belum diset sama kaprodi kamu deehhhh, coba minta di setting dulu jadwalnya....'
    else:
        startdate = datetime.date(datefromdatabasehomebase)
        pertemuan, datemulai, dateakhir=countPertemuan(startdate)
        if pertemuan==False:
            msgreply='yahhh pertemuannya udah kelewat batasss, yang sabar yaaaaaa..... :('
        else:
            successsplit=''
            try:
                studentid = msg.split('bimbingan ')[1].split(' ')[1]
                tipe=msg.split('bimbingan ')[1].split(' ')[0]
                target_selesai=msg.split('sudah dikerjakan ')[1].split(' pekerjaan selanjutnya')[0]
                terget_selanjutnya=msg.split('pekerjaan selanjutnya ')[1].split(' nilai')[0]
                topik=target_selesai+';'+terget_selanjutnya
                nilai=msg.split('nilai ')[1].split(' passcode')[0]
                passcode=msg.split('passcode ')[1]
            except:
                successsplit='error'
            if successsplit == 'error':
                msgreply='wahhhh salah nih keywordnya coba diperbaikin deh....'
            else:
                obj = AES.new(config.key, AES.MODE_CBC, config.iv)
                dec = bytes.fromhex(passcode)
                resultpasscode=obj.decrypt(dec).decode('utf-8')
                datenow = datetime.date(datetime.now()).strftime('%d%m%Y')
                hari = datetime.now().strftime('%A')
                hari = bimbingan_mahasiswa.hariSwitcher(hari)
                studentphonenumber=kelas.getStudentPhoneNumberFromNPM(studentid)
                studentphonenumber=normalizePhoneNumberToWhatsappVersion(studentphonenumber)
                logmsg=''
                for i in getLogMessageStudent(datemulai, dateakhir, kelas.getKodeDosen(num), studentphonenumber):
                    if i[0] != '':
                        logmsg+=i[0]+';'
                if logmsg=='':
                    msgreply='mohon maaf tidak ada diskusi diantara Dosen dan Mahasiswa maka tidak bisa di input... atau dosen dan mahasiswa kurang aktif diskusi'
                else:
                    if resultpasscode == studentid+datenow+hari:
                        if int(nilai) > 100:
                            msgreply='buset nilainya kaga salah itu bos?? gede benerr......'
                        else:
                            if isSudahInputBimbingan(studentid, pertemuan):
                                updateNilaiBimbingan(studentid=studentid, nilai=nilai, topik=topik, pertemuan=pertemuan, logmsg=logmsg)
                                msgreply='oke sudah iteung update yaaa nilainya.....'
                            else:
                                insertBimbingan(studentid=studentid, lecturerid=kelas.getKodeDosen(num), tipe=tipe, topik=topik, nilai=nilai, pertemuan=pertemuan, logmsg=logmsg)
                                msgreply='oke sudah di input yaaa....'
                            nama=kelas.getStudentNameOnly(studentid)
                            for i in getDataBimbingan(studentid):
                                topik=i[3].split(';')
                                target_selesai=topik[0]
                                target_selanjutnya=topik[1]
                                datalog=i[7]
                                datalog=datalog.split(';')
                                msgreply+='\n\nNama: {nama}\nNPM: {studentid}\nTipe: {tipe}\nPertemuan: {pertemuanke}\nSudah Dikerjakan: {targetselesai}\nPekerjaan Selanjutnya: {targetselanjutnya}\nNilai: {nilai}\nPenilai: {penilai}\nLog: {log}'.format(
                                    nama=nama,
                                    studentid=i[0],
                                    tipe=i[1],
                                    pertemuanke=i[2],
                                    targetselesai=target_selesai,
                                    targetselanjutnya=target_selanjutnya,
                                    nilai=i[4],
                                    penilai=i[5],
                                    log=str(len(datalog))
                                )
                    else:
                        msgreply='passcodenya salah bosqueeeeee'
    return msgreply

def countPertemuan(startdate):
    nowdate=datetime.date(datetime.now())
    countday = 7
    for i in range(10):
        if nowdate >= startdate and nowdate < startdate+timedelta(countday):
            pertemuan=i+1
            mulaidate=startdate
            akhirdate=startdate+timedelta(countday)
            print(mulaidate)
            print(akhirdate)
            break
        else:
            pertemuan=False
        startdate+=timedelta(countday)
    return pertemuan, mulaidate, akhirdate

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
        else:
            ret=None
    return ret

def insertBimbingan(studentid, lecturerid, tipe, pertemuan, nilai, topik, logmsg):
    db=kelas.dbConnectSiap()
    sql="INSERT INTO `simpati`.`simak_croot_bimbingan`(`kodepertemuan`, `MhswID`, `DosenID`, `TahunID`, `Tipe`, `Pertemuan_`, `Nilai`, `Topik`, `Tanggal`, `Penilai`, `Log`) VALUES (DEFAULT, '{studentid}', '{lecturerid}', '{tahunid}', '{tipe}', {pertemuan}, {nilai}, '{topik}', '{tanggal}', '{penilai}', '{logmsg}')".format(
        studentid=studentid,
        lecturerid=lecturerid,
        penilai=lecturerid,
        tahunid=kelas.getTahunID(),
        tipe=tipe,
        nilai=nilai,
        topik=topik,
        tanggal=datetime.now(),
        pertemuan=pertemuan,
        logmsg=logmsg
    )
    with db:
        cur=db.cursor()
        cur.execute(sql)

def isSudahInputBimbingan(studentid, pertemuan):
    db=kelas.dbConnectSiap()
    sql="select * from simak_croot_bimbingan where `MhswID`={studentid} and `Pertemuan_`={pertemuan} and `Tanggal`".format(studentid=studentid, pertemuan=pertemuan)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return True
        else:
            return False

def updateNilaiBimbingan(studentid, pertemuan, nilai, topik, logmsg):
    db=kelas.dbConnectSiap()
    sql="UPDATE `simpati`.`simak_croot_bimbingan` SET `Nilai` = {nilai}, `Topik` = '{topik}', `Tanggal` = '{datenow}', `Log` = '{logmsg}' WHERE `MhswID` = {studentid} and `Pertemuan_`={pertemuanke}".format(
        nilai=nilai,
        topik=topik,
        datenow=datetime.now(),
        studentid=studentid,
        pertemuanke=pertemuan,
        logmsg=logmsg
    )
    with db:
        cur=db.cursor()
        cur.execute(sql)

def getDataBimbingan(studentid):
    db=kelas.dbConnectSiap()
    sql="select MhswID, Tipe, Pertemuan_, Topik, Nilai, Penilai, Tanggal, Log from simak_croot_bimbingan where MhswID='{studentid}'".format(studentid=studentid)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchall()
    return row

def getLogMessageStudent(startdate, enddate, dosenid, phonenumber):
    db=kelas.dbConnect()
    sql="SELECT message FROM log WHERE timestamps >= '{startdate}' AND timestamps <= '{enddate}' AND number = '{phonenumber}' AND groupname='BIMBINGAN-{dosenid}'".format(
        startdate=startdate,
        enddate=enddate,
        phonenumber=phonenumber,
        dosenid=dosenid
    )
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchall()
        if row is not None:
            return row
        else:
            return None

def normalizePhoneNumberToWhatsappVersion(num):
    abc=num
    firstnumbersplit=2
    secondnumbersplit=5
    thirdnumbersplit=9
    fixnumber='+'+abc[:2]+' '+abc[firstnumbersplit:secondnumbersplit]+'-'+abc[secondnumbersplit:thirdnumbersplit]+'-'+abc[thirdnumbersplit:]
    return fixnumber