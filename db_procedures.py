#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:08:11 2021

@author: Viktor Semenov
"""
from model import Word,File
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine=create_engine('sqlite:///db_test_task.db', echo=True)
Session = sessionmaker(bind=engine)
Base=declarative_base()
session = Session()

def create_db():
    Base.metadata.create_all(engine)
    
create_db()


def check_words():
    current_state={}
    for row in session.query(Word).all():
        current_state[row.word]=[]
        current_state[row.word].append(row.count)
        current_state[row.word].append(row.files)
    return current_state


def update_words(word,count,file_name):
    all_words=check_words()
    file=File(file_name=file_name)
    sql_add=[]
    if word in all_words.keys():
        db_word = session.query(Word).filter(Word.word==word).first()
        db_word.count += count
        db_word.files.append(file)
        session.commit()
    else:
        word_add=Word(word=word,count=count,files=[file])
        sql_add.append(word_add)
        
    session.add_all(sql_add)
    session.commit() 

def delete_words(word):
    word_delete = session.query(Word).filter(Word.word==word).first()
    print('Deleting word: ',word)
    session.delete(word_delete)
    session.commit()

def csv_query(limit):
    all_data={}
    
    for row in session.query(Word).filter(Word.count>=limit):
        all_data[row.word]=[]
        all_data[row.word].append(row.count)
        all_data[row.word].append(row.files)
    return all_data