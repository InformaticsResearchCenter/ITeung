# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:27:37 2020

@author: rolly
"""
#from lib import wa,reply
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/wa", methods=['GET', 'POST'])
def sms_reply():
    msg = request.values.get('Body', None)
    num = request.values.get('From', None)
    resp = MessagingResponse()
    resp.message(msg+num)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
