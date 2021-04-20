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

## paths
pdf_path = '../documents/pdfs/EO/EO/'
if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)
EO_fname = '../documents_of_type_presidential_document_and_of_presidential_document_type_executive_order'
df = pd.read_csv(EO_fname + '.csv')

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
## Note: I am treating these EOs differently than the other documents because it appears that the .gov site hosting these pdfs has some security measure in place that prevents my usual call to urllib.requests to fail with a 403 error message. My work-around is to use Selenium to open the link in a browser and to then save the pdf in the downloads folder.
download_time = []
download_success = []
for i in range(len(df)):
    try:
        driver.get(df['pdf_url'].iloc[i])
        keyboard = Controller()
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

## the filenames have a space in front that I need to remove, and I need to add .pdf
filenames = list(df['document_number'])
filenames = [f[1:] + '.pdf' for f in filenames]
filepaths = ['documents/pdfs/EO/EO/' + f for f in filenames]

df2 = pd.DataFrame({'Title':df['title'], 'source':source, 'source link':source_link, 'link':df['pdf_url'], 'link date':link_date, 'downloaded on':download_time, 'download success':download_success, 'file name':filenames, 'file path':filepaths})
df2.to_csv('../link_scrapers/logs/EO.csv', index=False)


## close the session
driver.quit()
