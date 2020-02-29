# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 06:35:15 2020

@author: rolly
"""

def setProfile():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=./user_data')
    driver = webdriver.Chrome(chrome_options=self.options)
        
def openWaWeb(self):
    setProfile()
    self.driver.get("https://web.whatsapp.com/")
    self.waitLogin()
    
def waitLogin(self):
    self.target = '"_3RWII"'
    self.x_arg = '//div[contains(@class, ' + self.target + ')]'
    self.wait = WebDriverWait(self.driver, 600)
    self.wait.until(EC.presence_of_element_located((By.XPATH, self.x_arg)))
    