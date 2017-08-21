
# coding: utf-8

# In[1]:

import json
import gspread
import asyncio
import datetime
from concurrent.futures import ThreadPoolExecutor
from oauth2client.service_account import ServiceAccountCredentials


# In[2]:

class ExportSheet:
   
    # Requires creds.json 
    # Export tweet to Google sheet
    def writeToSheet(self, timestampStr, ori_tweet, replaced_tweet, translated_tweet):
        try:   
            json_key = json.load(open('creds.json'))
            scope = ['https://spreadsheets.google.com/feeds']

            credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
            gs = gspread.authorize(credentials)
            sh1 = gs.open("sg translation").sheet1    

            print("Writing to sheets")
            new_row = [timestampStr, ori_tweet, replaced_tweet, translated_tweet]    
            sh1.insert_row(new_row, index=2)
            print("Write to sheets completed")
        except Exception as e:
            print("writeToSheet Error: {}".format(e))
            
    def writeToSheet2(self, timestampStr, ori_tweet, replaced_tweet, translated_tweet):
        try:   
            json_key = json.load(open('creds.json'))
            scope = ['https://spreadsheets.google.com/feeds']

            credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
            gs = gspread.authorize(credentials)
            sh2 = gs.open("sg translation")
            sh2 = sh2.get_worksheet(1)

            print("Writing to sheets")
            new_row = [timestampStr, ori_tweet, replaced_tweet, translated_tweet]    
            sh2.insert_row(new_row, index=2)
            print("Write to sheets completed")
        except Exception as e:
            print("writeToSheet Error: {}".format(e))
            
    def writeToSheet3(self, ori_tweet, replaced_tweet):
        try:
            json_key = json.load(open('creds.json'))
            scope = ['https://spreadsheets.google.com/feeds']

            credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
            gs = gspread.authorize(credentials)
            sh2 = gs.open("sg translation")
            sh2 = sh2.get_worksheet(2)

            print("Writing to sheets")
            dateStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = [dateStr, ori_tweet, replaced_tweet]
            sh2.insert_row(new_row, index=2)
            print("Write to sheets completed")
        except Exception as e:
            print("writeToSheet Error: {}".format(e))            


# In[13]:



