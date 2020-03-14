# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 09:27:37 2020

@author: rolly
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/wa", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    body = request.values.get('Body', None)
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message(body)
    #resp.media("https://farm8.staticflickr.com/7090/6941316406_80b4d6d50e_z_d.jpg")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
