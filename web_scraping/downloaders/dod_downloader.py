# Network Analysis of Vaccination Strategies
# Copyright (C) 2020 by The RAND Corporation
# See LICENSE and README.md for information on usage and licensing

import urllib.request
import datetime
import pandas as pd
import os

doc_type = [
    'instructions',
    'directives',
    'manuals',
    'dtms',
    'admin_instructions'
    ]

pdf_path = '../documents/pdfs/DoD/'
if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)

## scan through each document type
for j in range(len(doc_type)):
    if os.path.exists('../link_scrapers/logs/DoD_' + doc_type[j] + '.csv'):

        if not os.path.exists(pdf_path + doc_type[j]):
            os.makedirs(pdf_path + doc_type[j])

        print('\ndownloading %s documents' %doc_type[j])

        downloaded_time = []
        download_success = []
        filenames = []
        filepaths = []
        df = pd.read_csv('../link_scrapers/logs/DoD_' + doc_type[j] + '.csv')
        hrefs = df['link']

        if not os.path.exists(pdf_path + doc_type[j]):
            os.makedirs(pdf_path + doc_type[j])

        for i in range(len(hrefs)):
            indx1 = hrefs[i].rfind('/') + 1
            indx2 = hrefs[i].rfind('.pdf')
            try:
                message = '\n\n    downloading file: %s' % hrefs[i]
                print(message)
                print('saving it as: %s' %pdf_path + doc_type[j] + '/' + hrefs[i][indx1:indx2+4])
                urllib.request.urlretrieve(hrefs[i], (pdf_path + doc_type[j] + '/' + hrefs[i][indx1:indx2+4]))

                ## append logs
                downloaded_time.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                download_success.append(True)
                filenames.append(hrefs[i][indx1:indx2+4])
                filepaths.append(pdf_path + doc_type[j] + '/' + hrefs[i][indx1:indx2+4])

            except:
                message = '\n\n    failed to download file: %s' % hrefs[i]
                print(message)
                print('wanted to save it as: %s' % (pdf_path + doc_type[j] + '/' + hrefs[i][indx1:indx2+4]))

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
        df.to_csv('../link_scrapers/logs/DoD_' + doc_type[j] + '_afterDL' + '.csv', index=False)
