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
        '1': 'PLETON 1',
        '2': 'PLETON 2',
        '3': 'PLETON 3',
        '4': 'PLETON 4',
        '5': 'PLETON 5',
        '6': 'PLETON 6',
        '7': 'PLETON 7',
        '8': 'PLETON 8',
        '9': 'PLETON 9',
        '10': 'PLETON 10',
        '11': 'PLETON 11',
        '12': 'PLETON 12',
    }
    return switcher.get(kode_pleton, None)