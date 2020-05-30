from lib import wa, reply
from module import kelas, bimbingan_dosen
import os, config

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) == None:
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    studentid=kelas.getNpmandNameMahasiswa(data[0])[0]
    databimbingan=bimbingan_dosen.getDataBimbingan(studentid)
    if databimbingan == None:
        msgreply='mohon maaf data tidak dapat ditemukan...'
    else:
        msgreply='ini yaaa data bimbingannya ....'
        for i in databimbingan:
            nama=kelas.getStudentNameOnly(studentid)
            topik = i[3].split(';')
            target_selesai = topik[0]
            target_selanjutnya = topik[1]
            datalog = i[7]
            datalog = datalog.split(';')
            namadosen = kelas.getNamaDosen(i[5])
            msgreply += '\n\nNama: {nama}\nNPM: {studentid}\nTipe: {tipe}\nPertemuan: {pertemuanke}\nSudah Dikerjakan: {targetselesai}\nPekerjaan Selanjutnya: {targetselanjutnya}\nNilai: {nilai}\nPenilai: {penilai} / {namadosen}\nJumlah Percakapan: {log}'.format(
                nama=nama,
                studentid=i[0],
                tipe=i[1],
                pertemuanke=i[2],
                targetselesai=target_selesai,
                targetselanjutnya=target_selanjutnya,
                nilai=i[4],
                penilai=i[5],
                log=str(len(datalog)),
                namadosen=namadosen
            )
    return msgreply