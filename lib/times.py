# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 06:00:51 2020

@author: rolly
"""
import datetime
import locale
import config


locale.setlocale(locale.LC_TIME, config.locale)


def getCurrentDay():
    now=datetime.datetime.now()
    a=now.strftime('%A')
    return str(a.lower())