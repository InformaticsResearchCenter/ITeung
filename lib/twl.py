# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 08:55:39 2020

@author: rolly
"""
import config
from twilio.rest import Client

#https://api.whatsapp.com/send?phone=14155238886&text=join%20actual-nor&source=&data=


client = Client(config.account_sid, config.auth_token)

message = client.messages.create(
    to="whatsapp:+6281312000300", 
    from_="whatsapp:+14155238886",
    body="Hello from Python! crat cret crot nguikkk lalalalal ngok crot hahah")

print(message.sid)
