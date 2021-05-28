#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 12:26:23 2021

@author: Viktor Semenov
"""

from scrapper import scrape_link
from producer import file_check

import schedule
import time


txt_dir = ('TXTfiles')
link=input('Please enter the URL for scrapping: ')
scrape_link(link)


schedule.every(1).minutes.do(file_check,txt_dir)
    
while True:
  
    schedule.run_pending()
    time.sleep(1)



