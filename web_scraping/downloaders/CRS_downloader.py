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
import os, shutil
import pynput
from pynput.keyboard import Key, Controller
import re
import math
import datetime
from pathlib import Path

## paths
pdf_path = '../documents/pdfs/CRS_Reports/CRS_Reports'
if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)
CRS_fname = '../SearchResults.csv'
df = pd.read_csv(CRS_fname)

## Selenium options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument('window-size=2560,1440')
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.extensions_to_open": ""}
prefs = {
    "download.default_directory": pdf_path,
    "plugins.always_open_pdf_externally": True,
    }
options.add_experimental_option("prefs",prefs)

## set-up the chrome driver
from os.path import dirname, abspath
chromedriver_path = dirname(dirname(abspath(__file__)))  + '/chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

## scan through each document
"""
Note: I am treating these CRS documents differently than the other documents because
   1) in this case the CRS website is nice enough to give me a giant .csv file containing the links to all the files
   2) but it appears that the site hosting these pdfs has some security measure in place that prevents my usual call to urllib.requests to fail with a 403 error message.
A similar scenario occured for the EO documents. My work-around is to use Selenium to open the link in a browser and to then save the pdf in the downloads folder.

One last note: I can't figure out how to control the download folder, so I'll have to move the downloaded documents manually into the correct folder.
"""

download_time = []
download_success = []
for i in range(len(df)):
    try:
        ## download
        driver.get(df['Url'].iloc[i])
        keyboard = Controller()
        #time.sleep(6)

        ## move to the correct folder
        #fname = df['ProductNumber'].iloc[i] + '.pdf'
        #shutil.move('/Users/hartnett/Downloads/' + fname, pdf_path + '/' + fname)
        #time.sleep(6)

        ## append to download list
        download_time.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        download_success.append(True)
    except:
        download_time.append('N/A')
        download_success.append(False)

## save log file
source_link = ['https://crsreports.congress.gov']*len(df)
source = ['CRS Reports']*len(df)
date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
link_date = [date]*len(df)

filenames = list(df['ProductNumber'])
filenames = [f + '.pdf' for f in filenames]
filepaths = [pdf_path + '/' + f for f in filenames]

df2 = pd.DataFrame({'Title':df['Title'], 'source':source, 'source link':source_link, 'link':df['Url'], 'link date':link_date, 'downloaded on':download_time, 'download success':download_success, 'file name':filenames, 'file path':filepaths})
df2.to_csv('../link_scrapers/logs/CRS_Reports.csv', index=False)


## close the session
driver.quit()
