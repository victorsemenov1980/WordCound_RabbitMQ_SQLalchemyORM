#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 17:52:11 2021

@author: Viktor Semenov
"""
print('Starting Error Handler')
import pika
import smtplib
from email.message import EmailMessage

def sendmail(filename):
        me = "the sender's email address"
        you = "the recipient's email address"
        msg = EmailMessage()
        msg.set_content(f'Non txt file {filename} found')
        if me == "the sender's email address" or you == "the recipient's email address":
            print('Mail servers are not set, kindly update settings')
            return None
        else:
       
            msg['Subject'] = 'Non TXT file ALERT'
            msg['From'] = me
            msg['To'] = you
            
            # Send the message via our own SMTP server.
            s = smtplib.SMTP('localhost')
            s.send_message(msg)
            s.quit()
        

def consume_errors():
    params=pika.URLParameters('amqps://____your link here')

    connection = pika.BlockingConnection(params)

    channel = connection.channel()
    channel.queue_declare(queue='errors') # Declare a queue
    def callback(ch, method, properties, body):
        sendmail(str(body.decode()))
        
    channel.basic_consume('errors',
                      callback,
                      auto_ack=True)

    print(' [*] Waiting for errors:')
    channel.start_consuming()
    connection.close()
    
consume_errors()
