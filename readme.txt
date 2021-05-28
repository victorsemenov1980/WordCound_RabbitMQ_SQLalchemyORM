#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 12:10:11 2021

@author: Viktor Semenov
"""

Word count module with SQL ORM and RabbitMQ

Visual structure is in the wireframe.pdf file

This is ready for docker build
For run use: docker run -ti 

Conda env .yml file also provided

This module: 
- scrapes some web page for text
- tokenizes (with NLTK) words found on the page
- saves every page tokens in separate file with datetime unique name
- checks folder for new files every minute 
- checks the types of file and sends .txt new files into Rabbit AMQP cloud
queue "new_files" and non-txt files into "errors" queue
- error handler listens to the errors queue and sends email if there is a message
- parser listens to the new_files queue and puts the words into db
- db here is SQlite, however db access is via SQL Alchemy ORM, so no matter
what relational db to use
- with unique word count exceeding some number module deletes them from db and
saves into csv file

NOTE:
-csv module and scrapper module keep logs in txt files with unique datetime names
- for concurrent run of all .py files in bash there is a load.sh file

NB:
SetUps
1. In app.py the txt files dir path is located
2. in parse.py csv file path is located and word count limit is being set
3. in producer.py and parse.py for AMQP cloud there is a need to put the link
4. in error_handler.py the email accounts need to be set
5. in db_procedures.py the path to database is set

Notes of further improvements:
1. SQL Alchemy ORM offers rather slow way of updating existing words counts.
This issue needs to be addressed further
2. Pika RabbitMQ connection can die on long tasks (big web pages), probably
need to use Select connection instead of Blocking connection.

