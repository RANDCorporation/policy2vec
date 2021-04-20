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
parent_url = "https://www.e-publishing.af.mil/Product-Index/"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('window-size=2560,1440')
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.extensions_to_open": ""}
#option.add_argument(“ -- incognito”)

## set-up the chrome driver
from os.path import dirname, abspath
chromedriver_path = dirname(dirname(abspath(__file__)))  + '/chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
driver.get(parent_url)
keyboard = Controller()

## Get the space-force level pubs
get_internet = driver.find_element_by_xpath('//*[@id="mvcContainer-449"]/div[2]/div[1]/div[1]/ul/li[3]/a')
get_internet.click()
time.sleep(5)

top_level_url = driver.current_url
print(top_level_url)

#driver.execute_script("document.body.style.zoom='zoom 50'")

## scan through the different Units
hrefs = []
titles = []

## navigate to the top-level page
driver.get(top_level_url)

## select the only sub-category on the next page
get_internet = driver.find_element_by_xpath('//*[@id="cat-20"]/div/ul/li/a')
try:
    get_internet.click()
    time.sleep(10)
except: ## I may need to scroll down to see the link
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    get_internet.click()
    time.sleep(10)

## select All-Pubs
try: #(I found some links with no publications at all)
    get_internet = driver.find_element_by_xpath('//*[@id="org-list"]/div[1]/ul/li[1]/a')
    get_internet.click()
    time.sleep(10)

    ## find out how many pages there are
    s = driver.find_element_by_xpath('//*[@id="data_info"]').text
    s = s[s.index('of'):]
    num_docs = int(re.sub("[^0-9]", "", s))
    num_pages = math.ceil(num_docs/10)

    ## scan through multiple pages (each of which shows 10 items)
    print('scanning through %i pages' %num_pages)
    count = 0
    for j in range(1,num_pages+1):

        ## click on the appropriate page number
        if j <= 4:
            k = j
        if j == 5:
            k = 5
        elif num_pages > 5 and 5 < j and j < num_pages-1:
            k = 4
        elif num_pages > 5 and j == num_pages-1:
            k = 5
        elif num_pages > 5 and j == num_pages:
            k = 6
        get_internet = driver.find_element_by_xpath('//*[@id="data_paginate"]/span/a[' + str(k) + ']')
        get_internet.click()
        time.sleep(10)

        ## scan through a single page
        for i in range(1,11):
            ## try/except since the last page will have less than 10 items
            try:
                element = driver.find_element_by_xpath('//*[@id="data"]/tbody/tr[' + str(i) + ']/td[1]/a')
                title_xpath = '//*[@id="data"]/tbody/tr[' + str(i) + ']/td[2]'
                titles.append(driver.find_element_by_xpath(title_xpath).text)
                hrefs.append(element.get_attribute('href'))
                count += 1
            except:
                pass
        print('page: %i, links:%i ' %(j, count))
except:
    pass

## Save the links and document titles as a csv file
if not os.path.exists('logs'):
    os.makedirs('logs')
import pandas as pd
source_link = [parent_url]*len(hrefs)
source = ['Air Force E-Publishing']*len(hrefs)
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
link_date = [date]*len(hrefs)
df = pd.DataFrame({'Title':titles, 'source':source, 'source link':source_link, 'link':hrefs, 'link date':link_date})
df.to_csv('logs/AF_epubs_space_force.csv', index=False)

## Save the links
#with open('links/AF_epubs_units.txt', 'w') as f:
#    for item in hrefs:
#        f.write("%s\n" % item)
## close the session
driver.quit()
