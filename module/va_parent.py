import pymysql, config, os

from lib import wa, reply
from module import kelas

def auth(data):
    if kelas.isParent(data[0]):
        ret=True
    else:
        ret=False
    return ret

def replymsg(driver, data):
    num=data[0]
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    npmmahasiswa=kelas.getStudentIdFromParentPhoneNumber(num)
    msgreply=''
    for i in npmmahasiswa:
        vadata = getVaData(i[0])
        virtualaccount = vadata[0]
        jumlahygharusdibayar = vadata[1]
        jumlahterakhirbayar = vadata[2]
        jumlahygsudahdibayar = vadata[3]
        waktuterakhirbayar = vadata[4].strftime('%d-%m-%Y %H:%M:%S')
        customername=vadata[5]
        msgreply+="Nama: {customername}\nNomor virtual account: {virtualaccount}\nTotal yang harus dibayar: {jumlahygharusdibayar}\nTotal yang sudah dibayar: {jumlahygsudahdibayar}\n\nJumlah terakhir pembayaran: {jumlahterakhirbayar}\nWaktu terakhir pembayaran: {waktuterakhirbayar}\n\n".format(waktuterakhirbayar=waktuterakhirbayar, jumlahterakhirbayar=jumlahterakhirbayar, jumlahygsudahdibayar=jumlahygsudahdibayar, jumlahygharusdibayar=jumlahygharusdibayar, virtualaccount=virtualaccount, customername=customername)
    return msgreply

def dbConnectVA():
    db=pymysql.connect(config.db_host_va, config.db_username_va, config.db_password_va, config.db_name_va)
    return db

def getVaData(studentid):
    db=dbConnectVA()
    sql="select virtual_account, trx_amount, payment_amount, cumulative_payment_amount, datetime_payment, customer_name from payment_notification where trx_id like '%{npm}%' group by trx_id desc limit 1".format(npm=studentid)
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
    return row