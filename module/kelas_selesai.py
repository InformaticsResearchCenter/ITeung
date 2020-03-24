from module import kelas

def replymsg(driver, data):
    msgreply = 'oke selesai crot!'
    grp = data[1]
    num = data[0]
    coursename = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[1]
    starttimeclass = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[3]
    endtimeclass = kelas.getDataMatkul(grp.split('-')[0], kelas.kodeKelas(grp.split('-')[1]), num)[4]
    kelas.beritaAcara(driver, num, coursename, starttimeclass, endtimeclass, grp)
    return msgreply