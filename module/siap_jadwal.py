from module import kelas
from lib import wa,reply

import os, subprocess

def auth(data):
    if kelas.getKodeDosen(data[0]) == '':
        ret=False
    else:
        ret=True
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    kodedosen=kelas.getKodeDosen(data[0])
    subprocess.Popen(["python", "main_jadwal_uts.py", kodedosen], cwd='module')