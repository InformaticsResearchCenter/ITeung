from module import va_parent, kelas, surat_va
from datetime import datetime
import app, config

def getDataPayment(npm):
    db = va_parent.dbConnectVA()
    data_upload=getTrxIdFromUpload(npm)
    trx_id=data_upload['trx_id']
    sql = f"select * from payment_notification where trx_id = '{trx_id}'"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, data))
        else:
            result=None
        return result

def getProdiIDfromNPM(npm):
    db=kelas.dbConnectSiap()
    sql=f'SELECT ProdiID FROM `simak_mst_mahasiswa` where Login={npm}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]

def getTrxIdFromUpload(npm):
    db = va_parent.dbConnectVA()
    sql = f"select * from upload where trx_id like '%INV-%' and trx_id like '%-SPP-%' and trx_id like '%-{npm}-%' and expired_date > CURRENT_DATE"
    with db:
        cur = db.cursor()
        cur.execute(sql)
        data=cur.fetchone()
        if data != None:
            fields = map(lambda x: x[0], cur.description)
            result = dict(zip(fields, data))
        else:
            result=None
        return result

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]):
        return True
    else:
        return False

def replymsg(driver, data):
    npm, nama=kelas.getNpmandNameMahasiswa(data[0])
    datava=getDataPayment(npm)
    if datava:
        datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
        yearnow = datetime.date(datetime.now()).strftime('%Y')
        trxid = datava['trx_id']
        npm = app.cekNpmInTrxID(trxid)
        tipesemester = app.cekTipeSemester(trxid)
        tahunid = f'{yearnow}{tipesemester}'
        prodiid = getProdiIDfromNPM(npm)
        if prodiid == '64':
            prodiid='54'
        virtual_account = datava['virtual_account']
        customer_name =datava['customer_name']
        trx_amount = datava['trx_amount']
        payment_amount = datava['payment_amount']
        cumulative_payment_amount = datava['cumulative_payment_amount']
        payment_ntb = datava['payment_ntb']
        datetime_payment = datava['datetime_payment']
        datetime_payment_iso8601 = datava['datetime_payment_iso8601']
        ws = app.openfile().active
        prodi_singkatan = app.getProdiSingkatanFromProdiID(kelas.getProdiIDwithStudentID(npm)).lower()
        tingkat = f"tk{int(datetime.now().strftime('%Y')) - int(kelas.getTahunAngkatanWithStudentID(npm)) + 1}"
        angkatan = kelas.getTahunAngkatanWithStudentID(npm)
        message = f'Hai haiiiii kamu sudah transfer pembayaran semester yaaaa dengan\n\n*NPM: {npm}*\n*Nama: {customer_name}*\n*Virtual Account: {virtual_account}*\n*Tanggal: {datetime_payment}*\n*Jumlah Transfer: {app.floatToRupiah(payment_amount)}*\n*Total Sudah Bayar: {app.floatToRupiah(cumulative_payment_amount)}*\n*Total Harus Bayar: {app.floatToRupiah(trx_amount)}*\n*Sisa Yang Harus Dibayar: {app.floatToRupiah(float(int(trx_amount)-int(cumulative_payment_amount)))}*'
        if str(angkatan) == '2020':
            app.updateBiayaKHS(npm, tahunid, trx_amount - cumulative_payment_amount)
            message += f'\n\nterima kasih yaaa sudah bayar semester, semangat kuliahnya kakaaaa......'
            return message
            # return f'Mohon maaf untuk angkatan {angkatan}, sementara waktu verifikasi keuangan *BELUM* dapat dilakukan silahkan *VERIFIKASI KEMBALI SETELAH* tanggal *4 Desember 2020*.'
        key = f'{prodi_singkatan}{tingkat}{angkatan}'
        default_amount_payment = app.getDataDefault(key, ws)
        if default_amount_payment:
            default_amount_payment=int(default_amount_payment)
        else:
            if prodi_singkatan[:2] == 'd4':
                default_amount_payment = 2500000
            elif prodi_singkatan[:2] == 'd3':
                default_amount_payment = 2000000
            else:
                default_amount_payment = int(default_amount_payment)
        message = f'Hai haiiiii kamu sudah transfer pembayaran semester yaaaa dengan\n\n*NPM: {npm}*\n*Nama: {customer_name}*\n*Virtual Account: {virtual_account}*\n*Tanggal: {datetime_payment}*\n*Jumlah Transfer: {app.floatToRupiah(payment_amount)}*\n*Total Sudah Bayar: {app.floatToRupiah(cumulative_payment_amount)}*\n*Total Harus Bayar: {app.floatToRupiah(trx_amount)}*\n*Sisa Yang Harus Dibayar: {app.floatToRupiah(float(int(trx_amount)-int(cumulative_payment_amount)))}*'
        if int(trx_amount) > int(default_amount_payment):
            amount_tunggakan = int(trx_amount) - int(default_amount_payment)
            fifty_percent_default_payment = int(default_amount_payment) / 2
            minimum_payment = int(amount_tunggakan) + int(fifty_percent_default_payment)
            transfer_spp = int(cumulative_payment_amount) - int(amount_tunggakan)
            percentage = int(float(int(transfer_spp) / int(default_amount_payment)) * 100)
        else:
            potongan = int(default_amount_payment) - int(trx_amount)
            minimum_payment = int(default_amount_payment) / 2
            cumulative_payment_amount += potongan
            transfer_spp = int(cumulative_payment_amount)
            percentage = int(float(int(transfer_spp) / int(default_amount_payment)) * 100)
        if percentage >= 75 and percentage <= 100:
            if percentage == 100:
                percentage = 100
            else:
                percentage = 75
        else:
            percentage = 0
        app.openfile().close()
        if float(cumulative_payment_amount) >= float(minimum_payment):
            if app.cekSudahAdaKHS(npm, tahunid, 'A'):
                app.updateBiayaKHS(npm, tahunid, trx_amount - cumulative_payment_amount, percentage)
                message += f'\n\nterima kasih yaaa sudah bayar semester, semangat kuliahnya kakaaaa......'
            else:
                message += f'\n\nKamu *sudah bisa* isi KRS yaaa coba cek di *SIAP* yaaa...., #BOTNAME# ucapkan terima kasihhhh dan jangan salah saat isi KRS yaaa....'
                message = message.replace('#BOTNAME#', config.bot_name)
                app.insertnewKHS(npm, tahunid, prodiid, app.cekSesiSemester(tipesemester, npm), trx_amount - cumulative_payment_amount, percentage)
        else:
            message += f'\n\nYahhhh kamu *belum bisa* isi KRS nihhhh coba *buat surat* lalu *ajukan ke pihak BAUK* agar kamu bisa isi KRS..... Suratnya udah {config.bot_name} kirim ke *{kelas.getStudentEmail(npm)}*'
            surat_va.makePdfAndSendToEmail(npm)
        msgreply=message
    else:
        msgreply='kamu belum ada transfer'
    return msgreply