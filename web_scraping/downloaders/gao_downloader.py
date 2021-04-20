# Network Analysis of Vaccination Strategies
# Copyright (C) 2020 by The RAND Corporation
# See LICENSE and README.md for information on usage and licensing

import urllib.request
import datetime
import pandas as pd
import os, re
import string, random

doc_type = ['GAO']

pdf_path = '../documents/pdfs/'
if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)

## scan through each document type
for j in range(len(doc_type)):

    path = pdf_path + doc_type[j] + '/' + doc_type[j]
    if os.path.exists('../link_scrapers/logs/' + doc_type[j] + '.csv'):
        if not os.path.exists(pdf_path + doc_type[j]):
            os.makedirs(pdf_path + doc_type[j])

        print('\ndownloading %s documents' %doc_type[j])

        downloaded_time = []
        download_success = []
        filenames = []
        filepaths = []
        df = pd.read_csv('../link_scrapers/logs/' + doc_type[j] + '.csv', encoding = "utf-8")
        hrefs = df['link']

        if not os.path.exists(path):
            os.makedirs(path)

        for i in range(len(hrefs)):

            try:
                indx1 = hrefs[i].rfind('/') + 1
                indx2 = hrefs[i].rfind('.pdf')
                fname_tmp = df['Title'].iloc[i]
                fname = re.sub('[^A-Za-z0-9]+', '', fname_tmp)

                ## add a random string at the end to avoid duplicates
                fname = fname + '_' + ''.join(random.sample(string.ascii_lowercase, 3))

                #urllib.request.urlretrieve(hrefs[i], (path + '/' + hrefs[i][indx1:indx2+4]))
                urllib.request.urlretrieve(hrefs[i], (path + '/' + fname + '.pdf'))

                ## append logs
                downloaded_time.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                download_success.append(True)
                filenames.append(fname + '.pdf')
                filepaths.append(path + '/' + fname + '.pdf')
                message = '\n\n    downloaded file: %s' % (fname + '.pdf')
                print(message)

            except:
                message = '\n\n    failed to download file: %s' % (fname + '.pdf')
                print(message)
                #print('wanted to save it as: %s' % (path + '/' + hrefs[i][indx1:indx2+4]))

                ## append logs
                downloaded_time.append('')
                download_success.append(False)
                filenames.append('None')
                filepaths.append('None')

        ## add to csv file
        df['downloaded on'] = downloaded_time
        df['download success'] = download_success
        df['file name'] = filenames
        df['file path'] = filepaths

        ## save
        df.to_csv('../link_scrapers/logs/' + doc_type[j] + '_afterDL' + '.csv', index=False)
