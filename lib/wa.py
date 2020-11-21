# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 06:35:15 2020

@author: rolly
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from module import kelas
import os, clipboard, config


def setProfile(profile_folder):
    options = webdriver.ChromeOptions()
    set_dir = '--user-data-dir='+profile_folder
    options.add_argument(set_dir)
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def loginWA(driver):
    driver.get("https://web.whatsapp.com/")
    waitLogin(driver)

def detectphoneNotConnected(driver):
    try:
        driver.find_element_by_class_name('U0cj3')
        ret=True
    except:
        ret=False
    return ret

def arrowToGoDown(driver):
    try:
        driver.find_element_by_class_name('_3_BId').click()
    except:
        pass

def readMore(driver):
    try:
        driver.find_element_by_class_name('_2kMJX').click()
    except:
        pass

def retryNowClick(driver):
    retry = True
    wait = WebDriverWait(driver, 600)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, '_2XERB')))
    while retry:
        try:
            driver.find_elements_by_class_name('_2xUEC')[1].click
        except:
            retry=False

def restartMemu(ret):
    if ret:
        os.system(r'C:\Users\LENOVO\Desktop\ITeung\stopmemu.bat')
        sleep(.5)
        os.system(r'C:\Users\LENOVO\Desktop\ITeung\startmemu.bat')
        sleep(10)
    return ret

def waitLogin(driver):
    wait = WebDriverWait(driver, 600)
    retryNowClick(driver)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "_2O84H")))

def typeAndSendMessage(driver, message):
    messages = message.split("\n")
    for msg in messages:
        typeMessage(driver, msg.strip())
        lineBreakWhatsapp(driver)
    return sendMessage(driver)

def typeMessage(driver, message):
    return driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0].send_keys(message)

def sendMessage(driver):
    return driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0].click()

def lineBreakWhatsapp(driver):
    return ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()

def clickChatBox(driver):
    driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0].click()

def openMessage(driver):
    arrowToGoDown(driver)
    try:
        newnotifelement = driver.find_elements_by_class_name("VOr2j")[0]
        newnotifelement.click()
        newnotifelement.click()
        newnotifelement.click()
    except:
        pass

def copyToClipboard(message):
    clipboard.copy(message)

def pasteMessage(driver):
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()

def getData(driver, message_wa_index, default_alias_number_index):
    data = []
    data.append(getSenderNumber(driver, default_alias_number_index))
    data.append(getGroupName(driver))
    data.append(getSenderAlias(driver, default_alias_number_index))
    data.append(getMessage(driver, message_wa_index))
    data.append(isGroup(driver, default_alias_number_index))
    return data

def isGroup(driver, default_alias_number_index):
    if getSenderAlias(driver, default_alias_number_index) == '':
        group='false'
    else:
        group='true'
    return group

def sendOutbox(driver):
    status, data = getOutbox()
    if status:
        try:
            pesan=data[-1].split(' ')
            pesanresult=''
            for i in pesan:
                i=i.replace('\\n', '%0A')
                pesanresult+=str(i)+'+'
            nomortujuan=data[1]
            sleep(10)
            driver.get('https://web.whatsapp.com/send?phone={nomortujuan}&text={pesan}'.format(
                nomortujuan=str(nomortujuan),
                pesan=str(pesanresult)
            ))
            sleep(10)
            waitLogin(driver)
            try:
                sleep(2)
                driver.find_element_by_class_name('_2fuxX')
                print(f'phone number invalid {nomortujuan}')
                deleteOutbox(id=data[0])
                driver.get("https://web.whatsapp.com/")
            except:
                try:
                    sendMessage(driver)
                    deleteOutbox(id=data[0])
                except:
                    driver.get("https://web.whatsapp.com/")
        except:
            driver.get("https://web.whatsapp.com/")
    else:
        print('no outbox')

def getOutbox():
    db=kelas.dbConnect()
    sql='select * from outbox'
    with db:
        cur=db.cursor()
        cur.execute(sql)
        row=cur.fetchone()
        if row is not None:
            return True, row
        else:
            return False, None

def setOutbox(nomortujuan, pesan):
    db=kelas.dbConnect()
    sql="INSERT INTO `wanda`.`outbox`(`id`, `nomor_tujuan`, `pesan`) VALUES (DEFAULT, '{nomortujuan}', '{pesan}')".format(
        nomortujuan=nomortujuan,
        pesan=pesan
    )
    with db:
        cur=db.cursor()
        cur.execute(sql)

def deleteOutbox(id):
    db=kelas.dbConnect()
    sql='DELETE from outbox where id={id}'.format(id=id)
    with db:
        cur=db.cursor()
        cur.execute(sql)
    
def getSenderAlias(driver, default_alias_number_index):
    try:
        senderAlias = driver.find_elements_by_class_name("_2KXjI")[default_alias_number_index].text
    except:
        senderAlias = ''
    return senderAlias

def needChatClick(driver, status=config.NEED_CHAT_CLICK):
    try:
        if status:
            driver.driver.find_elements_by_class_name('_2kHpK')[0].click()
    except:
        driver.get('https://web.whatsapp.com/send?phone=6285155494985&text=open+new+message')
        sleep(10)
        waitLogin(driver)
        sleep(5)
        sendMessage(driver)


def getGroupName(driver):
    try:
        groupname=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span').text
    except:
        groupname=''
    return groupname

def getSenderNumber(driver, default_alias_number_index):
    try:
        senderNumber = driver.find_elements_by_class_name("_1o4HO")[default_alias_number_index].text
    except:
        try:
            senderNumber = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span").text
        except:
            senderNumber = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div/div/span").text
    return senderNumber

def getMessage(driver, message_wa_index):
    readMore(driver)
    try:
        message = driver.find_elements_by_xpath("(.//span)")[message_wa_index].text
    except:
        message=''
    return message

def jsWriteAndSendFunction(driver, msg):
    js_function = '''
        setTimeout(function() {
            var input = document.querySelector('#main [contenteditable~=true]');
            input.innerHTML = "%s";
            input.dispatchEvent(new Event('input', {bubbles: true}));
            var button = document.querySelector('button>span[data-icon="send"]').parentElement;
            button.click();
        }, 0);
        ''' % msg
    driver.execute_script(js_function)