# Network Analysis of Vaccination Strategies
# Copyright (C) 2020 by The RAND Corporation
# See LICENSE and README.md for information on usage and licensing

## Imports
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
import pandas as pd
#import tabula
import time
import os
import pynput
from pynput.keyboard import Key, Controller
import re
import math
import datetime

## Set-up
parent_url = "https://www.esd.whs.mil/Directives/issuances/dodm/"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('window-size=2560,1440')
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.extensions_to_open": ""}

## set-up the chrome driver
from os.path import dirname, abspath
chromedriver_path = dirname(dirname(abspath(__file__)))  + '/chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(parent_url)
keyboard = Controller()

## download all documents
hrefs = []
titles = []
for i in range(1, 1000+1):

    href = None
    title_xpath = '//*[@id="dnn_ctr6503_Default_List_grdData"]/tbody/tr[' + str(i) + ']/td[3]'

    ## first try
    try:
        xpath = '//*[@id="dnn_ctr6503_Default_List_grdData"]/tbody/tr[' + str(i) + ']/td[1]/a'
        element = driver.find_element_by_xpath(xpath)
        href = element.get_attribute('href')

    ## second try
    except:
        try:
            xpath = '//*[@id="dnn_ctr6503_Default_List_grdData"]/tbody/tr[' + str(i) + ']/td[1]/p/a'
            element = driver.find_element_by_xpath(xpath)
            href = element.get_attribute('href')

        ## couldn't grab it for some reason
        except:
            pass

    if href:
        hrefs.append(href)
        try:
            titles.append(driver.find_element_by_xpath(title_xpath).text)
        except:
            titles.append('N/A')

## Save the links and document titles as a csv file
import pandas as pd
if not os.path.exists('logs'):
    os.makedirs('logs')
source_link = [parent_url]*len(hrefs)
source = ['Executive Services Directorate']*len(hrefs)
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
link_date = [date]*len(hrefs)
df = pd.DataFrame({'Title':titles, 'source':source, 'source link':source_link, 'link':hrefs, 'link date':link_date})
df.to_csv('logs/DoD_manuals.csv', index=False)

### Save the links
#with open('links/DOD_issuances.txt', 'w') as f:
#    for item in hrefs:
#        f.write("%s\n" % item)
#
#with open('links/DOD_issuances_titles.txt', 'w') as f:
#    for item in titles:
#        f.write("%s\n" % item)
## close the session
driver.quit()
