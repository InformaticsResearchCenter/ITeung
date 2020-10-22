from module import kelas

from lib import message

def auth(data):
    return True

def replymsg(diver, data):
    msg=message.normalize(data[3])
    kode_beruntung=msg.split(' kode ')[1]
    if cekData(kode_beruntung):
        msgreply='ada hadiah'
    else:
        msgreply='tidak ada hadiah'
    return msgreply

def cekData(kode_beruntung):
    db=kelas.dbConnect()
    sql=f'select * from kode_beruntung where kode="{kode_beruntung}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        if cur.fetchone():
            return True
        else:
            return False