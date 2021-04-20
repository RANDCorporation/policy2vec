# Network Analysis of Vaccination Strategies
# Copyright (C) 2020 by The RAND Corporation
# See LICENSE and README.md for information on usage and licensing

## This notebook removes any non-alphanumeric characters in the GAO filenames.
import urllib.request
import datetime
import pandas as pd
import os, re
import numpy as np

doc_type = ['GAO']

pdf_path = '../documents/pdfs/'
if not os.path.exists(pdf_path):
    os.makedirs(pdf_path)

## scan through each document type
for j in range(len(doc_type)):

    path = pdf_path + doc_type[j] + '/' + doc_type[j]
    df = pd.read_csv('../link_scrapers/logs/' + doc_type[j] + '_afterDL.csv', encoding = "utf-8")
    filenames = []
    filepaths = []

    print(len(df['Title']), len(np.unique(df['Title'])))

    for i in range(1): #range(len(df)):

        if df['download success'].iloc[i] == True:
            fname_old = df['Title'].iloc[i]
            fname = re.sub('[^A-Za-z0-9]+', '', fname_old)

            filenames.append(fname + '.pdf')
            filepaths.append(path + '/' + fname + '.pdf')

            os.rename(path + '/' + fname_old + '.pdf', path + '/' + fname + '.pdf')

        else:
            filenames.append('None')
            filepaths.append('None')

    ## add to csv file
    df['file name'] = filenames
    df['file path'] = filepaths

    ## save
    df.to_csv('../link_scrapers/logs/' + doc_type[j] + '_afterDL2' + '.csv', index=False)
