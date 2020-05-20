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

app = Flask(__name__, static_url_path='')

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

if __name__ == "__main__":
    app.run(debug=True)