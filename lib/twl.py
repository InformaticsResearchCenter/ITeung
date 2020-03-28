# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 08:55:39 2020

@author: rolly
"""
import config
from twilio.rest import Client
from numba import jit
#https://api.whatsapp.com/send?phone=14155238886&text=join%20actual-nor&source=&data=

@jit(nopython=True)
def sendMsg(num,msg):
    client = Client(config.account_sid, config.auth_token)
    message = client.messages.create(
            to="whatsapp:+"+num, 
            from_="whatsapp:+14155238886",
            body=msg)
    print(message.sid)
