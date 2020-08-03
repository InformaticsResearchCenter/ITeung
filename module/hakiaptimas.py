from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyunpack import Archive
from time import sleep
from lib import reply, wa
import config
import csv
import os
import shutil

def auth(data):
    groupid=reply.getNumberGroup(data[0]).split('-')
    if '3' in groupid:
        ret=True
    else:
        ret=False
    return ret

def replymsg(driver, data):
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wmsg = wmsg.replace('#BOTNAME#', config.bot_name)
    wa.typeAndSendMessage(driver, wmsg)
    try:
        filename=downloadFile(driver)
        moveFiles(filename)
        folder=makeDirectory()
        try:
            extractFiles(namafile=filename, folder=folder)
            try:
                gotoEhaki(driver)
                loginEhaki(driver)
                gotoResigterHaki(driver)
                closeBanner(driver)
                datacsv=dataFromCSV(folder=folder)
                detailForm(driver=driver, data=datacsv)
                dataPenciptaForm(driver=driver, data=datacsv)
                dataPemegangHakCipta(driver=driver)
                uploadFileHaki(driver=driver, folder=folder)
                setujuHaki(driver)
                billingcode, biaya=billingCodeHaki(driver)
                gotoAptimas(driver)
                loginAptimas(driver)
                gotoRegisterAptimas(driver)
                APTimas(driver=driver, data=datacsv, folder=folder)
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
                removeFileandDir(filename=filename, path='.\\' + folder)
                msgreply="Billing Code: "+str(billingcode)+'\nBiaya: '+str(biaya)
            except Exception as e:
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
                removeFileandDir(filename=filename, path='.\\' + folder)
                msgreply='Proses Pembuatan Haki Error Mohon diulangi, Error: _#ERROR#_'
                msgreply=msgreply.replace('#ERROR#', str(e))
        except:
            msgreply='filenya harus .rar atau zip'
            removeFileandDir(filename=filename, path='.\\'+folder)
    except:
        msgreply='ga ada filenya....'
    return msgreply

def makeDirectory():
    mkdir = True
    create = '1'
    while mkdir:
        try:
            os.mkdir(str(create))
            mkdir = False
        except:
            create = int(create) + 1
            mkdir = True
    return create

def moveFiles(namafile):
    move = True
    while move:
        try:
            source = 'C:\\Users\\'+config.computeruser+'\\Downloads\\' + str(namafile)
            destination = os.getcwd()
            shutil.move(source, destination)
            move = False
        except Exception as e:
            if 'already exists' in str(e):
                move = False
            else:
                move = True

def downloadFile(driver):
    filecheck = driver.find_elements_by_class_name('r9_f4')[-1]
    filename = driver.find_elements_by_class_name('h3p5g')[-1].text
    driver.find_elements_by_class_name('_1-9IA')[-1].click()
    return filename

def extractFiles(namafile, folder):
    Archive(namafile).extractall('.\\' + str(folder))

def removeFileandDir(filename, path):
    os.remove(filename)
    shutil.rmtree(path)

def gotoEhaki(driver):
    driver.execute_script("window.open('https://e-hakcipta.dgip.go.id/index.php/login');")
    driver.switch_to_window(driver.window_handles[1])

def gotoAptimas(driver):
    driver.get('https://aptimas.poltekpos.ac.id/login')

def loginEhaki(driver):
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/form[1]/div[2]/input').send_keys(config.usernamehaki)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/form[1]/div[3]/input').send_keys(config.passwordhaki)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[2]/form[1]/button').click()

def loginAptimas(driver):
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/input').send_keys(config.usernameaptimas)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[2]/div/input[1]').send_keys(config.passwordaptimas)
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[3]/div[2]/input').click()

def gotoResigterHaki(driver):
    driver.get('https://e-hakcipta.dgip.go.id/index.php/register/hakcipta')

def gotoRegisterAptimas(driver):
    driver.get('https://aptimas.poltekpos.ac.id/haki/create')

def closeBanner(driver):
    sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[2]/div/div/div[1]/button').click()

def dataFromCSV(folder):
    with open('{folder}/data.csv'.format(folder=folder)) as csvfile:
        csvreader=csv.reader(csvfile)
        newdata=[]
        for i in csvreader:
            newdata.append(i)
    newdata.pop(0)
    return newdata

def detailForm(driver, data):
    kotaterbit = data[0][-1]
    tanggalterbit = data[0][-2]
    desk = data[0][-3]
    judul = data[0][-4]
    ciptaan = data[0][-5]
    #jenis permohonan
    driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[1]/div/span/span[1]/span').click()
    sleep(.5)
    driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[2]').click()
    sleep(.5)
    #jenis ciptaan dan sub-jenis ciptaan
    if ciptaan.lower() == 'buku':
        driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[2]/div/span/span[1]/span').click()
        sleep(.5)
        driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[2]').click()
        sleep(.5)
        driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[3]/div/span/span[1]/span').click()
        sleep(.5)
        driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[5]').click()
        sleep(.5)
    else:
        driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[2]/div/span/span[1]/span').click()
        sleep(.5)
        driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[9]').click()
        sleep(.5)
        driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[3]/div/span/span[1]/span').click()
        sleep(.5)
        driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[5]').click()
        sleep(.5)
    #judul
    driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[4]/div/input').send_keys(judul)
    sleep(.5)
    #deskripsi
    driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[5]/div/textarea').send_keys(desk)
    sleep(.5)
    for i in range(3):
        #time
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[6]/div/div/input[1]').click()
    for i in range(12):
        #delete time
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[6]/div/div/input[1]').send_keys(Keys.BACKSPACE)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[6]/div/div/input[1]').send_keys(tanggalterbit + Keys.ENTER)
    #kota terbit
    kota=kotaterbit.split(' ')
    newkota=[]
    for i in kota:
        newkota.append(i.capitalize())
    separator = ' '
    fixkota=separator.join(newkota)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[1]/div[2]/div/div[8]/div/input').send_keys(fixkota)

def normalizeprovinsi(text):
    text=text.lower()
    text=text.replace(' ', '')
    text=text.strip()
    return text

def dataPenciptaForm(driver, data):
    nama=0
    alamat=1
    kota=2
    kodepos=3
    provinsi=4
    for i in data:
        driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[3]/div[1]/div[2]/a').click()
        sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[1]/div/input').send_keys(i[nama])
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[3]/div/textarea').send_keys(i[alamat])
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[4]/div/input').send_keys(i[kota])
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[6]/div/input').send_keys(i[kodepos])
        provinsilist=driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[8]/div/select/option')
        for provinsidata in provinsilist:
            if normalizeprovinsi(i[provinsi]) == normalizeprovinsi(provinsidata.text):
                provinsidata.click()
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[9]/input').click()

def dataPemegangHakCipta(driver):
    driver.execute_script("window.scrollTo(0, 1000)")
    driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[4]/div[1]/div[2]/a').click()
    sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[1]/div/input').send_keys('Politeknik Pos Indonesia')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[3]/div/textarea').send_keys('Jl. Sariasih No. 54')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[4]/div/input').send_keys('Bandung')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[6]/div/input').send_keys('40151')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[8]/div/select/option[11]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[9]/div/input').send_keys('lppm@poltekpos.ac.id')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[10]/div/input').send_keys('(022) 2009562')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[4]/div/div/div[2]/div/div/form/div[11]/input').click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def getFilePath(filename, folder):
    devpath = os.getcwd()
    path='.\\{folder}'.format(folder=folder)
    for root, dirs, files in os.walk(path):
        for i in files:
            if filename == i:
                rootpath=os.path.join(root, i)
                resultpath=os.path.join(devpath, rootpath)
    return resultpath

def uploadFileHaki(driver, folder):
    driver.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[5]/div[2]/div/div[2]/div/div/singleupload/span[1]/input[1]').send_keys(
        getFilePath(folder=folder, filename='umkm.pdf'))
    sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[5]/div[2]/div/div[3]/div/div/singleupload/span[1]/input[1]').send_keys(
        getFilePath(folder=folder, filename='akta.pdf'))
    sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[5]/div[2]/div/div[4]/div/div/singleupload/span[1]/input[1]').send_keys(
        getFilePath(folder=folder, filename='ktp.pdf'))
    sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[5]/div[2]/div/div[5]/div/div/singleupload/span[1]/input[1]').send_keys(
        getFilePath(folder=folder, filename='npwp.pdf'))
    sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[5]/div[2]/div/div[6]/div/div/singleupload/span[1]/input[1]').send_keys(
        getFilePath(folder=folder, filename='pernyataan.pdf'))
    sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[5]/div[2]/div/div[7]/div/div/multipleupload/span[1]/input[1]').send_keys(
        getFilePath(folder=folder, filename='ciptaan.pdf'))
    sleep(1)
    driver.find_element_by_xpath(
        '/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[5]/div[2]/div/div[8]/div/div/singleupload/span[1]/input[1]').send_keys(
        getFilePath(folder=folder, filename='pengalihan.pdf'))
    sleep(1)
    driver.find_element_by_xpath('/html/body/div/div[3]/div/div/div[2]/div/main/div/div[1]/div/div/div[2]/form/div[6]/div[1]/input').click()

def uploadFileAptimas(driver, folder):
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[6]/div[2]/div/input').send_keys(
        getFilePath(folder=folder, filename='ktp.pdf'))
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[7]/div[1]/div/input').send_keys(
        getFilePath(folder=folder, filename='pernyataan.pdf'))
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[6]/div[1]/div/input').send_keys(
        getFilePath(folder=folder, filename='ciptaan.pdf'))
    driver.find_element_by_xpath(
        '/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[7]/div[2]/div/input').send_keys(
        getFilePath(folder=folder, filename='pengalihan.pdf'))

def setujuHaki(driver):
    sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[5]/div/div/div[2]/div/form/div[2]/div/div/label/span[3]').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[2]/div/main/div/div[5]/div/div/div[2]/div/form/div[3]/button').click()

def billingCodeHaki(driver):
    targetbillingcode='/html/body/div/div[3]/div/div/div[2]/div/main/div[1]/div/div/div/div[2]/form/div/div/div[1]/div/div[2]/div/div[14]/div/div/span'
    targetbiaya='/html/body/div/div[3]/div/div/div[2]/div/main/div[1]/div/div/div/div[2]/form/div/div/div[1]/div/div[2]/div/div[11]/div/div/span'
    wait = WebDriverWait(driver, 600)
    wait.until(EC.presence_of_element_located((By.XPATH, targetbillingcode)))
    return driver.find_element_by_xpath(targetbillingcode).text, driver.find_element_by_xpath(targetbiaya).text

def APTimas(driver, data, folder):
    kotaterbit = data[0][-1]
    tanggalterbit = data[0][-2]
    desk = data[0][-3]
    judul = data[0][-4]
    ciptaan = data[0][-5]
    driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[1]/span/span[1]/span/span[1]').click()
    if ciptaan.lower() == 'buku':
        driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[18]').click()
    else:
        driver.find_element_by_xpath('/html/body/span/span/span[2]/ul/li[17]').click()
    driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[2]/input').send_keys(judul)
    driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[3]/textarea').send_keys(desk)
    driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[4]/div[1]/div/input').send_keys(tanggalterbit + Keys.ENTER)
    driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[4]/div[2]/div/input').send_keys('Indonesia')
    driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[4]/div[3]/div/input').send_keys(kotaterbit)
    uploadFileAptimas(driver, folder)
    driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/div[8]/div/div[2]/div/input').send_keys(str(data[0][1])+' '+str(data[0][3])+' '+str(data[0][2])+' '+str(data[0][4]))
    driver.find_element_by_xpath('/html/body/div[2]/div/section[2]/div/div[1]/div/div[2]/form/button').click()