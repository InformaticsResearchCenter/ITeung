# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 07:21:02 2020

@author: rolly
"""

import sys
from importlib import import_module


modulename=str(sys.argv[1])
param=str(sys.argv[2])

mod=import_module('module.' + modulename)
mod.run(param)