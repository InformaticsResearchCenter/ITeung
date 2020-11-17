from module import kelas
from module import va_parent

from datetime import datetime

import app

def auth(data):
    if kelas.isParent(data[0]):
        return True
    else:
        return False

def replymsg(driver, data):
    msgreply = ''
    npms = kelas.getStudentIdFromParentPhoneNumber(data[0])
    for npm in npms:
        npm = npm[0]
        nama = kelas.getStudentNameOnly(npm)
        for trx_id in getTrxIDList(npm):
            trx_id=trx_id[0]
            payment=getDataPembayaran(trx_id)
            kode_transaksi=trx_id
            judul_transaksi=trx_id.split('-')[1]
            virtual_account=payment['virtual_account']
            customer_name=payment['customer_name']
            trx_amount=payment['trx_amount']
            payment_amount=payment['payment_amount']
            cumulative_payment_amount=payment['cumulative_payment_amount']
            datetime_payment=payment['datetime_payment']
            percentage = ''
            if 'SPP' in trx_id:
                npm = app.cekNpmInTrxID(trx_id)
                ws = app.openfile().active
                prodi_singkatan = app.getProdiSingkatanFromProdiID(kelas.getProdiIDwithStudentID(npm)).lower()
                tingkat = f"tk{int(datetime.now().strftime('%Y')) - int(kelas.getTahunAngkatanWithStudentID(npm)) + 1}"
                angkatan = kelas.getTahunAngkatanWithStudentID(npm)
                key = f'{prodi_singkatan}{tingkat}{angkatan}'
                default_amount_payment = app.getDataDefault(key, ws)
                if int(trx_amount) > int(default_amount_payment):
                    amount_tunggakan = int(trx_amount) - int(default_amount_payment)
                    transfer_spp = int(cumulative_payment_amount) - int(amount_tunggakan)
                    percentage = float(int(transfer_spp) / int(default_amount_payment)) * 100
                else:
                    potongan = int(default_amount_payment) - int(trx_amount)
                    cumulative_payment_amount += potongan
                    transfer_spp = int(cumulative_payment_amount)
                    percentage = float(int(transfer_spp) / int(default_amount_payment)) * 100
                app.openfile().close()
            msgreply+=f'Jenis Pembayaran: *{judul_transaksi}*\n' \
                    f'Kode Transaksi: *{kode_transaksi}*\n' \
                    f'Virtual Account: *{virtual_account}*\n' \
                    f'Nama Pelanggan: *{customer_name}*\n' \
                    f'Jumlah Yang Harus Dibayar: *{app.floatToRupiah(float(trx_amount))}*\n' \
                    f'Jumlah Transfer: *{app.floatToRupiah(float(payment_amount))}*\n' \
                    f'Total Transfer: *{app.floatToRupiah(float(cumulative_payment_amount))}*\n' \
                    f'Tanggal dan Jam Transfer: *{datetime_payment}*\n' \
                    f'Persentase Pembayaran SPP: {round(percentage)}%\n\n'
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