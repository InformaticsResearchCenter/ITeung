# from inputjadwal import inputJadwalUjian
from selenium.webdriver import ChromeOptions, Chrome
from emaildosen import *
from makefile import *

import sys

opts = ChromeOptions()
opts.add_argument("--headless")
opts.add_experimental_option("detach", True)
driver = Chrome(options=opts)

prodis = ['D4 Teknik Informatika',
          'D4 Manajemen Perusahaan',
          'D3 Logistik Bisnis',
          'D4 Logistik Bisnis']

filters = {'tahun': '20191',
           'jenis': '1',
           'program': 'REG'}

dosens = []
kodedosen=sys.argv[1]
dosens.append(kodedosen)

makeFileForDosen(driver, dosens, filters)
sendFileUjianDosen(dosens, filters)
