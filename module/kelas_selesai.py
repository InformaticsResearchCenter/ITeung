from module import kelas

def replymsg(driver, data):
    grp = data[1]
    num = data[0]
    coursename = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[1]
    starttimeclass = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[3]
    endtimeclass = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[4]
    msgreply=kelas.siapAbsensi(driver=driver, namagroup=grp, num=num, namamatkul=kelas.getDataMatkul(kodematkul=grp.split('-')[0], kodekelas=grp.split('-')[1], num=num))
    msgreply=kelas.beritaAcara(driver=driver, num=num, coursename=coursename, starttimeclass=starttimeclass, endtimeclass=endtimeclass, groupname=grp, data=msgreply)
    return msgreply