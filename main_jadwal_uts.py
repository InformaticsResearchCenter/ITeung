from selenium.webdriver import ChromeOptions, Chrome
from module import siap_jadwal

import sys

opts = ChromeOptions()
opts.add_argument("--headless")
opts.add_experimental_option("detach", True)
driver = Chrome(options=opts)

prodis = ['D4 Teknik Informatika',
          'D4 Manajemen Perusahaan',
          'D3 Logistik Bisnis',
          'D4 Logistik Bisnis']

filters = {'tahun': '20192',
           'jenis': '1',
           'program': 'REG'}

dosens = []
kodedosen=str(sys.argv[1])
dosens.append(kodedosen)

siap_jadwal.makeFileForDosen(driver, dosens, filters)
siap_jadwal.sendFileUjianDosen(dosens, filters)