# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:27:37 2020

@author: rolly
"""

from lib import iteung
from flask import Flask, request, render_template, make_response, jsonify, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from templates import index

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
    jadwalid=name.split('-')[0]
    kelas=name.split('-')[1]
    namakelas=name.split('-')[2]
    if len(kelas) != 1:
        return 'Bad URL: {kelas}'.format(kelas=kelas)
    else:
        return index.html_presensi

@app.route('/data/proses/phonenumber/to/database', methods=['POST'])
def prosesdata():
    req = request.get_json()
    phonenumber = req['phonenumber']
    res = make_response(jsonify({'message': 'JSON data received'}), 200)
    return res

if __name__ == "__main__":
    app.run(debug=True)


# In[]
#msgreply=iteung.get('6281312000300','teung') 
