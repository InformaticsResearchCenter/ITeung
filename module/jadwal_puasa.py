import requests, datetime, os, config
from lib import reply, wa

def auth(data):
    ret=True
    return ret

def replymsg(driver, data):
    status, linkdata=locateGmaps(driver=driver)
    if status:
        wmsg=reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
        wmsg=wmsg.replace('#BOTNAME#', config.bot_name)
        wa.typeAndSendMessage(driver, wmsg)
        try:
            datalinksplit=linkdata.split('@')
            datalatitudelongitudesplit = datalinksplit[1].split(',')
            latitude, longitude=datalatitudelongitudesplit[0], datalatitudelongitudesplit[1]
        except:
            datalinksplit = abc.split('&')
            datalinksplitagain = datalinksplit[0].split('=')
            datalatitudelongitudesplit = datalinksplitagain[1].split('%2C')
            latitude, longitude=datalatitudelongitudesplit[0], datalatitudelongitudesplit[1]
        now = datetime.datetime.now()
        method='5'
        api='http://api.aladhan.com/v1/calendar?latitude={lati}&longitude={long}&method={method}&month={months}&year={years}'.format(lati=latitude, long=longitude, method=method, months=now.month, years=now.year)
        req = requests.get(api)
        apidata = req.json()['data'][now.day - 1]
        fajr = apidata['timings']['Fajr']
        sunrise = apidata['timings']['Sunrise']
        dhuhr = apidata['timings']['Dhuhr']
        asr = apidata['timings']['Asr']
        sunset = apidata['timings']['Sunset']
        maghrib = apidata['timings']['Maghrib']
        isha = apidata['timings']['Isha']
        imsak = apidata['timings']['Imsak']
        midnight = apidata['timings']['Midnight']
        msgreply='Berdasarkan dari Lokasi yang kamu kirim berikut Jadwal Ibadah yang diminta...\n\n*JADWAL PUASA*\n\n*Tanggal*: _{now}_\n\nFajr: {fajr}\nSunrise: {sunrise}\nDhuhr: {dhuhr}\nAsr: {asr}\nSunset: {sunset}\nMaghrib: {maghrib}\nIsha: {isha}\nImsak: {imsak}\nMidnight: {midnight}\n\nSelamat menjalankan ibadah puasa bagi yang menjalankan yaaa Teman-Teman.... <3<3'.format(fajr=fajr, sunrise=sunrise, dhuhr=dhuhr, asr=asr, sunset=sunset, maghrib=maghrib, isha=isha, imsak=imsak, midnight=midnight, now=now.strftime('%d-%m-%Y'))
    else:
        msgreply='duh mana lokasinya, #BOTNAME# ga bisa nentuin kamu ada dimana.... nanti #BOTNAME# salah kasih informasi lagi...'
    return msgreply

def locateGmaps(driver):
    try:
        cekgmaps=driver.find_elements_by_class_name('_3hy7L')[-1].get_attribute('data-plain-text')
        ret=True
    except:
        ret=False
        cekgmaps=''
    return ret, cekgmaps

abc='https://maps.google.com/maps?q=-6.8758059%2C107.5785173&z=17&hl=en'
data0=abc.split('&')
data1=data0[0].split('=')
data2=data1[1].split('%2C')
print(data2)