from module import va_parent, kelas, surat_va
from datetime import datetime
import app, config

def getDataPayment(npm):
    db = va_parent.dbConnectVA()
    sql = f"select * from payment_notification where trx_id='INV-SPP-{npm}-1-0920'"
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
        prodiid = f'{npm[0]}{npm[3]}'
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
        key = f'{prodi_singkatan}{tingkat}{angkatan}'
        default_amount_payment = app.getDataDefault(key, ws)
        message = f'Hai haiiiii kamu sudah transfer pembayaran semester yaaaa dengan{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}*NPM: {npm}*{config.whatsapp_api_lineBreak}*Nama: {customer_name}*{config.whatsapp_api_lineBreak}*Virtual Account: {virtual_account}*{config.whatsapp_api_lineBreak}*Tanggal: {datetime_payment}*{config.whatsapp_api_lineBreak}*Jumlah Transfer: {app.floatToRupiah(payment_amount)}*{config.whatsapp_api_lineBreak}*Total Sudah Bayar: {app.floatToRupiah(cumulative_payment_amount)}*{config.whatsapp_api_lineBreak}*Total Harus Bayar: {app.floatToRupiah(trx_amount)}*'
        if int(trx_amount) > int(default_amount_payment):
            amount_tunggakan = int(trx_amount) - int(default_amount_payment)
            fifty_percent_default_payment = int(default_amount_payment) / 2
            minimum_payment = int(amount_tunggakan) + int(fifty_percent_default_payment)
        else:
            minimum_payment = int(trx_amount) / 2
        app.openfile().close()
        if float(cumulative_payment_amount) >= float(minimum_payment):
            if app.cekSudahAdaKHS(npm, tahunid, 'A'):
                app.updateBiayaKHS(npm, tahunid, trx_amount - cumulative_payment_amount)
                message += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}terima kasih yaaa sudah bayar semester, semangat kuliahnya kakaaaa......'
            else:
                message += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}Kamu *sudah bisa* isi KRS yaaa coba cek di *SIAP* yaaa...., #BOTNAME# ucapkan terima kasihhhh dan jangan salah saat isi KRS yaaa....'
                message = message.replace('#BOTNAME#', config.bot_name)
                app.insertnewKHS(npm, tahunid, prodiid, app.cekSesiSemester(tipesemester, npm), trx_amount - cumulative_payment_amount)
        else:
            message += f'{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}Yahhhh kamu *belum bisa* isi KRS nihhhh coba *buat surat* lalu *ajukan ke pihak BAUK* agar kamu bisa isi KRS..... Suratnya udah {config.bot_name} kirim ke *{kelas.getStudentEmail(npm)}*'
            surat_va.makePdfAndSendToEmail(npm)
        msgreply=message
    else:
        msgreply='kamu belum ada transfer'
    return msgreply