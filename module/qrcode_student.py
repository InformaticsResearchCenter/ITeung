from lib import wa, reply
from module import kelas
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import os, qrcode

def auth(data):
    if kelas.getNpmandNameMahasiswa(data[0]) == None:
        ret = False
    else:
        ret = True
    return ret

def replymsg(driver, data):
    num = data[0]
    wmsg = reply.getWaitingMessage(os.path.basename(__file__).split('.')[0])
    wa.typeAndSendMessage(driver, wmsg)
    makeQrcode(num)
    uploadFile(driver)
    removeFile()

def uploadFile(driver):
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    sleep(1)
    driver.find_element_by_css_selector("input[type='file']").send_keys('./qrcode.PNG')
    waitUpload(driver)
    driver.find_element_by_css_selector("span[data-icon='send-light").click()
    removeFile()

def waitUpload(driver):
    x_arg = "span[data-icon='send-light"
    wait = WebDriverWait(driver, 600)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, x_arg)))

def removeFile():
    os.remove('./qrcode.PNG')

def makeQrcode(num):
    img = qrcode.make(data=num)
    img.save('./qrcode.PNG')