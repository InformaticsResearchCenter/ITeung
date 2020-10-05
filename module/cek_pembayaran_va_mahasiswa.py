from module import kelas
from module import va_parent

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]):
        return True
    else:
        return False

def replymsg(driver, data):
    npm, nama = kelas.getNpmandNameMahasiswa(data[0])
    msgreply = ''
    for trx_id in getTrxIDList(npm):
        payment=getDataPembayaran(trx_id)
        kode_transaksi=trx_id
        judul_transaksi=trx_id.split('-')[1]
        virtual_account=payment['virtual_account']
        customer_name=payment['customer_name']
        trx_amount=payment['trx_amount']
        payment_amount=payment['payment_amount']
        cumulative_payment_amount=payment['cumulative_payment_amount']
        datetime_payment=payment['datetime_payment']
        msgreply+=f'Jenis Pembayaran: *{judul_transaksi}*\n' \
                  f'Kode Transaksi: *{kode_transaksi}*\n' \
                  f'Virtual Account: *{virtual_account}*\n' \
                  f'Nama Pelanggan: *{customer_name}*\n' \
                  f'Jumlah Yang Harus Dibayar: *{trx_amount}*\n' \
                  f'Jumlah Transfer: *{payment_amount}*\n' \
                  f'Total Transfer: *{cumulative_payment_amount}*\n' \
                  f'Tanggal dan Jam Transfer: *{datetime_payment}*\n\n'
    return msgreply

def getDataPembayaran(trx_id):
    db=va_parent.dbConnectVA()
    sql=f'select * from payment_notification where trx_id="{trx_id}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, row))
        else:
            result = None
        return result


def getTrxIDList(npm):
    db=va_parent.dbConnectVA()
    sql=f'SELECT trx_id FROM `upload` where trx_id LIKE "%-{npm}-%" and CURRENT_DATE < expired_date'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        if rows is not ():
            return rows
        else:
            return None