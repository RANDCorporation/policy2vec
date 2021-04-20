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
parent_url = "https://www.gao.gov/reports-testimonies/month-in-review/"
options = webdriver.ChromeOptions()
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.extensions_to_open": ""}
#option.add_argument(“ -- incognito”)

## set-up the chrome driver
from os.path import dirname, abspath
chromedriver_path = dirname(dirname(abspath(__file__)))  + '/chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
#driver.get(parent_url)
keyboard = Controller()

## scan through fiscal years
hrefs = []
titles = []
years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
for year in years:

    ## go to the page for that year
    get_internet = driver.get('https://www.gao.gov/reports-testimonies/month-in-review/' + str(year))
    #print('navigating to: ' + get_internet.text)
    #get_internet.click()
    #time.sleep(1)

    ## loop through all the documents for that year
    ## i'm not sure how many there are, but I'm guessing less than 10k
    count = 0
    for i in range(1,3000):
        try:
            element1 = driver.find_element_by_xpath('//*[@id="overview"]/div['  + str(i) + ']/div/div/ul[1]/li[1]/a')
            element2 = driver.find_element_by_xpath('//*[@id="overview"]/div['  + str(i) + ']/div/div/ul[1]/li[2]/a')
            title_xpath = '//*[@id="overview"]/div[' + str(i) + ']/a/span'

            if 'Print Version' in element1.text:
                hrefs.append(element1.get_attribute('href'))
                print(hrefs[-1])
                count += 1
                titles.append(driver.find_element_by_xpath(title_xpath).text)
            elif 'Print Version' in element2.text:
                hrefs.append(element2.get_attribute('href'))
                print(hrefs[-1])
                count += 1
                titles.append(driver.find_element_by_xpath(title_xpath).text)
        except:
            pass
    print('fiscal year: %i, links:%i ' %(year, count))

## Save the links and document titles as a csv file
import pandas as pd
if not os.path.exists('logs'):
    os.makedirs('logs')
source_link = [parent_url]*len(hrefs)
source = ['GAO reports']*len(hrefs)
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
link_date = [date]*len(hrefs)
df = pd.DataFrame({'Title':titles, 'source':source, 'source link':source_link, 'link':hrefs, 'link date':link_date})
df.to_csv('logs/GAO.csv', index=False)

driver.quit()
