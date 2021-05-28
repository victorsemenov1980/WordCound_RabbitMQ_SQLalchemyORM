#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 17:47:34 2021

@author: Viktor Semenov
"""
print('Starting Parser')
from db_procedures import update_words,csv_query,delete_words
import os
import pika
from datetime import datetime

word_count_limit=5


file='CSVfile/deleted_words.csv'

def save_csv(dict_,file):
    log=[]
    log.append(str(datetime.now(tz=None)))
    with open(file,'a') as deleted_words:
        deleted_words.write('\n')
        deleted_words.write(str(datetime.now()))
        for key,value in dict_.items():
            deleted_words.write(key)
            deleted_words.write('--->')
            for i in value:
                deleted_words.write(str(i))
            deleted_words.write('\n')
        unique_name=str(datetime.now(tz=None))
        log_file_name='csv_log'+unique_name+'.txt'
        log.append('Words deleted from db: ')
        log.append(str(len(dict_)))
        with open(f'LogFiles/{log_file_name}','w') as l_file:
            for i in log:
                l_file.write(i+ "\n")

def check_db(limit):
    
    query=csv_query(limit)
    to_delete={}
    for word, parameters in query.items():
        to_delete[word]=[]
        to_delete[word].append(parameters[0])
        to_delete[word].append(parameters[1])
        delete_words(word)
    if len(to_delete)>0:
        save_csv(to_delete, file)

def count_words(file):
    
    file_=os.path.join('TXTfiles/',file)
    word_count={}
    
    with open(file_,'r') as word_list:
        for line in word_list:
            string=line.rstrip()
            if string in word_count:
                word_count[string]+=1
            else:
                word_count[string]=1
    for word, count in word_count.items():
        update_words(word, count, file)
    check_db(word_count_limit)
        
    

def consume_files():
    params=pika.URLParameters('amqps://____your link here')

    connection = pika.BlockingConnection(params)

    channel = connection.channel()
    channel.queue_declare(queue='new_files') # Declare a queue
    def callback(ch, method, properties, body):
        print('Received new file')
        
        count_words(str(body.decode()))
        
    channel.basic_consume('new_files',
                      callback,
                      auto_ack=True)

    print(' [*] Waiting for files:')
    channel.start_consuming()
    connection.close()

consume_files()





    
   