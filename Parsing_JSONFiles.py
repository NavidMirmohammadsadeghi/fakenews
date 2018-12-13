#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 12:27:03 2018

@author: Navidmms
"""

import json
from os import listdir
from os.path import isfile,join

import csv

directory = 'News Articles'

onlyFiles = [f for f in listdir(directory) if isfile(join(directory,f))]

News_article = {}
News_article['Title'] = [];
News_article['Description'] = [];
News_article['Publish_time'] = [];
News_article['Source_URL'] = [];
News_article['Authors'] = [];
#News_article['Text'] = [];
News_Seconds = {}
News_Seconds['Title']  = []
News_Seconds['Text'] = []

Titles = []
Texts = []
title = []
text = []
desci = []
author = []
time = []
url = []


for j in range(1,len(onlyFiles)):
 
 if(j%20==0):
     print("20 More Analyzed!")
    

 with open(directory+"/"+ onlyFiles[j]) as json_data:
    d = json.load(json_data)
    try:
      #Text        = d['text']
      #News_article['Text'].append(Text)
      text        = d['text']
      title_second = d['title']
      News_Seconds['Text'].append(text)
      News_Seconds['Title'].append(title_second)
      Titles.append(title_second)
      Texts.append(text)
      Title       = d['meta_data']['og']['title']
      Description = d['meta_data']['og']['description']
      desci.append(Description)
      Publish_time = d['publish_date']
      Source_URL   = d['source_url']
      Authors      = d['authors']
      #print(d['meta_data'])
      title.append(Title )
      time.append(Publish_time)
      url.append(Source_URL)
      author.append(Authors)
    except:
         print("this row had issue"+ str(j))
         pass

      
with open('title.csv','w') as csv_file:
  fieldnames = ['Title','Text']  
  writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
  writer.writeheader()
  for row in range(0,len(title)):
      writer.writerow({'Title':title[row].encode(),'Text':desci[row].encode()})

with open('Complete.csv','w') as csv_file:
  fieldnames = ['Title','Description','Time','URL','Author']  
  writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
  writer.writeheader()
  for row in range(0,len(title)):
      writer.writerow({'Title':title[row].encode(),'Description':desci[row].encode(),'Time':time[row],'URL':url[row],'Author':author[row]})

    
