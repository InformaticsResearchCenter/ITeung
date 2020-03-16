from lib import lecturerPhoneNumber

def mulaiMatkul(msg):
    msgs = msg.split(" ")
    getIndexStart = msgs.index("mulai")
    getIndexClass = msgs.index("kelas")
    matakuliah = listtostring(msgs[getIndexClass+1:getIndexStart])
    return matakuliah

def selesaiMatkul(msg):
    msgs = msg.split(" ")
    getIndexStart = msgs.index("selesai")
    getIndexClass = msgs.index("kelas")
    matakuliah = listtostring(msgs[getIndexClass+1:getIndexStart])
    return matakuliah

def listtostring(msg):
    msgs = ' '
    return msgs.join(msg)

def numberAuth(num):
    if num in lecturerPhoneNumber.phoneNumber:
        return True
    else:
        return False