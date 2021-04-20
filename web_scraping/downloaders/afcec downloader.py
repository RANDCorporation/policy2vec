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
from pathlib import Path
#import pdfkit

## paths
text_path = '../documents/parsed_text/AF_afcec/AF_afcec'
if not os.path.exists(text_path):
    os.makedirs(text_path)
df = pd.read_csv('../link_scrapers/logs/AF_afcec.csv')

## Selenium options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('window-size=2560,1440')
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.extensions_to_open": ""}
prefs = {
    "download.default_directory": text_path,
    "plugins.always_open_pdf_externally": True,
    }
options.add_experimental_option("prefs",prefs)

## set-up the chrome driver
from os.path import dirname, abspath
chromedriver_path = dirname(dirname(abspath(__file__)))  + '/chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

## scan through each document
download_time = []
download_success = []
for i in range(len(df)):
    try:
        driver.get(df['link'].iloc[i])
        text = driver.find_element_by_xpath('//*[@id="dnn_ctr2425_ViewArticle_UpdatePanel1"]/div').text

        with open(text_path + "/" + df['Title'].iloc[i] +  '.txt', "w") as text_file:
            text_file.write(text)

        #driver.get(df['pdf_url'].iloc[i])
        download_time.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        download_success.append(True)
    except:
        download_time.append('N/A')
        download_success.append(False)

## save log file
source_link = ['https://www.federalregister.gov/presidential-documents/executive-orders']*len(df)
source = ['Federal Register']*len(df)
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
link_date = [date]*len(df)

filenames = list(df['Title'])
filenames = [f + '.pdf' for f in filenames]
filepaths = ['documents/parsed_text/AF_afcec/AF_afcec/' + f for f in filenames]

df2 = pd.DataFrame({'Title':df['Title'], 'source':df['source'], 'source link':df['source link'], 'link':df['link'], 'link date':df['link date'], 'downloaded on':download_time, 'download success':download_success, 'file name':filenames, 'file path':filepaths})
df2.to_csv('../link_scrapers/logs/AF_afcec_afterDL.csv', index=False)


## close the session
driver.quit()
