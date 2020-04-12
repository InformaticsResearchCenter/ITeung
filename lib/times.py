# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 06:00:51 2020

@author: rolly
"""
import datetime
import locale


locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')


def getCurrentDay():
    now=datetime.datetime.now()
    a=now.strftime('%A')
    return a.lower()