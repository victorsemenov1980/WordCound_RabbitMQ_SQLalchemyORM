#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 19:32:19 2021

@author: Viktor Semenov
"""

from os import listdir
from os.path import isfile, join
import mimetypes
from datetime import datetime

import pika



params=pika.URLParameters('amqps://____your link here')

#txt_dir = ('TXTfiles')


def publish_good(file_name):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='new_files') # Declare a queue
    
    message = file_name
    channel.basic_publish(exchange='', routing_key='new_files', body=message)
    print(" [x] Sent %r" % message)
    connection.close()

def publish_bad(file_name):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='errors') # Declare a queue
   
    
    message = file_name
    channel.basic_publish(exchange='', routing_key='errors', body=message)
    print(" [x] Sent %r" % message)
    connection.close()
    


def file_check(dir_):
    file_list=[]
    with open('filelist.txt','r+') as file:
        for line in file:
            file_list.append(line.rstrip('\n'))
        
        file.write(str(datetime.now()))
        file.write('\n')
    
    onlyfiles = [f for f in listdir(dir_) if isfile(join(dir_, f))]
    
    for i in onlyfiles:
        if i not in file_list:
            file_type=mimetypes.guess_type(i)
            if file_type[0] != 'text/plain':
                print('ALERT',' filename: ', i)
                publish_bad(i)
            else:
                print(i,'-->',file_type[0])
                publish_good(i)
            with open('filelist.txt','a') as file:
                file.write(i)
                file.write('\n')
        else:
            print('Found already processed file ',i)


        
      
        
        