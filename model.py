#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:12:06 2021

@author: Viktor Semenov
"""



# from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
# from sqlalchemy.orm import sessionmaker


# engine=create_engine('sqlite:///db_test_task.db', echo=True)
# Session = sessionmaker(bind=engine)
Base=declarative_base()
# session = Session()

class Word(Base):
    __tablename__='words'
    id=Column(Integer, primary_key=True)
    word=Column(String)
    count=Column(Integer)
    files = relationship("File", back_populates='word',cascade="all, delete,delete-orphan")
    
    def __repr__(self):
        return "<Word = '%s' --> count = '%s'>"%(self.word,self.count)

class File(Base):
    __tablename__='files'
    id=Column(Integer, primary_key=True)
    word_id=Column(Integer, ForeignKey('words.id'))
    file_name=Column(String)
    word = relationship("Word", back_populates="files")
       
    def __repr__(self):
        return "<File name = '%s'>"%(self.file_name)
    
# def create_db():
#     Base.metadata.create_all(engine)
    
# create_db()







    






    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    