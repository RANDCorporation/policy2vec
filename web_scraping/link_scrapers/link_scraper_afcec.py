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
parent_url = "https://www.afcec.af.mil/News/"
options = webdriver.ChromeOptions()
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.extensions_to_open": ""}
#option.add_argument(“ -- incognito”)

## set-up the chrome driver
from os.path import dirname, abspath
chromedriver_path = dirname(dirname(abspath(__file__)))  + '/chromedriver'
print(chromedriver_path)
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(parent_url)
keyboard = Controller()

## find out how many pages there are
s = driver.find_element_by_xpath('//*[@id="dnn_ctr2414_Article_desktopmodules_articlecs_article_ascx_UpdatePanel1"]/section/div[1]/ul/li[12]/a/span').text
num_pages = int(s)
print('num_pages = %i' % num_pages)

## scan through each page
hrefs = []
titles = []
for pg in range(1, num_pages+1):

    ## navigate m-th page
    get_internet = driver.get('https://www.afcec.af.mil/News/?Page=' + str(pg))
    #print('navigating to: ' + get_internet.text)
    #get_internet.click()
    #time.sleep(1)

    ## scan through a single page
    count = 0
    for i in range(1,11):

        ## try/except since the last page will have less than 10 items
        try:
            element = driver.find_element_by_xpath('//*[@id="dnn_ctr2414_Article_desktopmodules_articlecs_article_ascx_UpdatePanel1"]/section/ul/li[' + str(i) + ']/div/div[2]/div/h2/a')

            title_xpath = '//*[@id="dnn_ctr2414_Article_desktopmodules_articlecs_article_ascx_UpdatePanel1"]/section/ul/li[' + str(i) + ']/div/div[2]/div/h2/a'
            titles.append(driver.find_element_by_xpath(title_xpath).text)
            hrefs.append(element.get_attribute('href'))
            count += 1
        except:
            pass
    print('page: %i, links:%i ' %(pg, count))

## Save the links and document titles as a csv file
import pandas as pd
if not os.path.exists('logs'):
    os.makedirs('logs')
source_link = [parent_url]*len(hrefs)
source = ['Air Force Civil Engineering Center']*len(hrefs)
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
link_date = [date]*len(hrefs)
df = pd.DataFrame({'Title':titles, 'source':source, 'source link':source_link, 'link':hrefs, 'link date':link_date})
df.to_csv('logs/AF_afcec.csv', index=False)

driver.quit()
