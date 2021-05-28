#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 12:27:35 2021

@author: Viktor Semenov
"""

from bs4 import BeautifulSoup
import requests
import nltk
from nltk.stem import WordNetLemmatizer
from datetime import datetime
log=[]
log.append(str(datetime.now(tz=None)))
#link=input('Please enter the URL for scrapping: ')


def my_scrapper(link):
    
    try: 
        doc=requests.get(link)
        page=doc.content
        soup=BeautifulSoup(page,'html.parser')
        site_text=soup.get_text()
        return site_text
    except:
        print('There is a problem with link provided')
        return 0

def my_tokenizer(s):
    wordnet_lemmatizer = WordNetLemmatizer()
    s = s.lower() # downcase
    tokens = nltk.tokenize.word_tokenize(s) # split string into words (tokens)
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [wordnet_lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    return tokens

def scrape_link(link):
    log.append(link)
    page_=my_scrapper(link)
    if page_!=0:
        tokens_list=my_tokenizer(page_)
        log.append('Number of words scrapped and saved:')
        log.append(str(len(tokens_list)))
        unique_name=str(datetime.now(tz=None))
        log_file_name='scrapper_log'+unique_name+'.txt'
        txt_file_name='page_text'+unique_name+'.txt'
        with open(f'LogFiles/{log_file_name}','w') as l_file:
            for i in log:
                l_file.write(i+ "\n")
        with open(f'TXTfiles/{txt_file_name}','w') as t_file:
            for i in tokens_list:
                t_file.write(i+ "\n")




