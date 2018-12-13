# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 12:31:18 2018

@author: Navid
"""

# Analyzing Current Data Table 

import pandas as pd
import csv
from textblob import TextBlob
import matplotlib.pyplot as plt



list_nonEnglish = [0,5,12,16,22,39,40,43,44,48,56,67]

# Importing the Excel Having the Claim Links List

Excel_File_Claimed = pd.read_excel('Copy of Fake News List and Claim.xlsx','ClaimLinks')
Excel_File_Fake1   = pd.read_excel('Copy of Fake News List and Claim.xlsx','FakeNewsList1')
Excel_File_Fake2   = pd.read_excel('Copy of Fake News List and Claim.xlsx','FakeNewsList2')

input_user = pd.read_csv('Complete (1).csv')

Claimed_Links = [Excel_File_Claimed.Sites][0].tolist()
Fake_List_1   = [Excel_File_Fake1.Name][0].tolist()
Fake_List_2   = [Excel_File_Fake2.Name][0].tolist()
titles        = [] #[input_user.Title][0].tolist()
texts         = [] #[input_user.Text][0].tolist()
descriptions  = [] #[input_user.Description][0].tolist()
urls          = [] #[input_user.URL][0].tolist()
authors       = [] #[input_user.Author][0].tolist()
PotentialFake = []
NumberAuthor  = []
TitleLength   = []
FullTextLength = []
TextLength    = []
CapitalWordTitle = []
NumberOfQuotes = []
Title_sentiment = []
Text_sentiment = []
Description_sentiment = []
update_date = []
ad_count    = []



for i in range(len(input_user)):
    if i not in list_nonEnglish:
    

#Potential Fake
        titles.append(input_user.Title[i])
        texts.append(input_user.Text[i])
        descriptions.append(input_user.Description[i])
        urls.append(input_user.URL[i])
        authors.append(input_user.Author[i])
        # Identifying the URL Type
        # Type1 : has www.
        # Type2 : does not have www.
        if 'www' in input_user.URL[i]:
            X = input_user.URL[i].split('www.')[1]
        else:
            X = input_user.URL[i].split('://')[1]
            
        if any(input_user.URL[i] in u for u in Claimed_Links):
            PotentialFake.append(0)
        elif any(X in u for u in Fake_List_1) or any(X in u for u in Fake_List_2):
            PotentialFake.append(1)
        else:
            PotentialFake.append(0.5)

#Number of Authors
        if input_user.Author[i] == '[]':
            NumberAuthor.append(0)
        else:
            NumberAuthor.append(len(input_user.Author[i].split(',')))
    
#Title Length
        TitleLength.append( len(input_user.Title[i].split()))
#Text Length
        FullTextLength.append(len(input_user.Text[i].split()))
#Description Length
        TextLength.append( len(input_user.Description[i].split()))
#CapitalWordTitle
        if any(s.isupper() for s in input_user.Title[i].split()):
            CapitalWordTitle.append(1)
        else:
            CapitalWordTitle.append(0)

#NumberOfQuotes
        NumberOfQuotes.append( input_user.Text[i].count('@'))

#Title Sentiment 
        Title_sentiment.append(TextBlob(input_user.Title[i]).sentiment.polarity)
#Text Sentiment
        Text_sentiment.append(TextBlob(input_user.Text[i]).sentiment.polarity)
#Description Sentiment 
        Description_sentiment.append(TextBlob(input_user.Description[i]).sentiment.polarity)
        update_date.append(0)
        ad_count.append(0)

with open('Fake-news-original.csv', mode='a', newline="") as input_file:
            #Title,Text,Description,Author,URL,AdvertisementCount,UpdatedDate
            input_writer = csv.writer(input_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in range(0,64):
             input_writer.writerow([titles[row].encode(),texts[row].encode(),descriptions[row].encode(), authors[row], urls[row], ad_count[row], update_date[row]
             ,PotentialFake[row],NumberAuthor[row],TitleLength[row],FullTextLength[row],TextLength[row],CapitalWordTitle[row],NumberOfQuotes[row]
             ,Title_sentiment[row],Text_sentiment[row],Description_sentiment[row]])

