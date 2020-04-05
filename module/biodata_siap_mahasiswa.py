from module import kelas
from lib import wa, reply

import os

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    msgreply=message(data)
    return msgreply

def message(data):
    msg = data[3]
    studentid = msg.split(' ')[-1]
    studentData = kelas.getDataMahasiswa(studentid)
    studentid = studentData[0]
    name = studentData[1]
    handphone = studentData[2]
    email = studentData[3]
    msgreply = "NPM: " + str(studentid) + \
               "\nNama: " + str(name) + \
               "\nHandphone: " + str(handphone) + \
               "\nE-mail: " + str(email)
    return msgreply