# Network Analysis of Vaccination Strategies
# Copyright (C) 2020 by The RAND Corporation
# See LICENSE and README.md for information on usage and licensing

## This script goes through the pdf files located in the documents/pdfs directory and converts each file into a text file using pdftotext.

import os
import subprocess
import string, random

pdf_path = 'documents/pdfs/'
parsed_path = 'documents/parsed_text/'

## scan through top-level directories
dirnames_1 = os.listdir(pdf_path)
for d1 in dirnames_1:
    if d1 != '.DS_Store':
        ## create corresponding top-level directory in parsed_text
        if not os.path.exists(parsed_path + d1):
            os.makedirs(parsed_path + d1)
        dirnames_2 = os.listdir(pdf_path + d1)

        ## scan through 2nd-level directories
        for d2 in dirnames_2:
            if d2 != '.DS_Store':
                ## create corresponding low-level directory in parsed_text
                if not os.path.exists(parsed_path + d1 + '/' + d2):
                    os.makedirs(parsed_path + d1 + '/' + d2)

                ## path
                path_to_pdf = pdf_path + d1 + '/' + d2 + '/'
                path_to_txt = parsed_path + d1 + '/' + d2 + '/'

                ## all the filenames within the current pdf directory
                filenames = os.listdir(path_to_pdf)

                for f in filenames:
                    if f.endswith('.pdf'):
                        print(f)
                        bashCommand = 'pdftotext ' + path_to_pdf + f + " " + path_to_txt + f[0:-4] + '.txt'
                        print('bash command = ', bashCommand.split())
                        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                        output, error = process.communicate()
