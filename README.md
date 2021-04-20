# Policy2Vec

## Introduction
This repository contains code used to create a corpus of official US government policy and doctrine documents. It also includes code for a growing list of Natural Language Processing (NLP) applications which utilize this corpus. The repository's name, *Policy2Vec* arose because the first of these applications used the *Doc2Vec* algorithm to train document embeddings for these policy documents.

## Installation
To install, run

```
$ git clone https://code.rand.org/hartnett/policy2vec.git
$ cd policy2vec
$ pip install -r requirements.txt
```
It is recommended to install within a conda environment, in which case the installation commands should be modified to be:

```
$ git clone https://code.rand.org/hartnett/policy2vec.git
$ cd policy2vec
$ conda create --name policy2vec python=3.8
$ conda activate policy2vec
$ pip install -r requirements.txt
```

*Selenium* is used to do the scraping and downloading. *Selenium* will be automatically installed along with the other packages used in this repository, but in addition a web driver file will need to be downloaded in order for *Selenium* to work. The web driver file is specific to the web browser used and the version. This repository assumes the use of Google Chrome. The web driver may be downloaded by following [this link](https://chromedriver.chromium.org/downloads) and downloading the file corresponding to the version of Chrome on your machine. Then, place it into the `web_scraping` directory so that the link scraper scripts may find it. Other browsers such as Safari or Firefox may also be used, but these would require making some minor modifications to the code.

## Corpus of Official USG Documents

### Download a new corpus from scratch
The code in the `web_scraping` directory may be used to scrape official government websites. The currently supported websites are:
- [AF Civil Engineering Center News](https://www.afcec.af.mil/News/)
- [AF E-Publishing](https://www.e-publishing.af.mil/Product-Index/)
- [DoD Issuances](https://www.esd.whs.mil/Directives/issuances/)
- [Goverment Accountability Office (GAO) Reports](https://www.gao.gov/reports-testimonies/month-in-review/)

We have also included support for Executive Orders (EOs) and Congressional Research Service (CRS) reports. These do not require scraping, as the US Government makes available a list of these documents with links. To download these documents, these lists will first have to be downloaded and placed in the `web_scraping` directory. These links may be found here:
- CRS: [click here](https://crsreports.congress.gov/search/#/?termsToSearch=&orderBy=Date) and then click the "bulk download results" button.
- EO list: [click here](https://www.federalregister.gov/presidential-documents/executive-orders) and then click the button to download "All Executive Orders since 1994" as an CSV/Excel file.

The scraping scripts download links to the documents, and not the documents directly. Once the scraping scripts have been run, the scraped links can be downloaded by running the corresponding downloader script. For example, to download all DoD documents, run the commands:
```
## scrape all the DoD document links
python link_scrapers/link_scraper_DoD_admin_instructions.py
python link_scrapers/link_scraper_DoD_directives.py
python link_scrapers/link_scraper_DoD_dtms.py
python link_scrapers/link_scraper_DoD_instructions.py
python link_scrapers/link_scraper_DoD_manuals.py

## download the scraped links
python downloaders/dod_downloader.py
```

### Download a corpus using existing URLs
The repository contains lists of URLs obtained by running the scraping code on Dec 30-31, 2020. These may be found in the `web_scraping/link_scrapers/logs` directory. These may be used to skip the scraping step, although beware that as more time elapses more and more of these links will point to removed documents, and more and more new documents not contained in these lists will have been added to the host websites.

Finally, to convert the downloaded pdf's to raw text files, run `python web_scraping/pdf_parser.py`. The NLP applications will use this as input.

A cautionary note: the government websites are periodically updated in ways that break the scraping scripts. Often these can be fixed with minor tweaks to the code.

### Natural Language Processing (NLP) Applications
A growing list of NLP applications may be found in the `nlp` directory.

#### search tool
Perhaps the simplest way in which the corpus can be used is by performing simple keyword searches. A very rudimentary search capability is provided by the notebook `search_tool.ipynb`. In the future it would be good to improve this to a web-based search tool. Also, the current version does not use indexing, and as a result the searches are a bit slow.

#### document embeddings
The "policy2vec.ipynb" notebook used The [*Gensim* implementation of Doc2Vec](https://radimrehurek.com/gensim/models/doc2vec.html) to train document embeddings for the downloaded policy documents (hence the name, Policy2Vec). This notebook was used to generate the results discussed in the [technical note](technical_note.pdf).
