# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:27:37 2020

@author: rolly
"""

from lib import iteung
from flask import Flask, request, render_template, make_response, jsonify, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from lib import log
from module import kelas
from Crypto.Cipher import AES
from datetime import datetime

from flask_restful import Resource, Api, abort

import config, pymysql

app = Flask(__name__, static_url_path='')
apirest=Api(app=app)

def dbConnectPMB():
    db=pymysql.connect(config.db_host_pmb, config.db_username_pmb, config.db_password_pmb, config.db_name_pmb)
    return db

@app.route("/")
def home():
    return 'hello crot...'

@app.route("/wa", methods=['GET', 'POST'])
def sms_reply():
    msg = request.values.get('Body', None)
    wanum = request.values.get('From', None)
    num=wanum.split('+')[1]
    msgreply=iteung.get(num,msg)
    resp = MessagingResponse()
    resp.message(msgreply)
    return str(resp)

@app.route('/<name>')
def senddatajavascript(name):
    return render_template('index.html', groupname=name)

@app.route('/data/proses', methods=['POST'])
def prosesdata():
    req = request.get_json()
    number=req['number']
    url=req['url']
    groupname = url.split('/')[-1].replace('%20', ' ')
    message = 'hadir'
    alias = kelas.getNpmandNameMahasiswa(number)[1]
    isgroup='true'
    tipe='luring'
    log.save(number, message, alias, groupname, isgroup, tipe)
    res = make_response(jsonify({'message': 'JSON data received'}), 200)
    return res

@app.route('/<token>/callback/api/va', methods=['POST'])
def callback_api_va(token):
    try:
        datenow = datetime.date(datetime.now()).strftime('%d-%m-%Y')
        req=request.json
        trxid=req['trx_id']
        npm=trxid.split('-')[2]
        virtual_account=req['virtual account']
        customer_name=req['customer_name']
        trx_amount=req['trx_amount']
        payment_amount=req['payment amount']
        cumulative_payment_amount=req['cumulative payment amount']
        payment_ntb=req['payment_ntb']
        datetime_payment=req['datetime payment']
        datetime_payment_iso8601=req['datetime payment iso8601']
        try:
            obj = AES.new(config.key.encode("utf8"), AES.MODE_CBC, config.iv.encode("utf8"))
            dec = bytes.fromhex(token)
            resultpasscode, status = obj.decrypt(dec).decode('utf-8'), True
        except:
            resultpasscode, status = '', False
        if status:
            passcodetrxid=resultpasscode.split(';')[0]
            passcodevirtualaccount=resultpasscode.split(';')[1]
            passcodedatetime=resultpasscode.split(';')[2]
            if passcodetrxid == trxid and passcodevirtualaccount == virtual_account and passcodedatetime == datenow:
                if float(cumulative_payment_amount) >= float(float(trx_amount)/2):
                    return make_response(jsonify(
                        {
                            "message": "success",
                            "status": "krs otomatis"
                        }
                    ), 200)
                else:
                    return make_response(jsonify(
                        {
                            "message": "success",
                            "status": "kirim whatsapp bikin surat"
                        }
                    ), 200)
            else:
                return make_response(jsonify({'message': 'bad token'}), 401)
        else:
            return make_response(jsonify({'message': 'bad token'}), 401)
    except Exception as e:
        return {
            "code": 404,
            "message": f"ERROR={e}"
        }

class PMDK(Resource):
    def get(self, token):
        if token == config.tokenpmb:
            db=dbConnectPMB()
            query='SELECT nama_lengkap, jenis_kelamin, nisn, ttl, telephone, ' \
                  'bbm_line, email, nama_ayah_kandung, hp_ayah_kandung, nama_ibu_kandung, ' \
                  'hp_ibu_kandung,informasi_kampus, guru_bk, hp_guru_bk, status_kelulusan, ' \
                  'daftar_ulang, date_daftar_ulang, nama_penyetor, nominal_yang_disetor, tanggal_penyetoran ' \
                  'from mahasiswa_baru where tahun = "2019/2020" and jalur = "pmdk"'
            with db:
                cur=db.cursor()
                cur.execute(query)
                data=cur.fetchall()
                if data:
                    columnname = [headers[0] for headers in cur.description]
                    json_data = []
                    for result in data:
                        json_data.append(dict(zip(columnname, result)))
                    data = {'data_pmdk': json_data}
                    response=jsonify(data)
                    response.status_code=200
                    return response
                else:
                    abort(404, message= "data kosong...")
        else:
            abort(401, message='bad token')

class Reguler(Resource):
    def get(self, token):
        if token == config.tokenpmb:
            db = dbConnectPMB()
            query = 'SELECT nama_lengkap, jenis_kelamin, nisn, ttl, telephone, bbm_line, ' \
                    'email, nama_ayah_kandung, hp_ayah_kandung, nama_ibu_kandung, hp_ibu_kandung,' \
                    'informasi_kampus, guru_bk, hp_guru_bk, status_kelulusan, daftar_ulang, ' \
                    'date_daftar_ulang, nama_penyetor, nominal_yang_disetor, tanggal_penyetoran ' \
                    'from mahasiswa_baru where tahun = "2019/2020" and jalur = "reguler"'
            with db:
                cur = db.cursor()
                cur.execute(query)
                data = cur.fetchall()
                if data:
                    columnname = [headers[0] for headers in cur.description]
                    json_data = []
                    for result in data:
                        json_data.append(dict(zip(columnname, result)))
                    data = {'data_reguler': json_data}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    abort(404, message="data kosong...")
        else:
            abort(401, message='bad token')

class Mandiri(Resource):
    def get(self, token):
        if token == config.tokenpmb:
            db = dbConnectPMB()
            query = 'SELECT nama_lengkap, jenis_kelamin, nisn, ttl, telephone, bbm_line, ' \
                    'email, nama_ayah_kandung, hp_ayah_kandung, nama_ibu_kandung, hp_ibu_kandung,' \
                    'informasi_kampus, guru_bk, hp_guru_bk, status_kelulusan, daftar_ulang, ' \
                    'date_daftar_ulang, nama_penyetor, nominal_yang_disetor, tanggal_penyetoran ' \
                    'from mahasiswa_baru where tahun = "2019/2020" and jalur = "mandiri"'
            with db:
                cur = db.cursor()
                cur.execute(query)
                data = cur.fetchall()
                if data:
                    columnname = [headers[0] for headers in cur.description]
                    json_data = []
                    for result in data:
                        json_data.append(dict(zip(columnname, result)))
                    data = {'data_mandiri': json_data}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    abort(404, message="data kosong...")
        else:
            abort(401, message='bad token')

class Undangan(Resource):
    def get(self, token):
        if token == config.tokenpmb:
            db = dbConnectPMB()
            query = 'SELECT nama_lengkap, jenis_kelamin, nisn, ttl, telephone, bbm_line, ' \
                    'email, nama_ayah_kandung, hp_ayah_kandung, nama_ibu_kandung, hp_ibu_kandung,' \
                    'informasi_kampus, guru_bk, hp_guru_bk, status_kelulusan, daftar_ulang, ' \
                    'date_daftar_ulang, nama_penyetor, nominal_yang_disetor, tanggal_penyetoran ' \
                    'from mahasiswa_baru where tahun = "2019/2020" and jalur = "undangan"'
            with db:
                cur = db.cursor()
                cur.execute(query)
                data = cur.fetchall()
                if data:
                    columnname = [headers[0] for headers in cur.description]
                    json_data = []
                    for result in data:
                        json_data.append(dict(zip(columnname, result)))
                    data = {'data_mandiri': json_data}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    abort(404, message="data kosong...")
        else:
            abort(401, message='bad token')

class Beasiswa(Resource):
    def get(self, token):
        if token == config.tokenpmb:
            db = dbConnectPMB()
            query = 'SELECT nama_lengkap, jenis_kelamin, nisn, ttl, telephone, bbm_line, ' \
                    'email, nama_ayah_kandung, hp_ayah_kandung, nama_ibu_kandung, hp_ibu_kandung,' \
                    'informasi_kampus, guru_bk, hp_guru_bk, status_kelulusan, daftar_ulang, ' \
                    'date_daftar_ulang, nama_penyetor, nominal_yang_disetor, tanggal_penyetoran ' \
                    'from mahasiswa_baru where tahun = "2019/2020" and jalur = "beasiswa"'
            with db:
                cur = db.cursor()
                cur.execute(query)
                data = cur.fetchall()
                if data:
                    columnname = [headers[0] for headers in cur.description]
                    json_data = []
                    for result in data:
                        json_data.append(dict(zip(columnname, result)))
                    data = {'data_beasiswa': json_data}
                    response = jsonify(data)
                    response.status_code = 200
                    return response
                else:
                    abort(404, message="data kosong...")
        else:
            abort(401, message='bad token')

apirest.add_resource(PMDK, '/<string:token>/api/android/pmdk')
apirest.add_resource(Reguler, '/<string:token>/api/android/reguler')
apirest.add_resource(Mandiri, '/<string:token>/api/android/mandiri')
apirest.add_resource(Undangan, '/<string:token>/api/android/undangan')
apirest.add_resource(Beasiswa, '/<string:token>/api/android/beasiswa')

if __name__ == "__main__":
    app.run(debug=True)