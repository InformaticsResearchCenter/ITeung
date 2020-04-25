from module import jadwal_puasa
import requests, datetime, os, config

def auth(data):
    ret=True
    return ret

def replymsg(driver, data):
    status, linkdata=jadwal_puasa.locateGmaps(driver)
    nowdatetime = datetime.datetime.now()
    if status:
        try:
            datalinksplit = linkdata.split('@')
            datalatitudelongitudesplit = datalinksplit[1].split(',')
            latitude, longitude = datalatitudelongitudesplit[0], datalatitudelongitudesplit[1]
        except:
            datalinksplit = linkdata.split('&')
            datalinksplitagain = datalinksplit[0].split('=')
            datalatitudelongitudesplit = datalinksplitagain[1].split('%2C')
            latitude, longitude = datalatitudelongitudesplit[0], datalatitudelongitudesplit[1]
        method = '5'
        api = 'http://api.aladhan.com/v1/calendar?latitude={lati}&longitude={long}&method={method}&month={months}&year={years}'.format(lati=latitude, long=longitude, method=method, months=nowdatetime.month, years=nowdatetime.year)
        req = requests.get(api)
        apidata = req.json()['data'][nowdatetime.day - 1]
        imsak = apidata['timings']['Imsak'].split(' ')[0]
        imsaktime = datetime.datetime.strptime(imsak, '%H:%M')
        now = datetime.datetime.now().strftime('%H:%M:%S')
        nowtime = datetime.datetime.strptime(now, '%H:%M:%S')
        result = str(imsaktime-nowtime).split(':')
        if nowtime > imsaktime:
            msgreply='yah udah kelewat waktu imsaknya....'
        else:
            if result[0] == '0' and result[1] != '00' and result[2] != '00':
                time='{menit} Menit {detik} Detik lagi kita buka yaa....'.format(menit=result[1], detik=result[2])
            elif result[0] == '0' and result[1] == '00' and result[2] != '00':
                time='{detik} Detik lagi kita buka yaa....'.format(detik=result[2])
            else:
                time='{jam} Jam {menit} Menit {detik} Detik lagi kita buka yaa....'.format(jam=result[0], menit=result[1], detik=result[2])
            msgreply='menurut dari peta yang kamu kirim ke #BOTNAME# maka, {time}'.format(time=time)
    else:
        method = '5'
        latitude, longitude = '-6.8737943', '107.5757477'
        api = 'http://api.aladhan.com/v1/calendar?latitude={lati}&longitude={long}&method={method}&month={months}&year={years}'.format(
            lati=latitude, long=longitude, method=method, months=nowdatetime.month, years=nowdatetime.year)
        req = requests.get(api)
        apidata = req.json()['data'][nowdatetime.day - 1]
        imsak = apidata['timings']['Imsak'].split(' ')[0]
        imsaktime = datetime.datetime.strptime(imsak, '%H:%M')
        now = datetime.datetime.now().strftime('%H:%M:%S')
        nowtime = datetime.datetime.strptime(now, '%H:%M:%S')
        result = str(imsaktime - nowtime).split(':')
        if nowtime > imsaktime:
            msgreply = 'yah udah kelewat waktu imsaknya....'
        else:
            if result[0] == '0' and result[1] != '00' and result[2] != '00':
                time = '{menit} Menit {detik} Detik lagi kita buka yaa....'.format(menit=result[1], detik=result[2])
            elif result[0] == '0' and result[1] == '00' and result[2] != '00':
                time = '{detik} Detik lagi kita buka yaa....'.format(detik=result[2])
            else:
                time = '{jam} Jam {menit} Menit {detik} Detik lagi kita buka yaa....'.format(jam=result[0], menit=result[1], detik=result[2])
            msgreply = 'karena kamu ga kirim peta kamu ke #BOTNAME# yaudah deh #BOTNAME# kasih perhitungan dari rumah #BOTNAME# aja yaa ..., {time}'.format(time=time)
    return msgreply
