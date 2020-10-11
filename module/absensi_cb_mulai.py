from lib import numbers

import config

def auth(data):
    if numbers.normalize(data[0]) in config.nomor_koor_pleton_cb:
        return True
    else:
        return False

def replymsg(driver, data):
    grp=data[1]
    kode_pleton=grp.split('-')[1]
    nama_pleton=pletonSwitcher(kode_pleton)
    if nama_pleton:
        msgreply=f'okeeeeee, absensi CB untuk *PLETON {nama_pleton}* dimulai, kepada peserta Character Building Politeknik Pos Indonesia 2020 untuk segera absen ke {config.bot_name} yaa, cukup dengan kirimkan pesannya ke GROUP PLETON kamu sudah bisa terabsen, minimal 2 - 3 pesan yaa...'
    else:
        msgreply=f'duhhh kakak koordinator, nama pletonnya ngga bisa {config.bot_name} temuin nih, coba cek yaa nama groupnyaa'
    return msgreply

def pletonSwitcher(kode_pleton):
    switcher = {
        '0': 'ITeung hore hore',
        '1': 'Bojong Menjeng',
        '2': 'Cangkuang',
        '3': 'Jiwa',
        '4': 'Batu Jaya',
        '5': 'Cibuaya',
        '6': 'Karangkamulyan',
        '7': 'Blandongan',
        '8': 'Tanggulun',
        '9': 'Serut',
        '10': 'Tridarma',
        '11': 'Batu Kalde',
        '12': 'Pasir Datar',
        '13': 'Huludayeuh',
        '14': 'Ulubelu',
        '15': 'Kawali',
        '16': 'Sanghyang',
        '17': 'Batu Tulis'
    }
    return switcher.get(kode_pleton, None)