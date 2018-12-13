# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 10:52:25 2018

@author: Navid
"""
def ExtractingNumericFeatures(Dict_Input):
    
 import pandas as pd

 from textblob import TextBlob

# Importing the Excel Having the Claim Links List

 Excel_File_Claimed = pd.read_excel('Copy of Fake News List and Claim.xlsx','ClaimLinks')
 Excel_File_Fake1   = pd.read_excel('Copy of Fake News List and Claim.xlsx','FakeNewsList1')
 Excel_File_Fake2   = pd.read_excel('Copy of Fake News List and Claim.xlsx','FakeNewsList2')

# Importing the Input File


 Claimed_Links = [Excel_File_Claimed.Sites][0].tolist()
 Fake_List_1   = [Excel_File_Fake1.Name][0].tolist()
 Fake_List_2   = [Excel_File_Fake2.Name][0].tolist()

#Potential Fake
 if 'www' in Dict_Input['url']:
            X = Dict_Input['url'].split('www.')[1].lower()
 elif '://' in Dict_Input['url']:
            X = Dict_Input['url'].split('://')[1].lower()
 else:
            X = Dict_Input['url'].lower()

 if any(X in u.lower() or u.lower() in X for u in Fake_List_1) or any(X in u.lower() or u.lower() in X for u in Fake_List_2):
    PotentialFake = 1
 elif any(X in u.lower() or u.lower() in X.lower() for u in Claimed_Links):
    PotentialFake = 0
 else:
    PotentialFake = 0.5

#Number of Authors
 if Dict_Input['author'] == ' ':
            NumberAuthor = 0
 else:
            NumberAuthor = len(Dict_Input['author'].split(','))
    
#Title Length
 TitleLength    = len(Dict_Input['title'].split())
#Text Length
 FullTextLength = len(Dict_Input['text'].split())
#Description Length
 TextLength     = len(Dict_Input['description'].split())
#CapitalWordTitle
 if any(s.isupper() for s in Dict_Input['title'].split()):
    CapitalWordTitle = 1
 else:
    CapitalWordTitle = 0

#NumberOfQuotes
 NumberOfQuotes = Dict_Input['text'].count('\"')

#Title Sentiment 
 Title_sentiment = TextBlob(Dict_Input['title']).sentiment.polarity
#Text Sentiment
 Text_sentiment = TextBlob(Dict_Input['text']).sentiment.polarity
#Description Sentiment 
 Description_sentiment = TextBlob(Dict_Input['description']).sentiment.polarity
 # Emotional Language 
 EmotionalLanguage = (abs(Title_sentiment) + abs(Text_sentiment) + abs(Description_sentiment)) / 3

 
 Dict_Input['PotentialFake'] = PotentialFake
 Dict_Input['TitleLength']   = TitleLength
 Dict_Input['FullTextLength'] = FullTextLength
 Dict_Input['TextLength']    = TextLength
 Dict_Input['CapitalWordTitle'] = CapitalWordTitle
 Dict_Input['NumberOfQuotes'] = NumberOfQuotes
 Dict_Input['Title_sentiment'] = Title_sentiment
 Dict_Input['Text_sentiment'] = Text_sentiment
 Dict_Input['Description_sentiment'] = Description_sentiment
 Dict_Input['NumberAuthor'] = NumberAuthor
 Dict_Input['EmotionalLanguage']= EmotionalLanguage
 
 return Dict_Input
 
 








        
    
    


    

        






