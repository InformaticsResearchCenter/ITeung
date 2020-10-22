import pymysql, config, os, app

from lib import wa
from lib import reply

from module import kelas
from module import cek_pembayaran_va_mahasiswa

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
        trx_id_mahasiswa=cek_pembayaran_va_mahasiswa.getTrxIDList(i[0])
        if trx_id_mahasiswa:
            for j in trx_id_mahasiswa:
                vadata=cek_pembayaran_va_mahasiswa.getDataPembayaran(j[0])
                virtualaccount = vadata['virtual_account']
                jumlahygharusdibayar = app.floatToRupiah(float(vadata['trx_amount']))
                jumlahterakhirbayar = app.floatToRupiah(float(vadata['payment_amount']))
                jumlahygsudahdibayar = app.floatToRupiah(float(vadata['cumulative_payment_amount']))
                waktuterakhirbayar = vadata['datetime_payment'].strftime('%d-%m-%Y %H:%M:%S')
                customername=vadata['customer_name']
                msgreply+=f"Nama: *{customername}*\nNomor virtual account: *{virtualaccount}*\nTotal yang harus dibayar: *{jumlahygharusdibayar}*\nTotal yang sudah dibayar: *{jumlahygsudahdibayar}*\n\nJumlah terakhir pembayaran: *{jumlahterakhirbayar}*\nWaktu terakhir pembayaran: {waktuterakhirbayar}\n\n"
            else:
                msgreply+='Data Tidak ditemukan\n\n'
    return msgreply

def dbConnectVA():
    db=pymysql.connect(config.db_host_va, config.db_username_va, config.db_password_va, config.db_name_va)
    return db

def getVaData(studentid):
    db=dbConnectVA()
    sql=f"select * from upload where trx_id like '%{studentid}%' and expired_date > CURRENT_DATE"
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchall()
    return row