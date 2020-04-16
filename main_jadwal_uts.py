from selenium.webdriver import ChromeOptions, Chrome
from module import siap_jadwal

import sys
import config

opts = ChromeOptions()
opts.add_argument("--headless")
opts.add_experimental_option("detach", True)
driver = Chrome(options=opts)

# prodis = ['D4 Teknik Informatika',
#           'D4 Manajemen Perusahaan',
#           'D3 Logistik Bisnis',
#           'D4 Logistik Bisnis']

# filters = {'tahun': config.siap_tahun_id,
#            'jenis': config.jenis_ujian,
#            'program': config.jalur_program}

# dosens = []
kodedosen=str(sys.argv[1])
# dosens.append(kodedosen)

param = {
    'dosen': kodedosen,
    'tahun': config.siap_tahun_id,
    'jenis': config.jenis_ujian,
    'program': config.jalur_program
}
siap_jadwal.makeExcelAndSend(param)
# siap_jadwal.makeFileForDosen(driver, dosens, filters)
# siap_jadwal.sendFileUjianDosen(dosens, filters)
