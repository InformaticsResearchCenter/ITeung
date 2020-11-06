from module import kelas

from lib import sql_to_dictionary
from lib import message
from lib import numbers
from lib import wa

import config
import subprocess
import os

def auth(data):
    if numbers.normalize(data[0]) == '6289505191519':
        return True
    else:
        return False

def get_npm_distinct(npm_range_begin, npm_range_end, tahunid):
    db=kelas.dbConnectSiap()
    sql=f'SELECT DISTINCT(MhswID) FROM simak_trn_krs WHERE TahunID={tahunid} AND MhswID BETWEEN {npm_range_begin} AND {npm_range_end}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        return sql_to_dictionary.fetchAllMode(cur.fetchall(), cur)

def data_student_krs(mhsw_id, tahunid):
    db=kelas.dbConnectSiap()
    sql=f'SELECT * from simak_trn_krs WHERE MhswID={mhsw_id} and TahunID={tahunid}'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        return sql_to_dictionary.fetchAllMode(cur.fetchall(), cur)

def split_and_get_npm(message):
    try:
        message_list=message.split(' sampai ')
        return get_npm_from_list(message_list[0], message_list[1])
    except:
        return False

def get_npm_from_list(*argv):
    npm_begin=argv[0].split(' ')[-1]
    npm_end=argv[1].split(' ')[0]
    return npm_begin, npm_end

def tahun_id_check(tahunid):
    db=kelas.dbConnectSiap()
    sql=f'select * from simak_mst_tahun where TahunID="{tahunid}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        if cur.fetchone():
            return True
        else:
            return False

def insert_transkrip(data_krs_mahasiswa_dictionary):
    db=kelas.dbConnectSiap()
    sql=f"INSERT INTO `simpati`.`simak_trn_transkrip`" \
        f"(`KRSPRCID`, " \
        f"`KRSID`, " \
        f"`KHSID`, " \
        f"`MhswID`, " \
        f"`TahunID`, " \
        f"`MKID`, " \
        f"`MKKode`, " \
        f"`SKS`, " \
        f"`GradeNilai`, " \
        f"`BobotNilai`, " \
        f"`StatusKRSID`, " \
        f"`MKSetara`, " \
        f"`NA`) " \
        f"VALUES " \
        f'(DEFAULT, ' \
        f'{data_krs_mahasiswa_dictionary["KRSID"]}, ' \
        f'{data_krs_mahasiswa_dictionary["KHSID"]}, ' \
        f'"{data_krs_mahasiswa_dictionary["MhswID"]}", ' \
        f'"{data_krs_mahasiswa_dictionary["TahunID"]}", ' \
        f'{data_krs_mahasiswa_dictionary["MKID"]}, ' \
        f'"{data_krs_mahasiswa_dictionary["MKKode"]}", ' \
        f'{data_krs_mahasiswa_dictionary["SKS"]}, ' \
        f'"{data_krs_mahasiswa_dictionary["GradeNilai"]}", ' \
        f'{data_krs_mahasiswa_dictionary["BobotNilai"]}, ' \
        f'"{data_krs_mahasiswa_dictionary["StatusKRSID"]}", ' \
        f'"", ' \
        f'"N");'
    with db:
        cur=db.cursor()
        cur.execute(sql)

def data_check_krs_to_transkrip(data_krs_mahasiswa_dictionary):
    db=kelas.dbConnectSiap()
    sql=f'select * from simak_trn_transkrip ' \
        f'where ' \
        f'MhswID={data_krs_mahasiswa_dictionary["MhswID"]} ' \
        f'and ' \
        f'MKKode="{data_krs_mahasiswa_dictionary["MKKode"]}"'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        if cur.fetchone():
            return {
                'status': False,
                'mhswid': data_krs_mahasiswa_dictionary["MhswID"],
                'mkkode': data_krs_mahasiswa_dictionary["MKKode"]
            }
        insert_transkrip(data_krs_mahasiswa_dictionary)
        return {
            'status': True,
            'mhswid': data_krs_mahasiswa_dictionary["MhswID"],
            'mkkode': data_krs_mahasiswa_dictionary["MKKode"]
        }

def find_tahun_id_from_message(message):
    tahun_id=[word for word in message.split(' ') if tahun_id_check(word)]
    return tahun_id

def run(data):
    krs_to_transkrip(data)

def replymsg(driver, data):
    subprocess.Popen(["python", "run.py", os.path.basename(__file__).split('.')[0], data], cwd=config.cwd)
    return f'okee tungguin bentar yaa, nanti {config.bot_name} sampein hasilnya'

def krs_to_transkrip(data):
    try:
        tahun_id = find_tahun_id_from_message(message.normalize(data[3]))
        if tahun_id:
            tahun_id = tahun_id[0]
            data_npm_begin_and_npm_end=split_and_get_npm(message.normalize(data[3]))
            if data_npm_begin_and_npm_end:
                npm_begin, npm_end = data_npm_begin_and_npm_end
                data_mhsw_id_distinct = get_npm_distinct(
                    npm_range_begin=npm_begin,
                    npm_range_end=npm_end,
                    tahunid=tahun_id
                )

                data_check = [data_check_krs_to_transkrip(data_mahasiswa_krs) for mshw in data_mhsw_id_distinct for
                              data_mahasiswa_krs in data_student_krs(mshw["MhswID"], tahun_id)]

                msg_data_insert = f'Data perpindahan dari KRS to TRANSKRIP:{config.whatsapp_api_lineBreak}{config.whatsapp_api_lineBreak}'
                for data_check_loop in data_check:
                    if data_check_loop['status']:
                        msg_data_insert += f'{data_check_loop["mhswid"]} | {data_check_loop["mkkode"]}{config.whatsapp_api_lineBreak}'

                return wa.setOutbox(numbers.normalize(data[0]), msg_data_insert)
            return wa.setOutbox(numbers.normalize(data[0]), 'kata sampai tidak ada')
        return wa.setOutbox(numbers.normalize(data[0]), 'tidak ada tahun id')
    except Exception as e:
        return wa.setOutbox(numbers.normalize(data[0]), f'ERROR: {e}')