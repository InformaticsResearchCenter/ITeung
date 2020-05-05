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
import os, clipboard


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

#fix 32
def retryNowClick(driver):
    retry = True
    wait = WebDriverWait(driver, 600)
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'Pg7Si')))
    while retry:
        try:
            driver.find_element_by_class_name('PNlAR').click
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
    target = '"_3ZW2E"'
    x_arg = '//div[contains(@class, ' + target + ')]'
    wait = WebDriverWait(driver, 600)
    retryNowClick(driver)
    wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))

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

def openMessage(driver):
    try:
        newnotifelement = driver.find_elements_by_class_name("OUeyt")[0]
        action=ActionChains(driver)
        action.move_to_element_with_offset(to_element=newnotifelement, xoffset=-10, yoffset=0).click().perform()
    except:
        print('no notification')

def copyToClipboard(message):
    copyToClipboard(message)

def pasteMessage(driver):
    ActionChains(driver).key_down(Keys.CONTROL).send_keys("V").key_up(Keys.CONTROL).perform()

def messageunread(driver):
    try:
        return int(driver.find_elements_by_class_name("OUeyt")[0].text)
    except:
        return 1

def messageReply(driver, default_alias_number_index):
    classvalue=driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[4]/div/div[3]/div/div/div[3]/div')[-1].get_attribute('class')
    if '_1T1d2' in classvalue:
        default_alias_number_index-=1
    else:
        default_alias_number_index-=0

def getData(driver, message_wa_index, default_alias_number_index):
    data = []
    # default_alias_number_index=messageReply(driver, default_alias_number_index)
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
    
def getSenderAlias(driver, default_alias_number_index):
    try:
        senderAlias = driver.find_elements_by_class_name("_3Ye_R")[default_alias_number_index].text
    except:
        senderAlias = ''
    return senderAlias

def getGroupName(driver):
    try:
        groupname=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span').text
    except:
        groupname=''
    return groupname

def getSenderNumber(driver, default_alias_number_index):
    try:
        senderNumber = driver.find_elements_by_class_name("RZ7GO")[default_alias_number_index].text
    except:
        try:
            senderNumber = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span").text
        except:
            senderNumber = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div/div/span").text
    return senderNumber

def getMessage(driver, message_wa_index):
    try:
        message = driver.find_elements_by_xpath("(.//span)")[message_wa_index].text
    except:
        message=''
    return message