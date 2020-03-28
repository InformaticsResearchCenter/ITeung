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
from numba import jit
from time import sleep

@jit(nopython=True)
def setProfile(profile_folder):
    options = webdriver.ChromeOptions()
    set_dir = '--user-data-dir='+profile_folder
    options.add_argument(set_dir)
    driver = webdriver.Chrome(chrome_options=options)
    return driver

@jit(nopython=True)
def loginWA(driver):
    driver.get("https://web.whatsapp.com/")
    waitLogin(driver)

@jit(nopython=True)
def waitLogin(driver):
    target = '"_3ZW2E"'
    x_arg = '//div[contains(@class, ' + target + ')]'
    wait = WebDriverWait(driver, 600)
    wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))

@jit(nopython=True)
def typeAndSendMessage(driver, message):
    messages = message.split("\n")
    for msg in messages:
        typeMessage(driver, msg)
        lineBreakWhatsapp(driver)
    return sendMessage(driver)

@jit(nopython=True)
def typeMessage(driver, message):
    return driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0].send_keys(message)

@jit(nopython=True)
def sendMessage(driver):
    return driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0].click()

@jit(nopython=True)
def lineBreakWhatsapp(driver):
    return ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()

@jit(nopython=True)
def openMessage(driver):
    try:
        chat = driver.find_elements_by_class_name("OUeyt")[0]
        chat.click()
        chat.click()
        chat.click()
    except:
        print('no notification')
    sleep(0.5)

@jit(nopython=True)
def messageunread(driver):
    try:
        return int(driver.find_elements_by_class_name("OUeyt")[0].text)
    except:
        return 1

@jit(nopython=True)
def getData(driver, message_wa_index, default_alias_number_index):
    data = []
    data.append(getSenderNumber(driver, default_alias_number_index))
    data.append(getGroupName(driver))
    data.append(getSenderAlias(driver, default_alias_number_index))
    data.append(getMessage(driver, message_wa_index))
    data.append(isGroup(driver, default_alias_number_index))
    return data

@jit(nopython=True)
def isGroup(driver, default_alias_number_index):
    if getSenderAlias(driver, default_alias_number_index) == '':
        group='false'
    else:
        group='true'
    return group

@jit(nopython=True)
def getSenderAlias(driver, default_alias_number_index):
    try:
        senderAlias = driver.find_elements_by_class_name("_3Ye_R")[default_alias_number_index].text
    except:
        senderAlias = ''
    return senderAlias

@jit(nopython=True)
def getGroupName(driver):
    try:
        groupname=driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span').text
    except:
        groupname=''
    return groupname

@jit(nopython=True)
def getSenderNumber(driver, default_alias_number_index):
    try:
        senderNumber = driver.find_elements_by_class_name("RZ7GO")[default_alias_number_index].text
    except:
        try:
            senderNumber = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[1]/div/span").text
        except:
            senderNumber = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/header/div[2]/div/div/span").text
    return senderNumber

@jit(nopython=True)
def getMessage(driver, message_wa_index):
    try:
        message = driver.find_elements_by_xpath("(.//span)")[message_wa_index].text
    except:
        message=''
    return message