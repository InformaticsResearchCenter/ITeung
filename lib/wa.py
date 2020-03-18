# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 06:35:15 2020

@author: rolly
"""
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import config

def setProfile(profile_folder):
    options = webdriver.ChromeOptions()
    set_dir = '--user-data-dir='+profile_folder
    options.add_argument(set_dir)
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def loginWA(driver):
    driver.get("https://web.whatsapp.com/")
    waitLogin(driver)

def waitLogin(driver):
    target = '"_3RWII"'
    x_arg = '//div[contains(@class, ' + target + ')]'
    wait = WebDriverWait(driver, 600)
    wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))

def typeAndSendMessage(driver, message):
    message_target = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message_target.send_keys(message)
    sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
    sendbutton.click()

def deleteMessage(driver):
    driver.find_elements_by_class_name('_3j8Pd')[-1].click()
    sleep(1)

    value_name = driver.find_elements_by_class_name('_3zy-4')
    sleep(1)

    if 'Exit group' in value_name[4].text:
        print('group')
        value_name[3].click()
        driver.find_elements_by_class_name('_2eK7W')[1].click()
    else:
        print('personal')
        value_name[4].click()
        driver.find_elements_by_class_name('_2eK7W')[1].click()

def openMessage(driver):
    try:
        chat = driver.find_elements_by_class_name("P6z4j")[0]
        chat.click()
        chat.click()
        chat.click()
    except:
        print('no notification')
    sleep(0.5)

def getData(driver):
    data = []
    try:
        message = driver.find_elements_by_xpath("'.//span'")[-11].text
    except Exception as e:
        print(str(e))
        message = ''
    try:
        senderNumber = driver.find_elements_by_class_name("ZObjg")[-1].text
        senderAlias = driver.find_elements_by_class_name("_1F9Ap")[-1].text
        group = True
    except:
        # driver.find_element_by_class_name('_3fs0K').click()
        senderAlias=''
        try:
            senderNumber = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span").text
        except:
            senderNumber = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div/div/span")
        # senderNumber = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div/div/span').text
        # senderName = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[1]/div[2]/span/span').text
        # driver.find_element_by_class_name("qfKkX").click()
        group = False
    data.append(senderNumber)
    if group:
        data.append(senderAlias)
    data.append(message)
    return data
    
def getSenderName(driver):
    try:
        senderName = driver.find_elements_by_class_name("_1F9Ap")[-1].text
    except:
        driver.find_element_by_class_name('_3fs0K').click()
        sleep(1)
        senderName = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[1]/div[2]/span/span').text
    return senderName

def getSenderNumber(driver):
    try:
        senderNumber = driver.find_elements_by_class_name("ZObjg")[-1].text
    except:
        driver.find_element_by_class_name('_3fs0K').click()
        sleep(1)
        senderNumber = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[3]/span/div/span/div/div/div[1]/div[1]/span/span').text
    return senderNumber

def getMessage(driver):
    return driver.find_elements_by_xpath("(.//span)")[-11].text

 