
# coding: utf-8

# In[1]:

import asyncio
import datetime
import json
import re
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
# Custom python file to allow import of python notebook "ipynb" as module
import import_notebook

# Python notebook files
from WordFormat import WordFormat
from ExportSheet import ExportSheet


# In[2]:

'''
User tweet will listen and store all tweets that is send to @SG_SMRT
No translation is done but replace of abbrivation words is carried out
'''
class UserTweet:
    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = '80337313-lbccFWgRT0BM8VGvepY9foRbiAXbdKYJOo8kC1NFC'
    ACCESS_SECRET = 'GyPBROB8XPkz3YwRQoJlyNg1kud4ylCPHS73z5M34V7Es'
    CONSUMER_KEY = 'LZ30cTS3iKCZ6XDAlTeTD54xj'
    CONSUMER_SECRET = '1yB0ydySHdFKYcMw0baxYkhzMPgzTkfYvNApoGdfCEnGVqTxV3'

    def listen(self):
        wordFormat = WordFormat()
        exportSheet = ExportSheet()
        oauth = OAuth(self.ACCESS_TOKEN, self.ACCESS_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET)  
        print("Running twitter stream...")
        try:
            # Initiate the connection to Twitter Streaming API
            twitter_stream = TwitterStream(auth=oauth)

            # Get a sample of the public data following through Twitter
            # location lng/lat pair, 1st: south-west 2nd: north-east 
            # My ID: 80337313
            # SMRT_Singapore: 307781209
            # SBSTransit_Ltd: 3087502272
            stream = twitter_stream.statuses.filter(follow="307781209, 3087502272, 80337313", language="en")
        except Exception as e: 
            print("Connecting to twitter error: {}".format(e))   
        
        print("Waiting for twitter msg...")
        
        for tweet in stream:
            try:
                tweetJson = json.dumps(tweet)
                print(tweetJson)

                jsonData = self.extractTweet(tweetJson)                                            
                if jsonData != None:
                    ori_tweet = jsonData['text']
                    replaced_tweet = wordFormat.replaceAbbsWords(jsonData['text'])            
                    thread = Thread(target=writeToSheet(ori_tweet, replaced_tweet))
                    thread.start()
                    thread.join()
            except Exception as e:    
                 print("Error in tweet stream: {}".format(e))
                    
    def writeToSheet(self, ori_tweet, replaced_tweet):
        exportSheet.writeToSheet3Async(ori_tweet, replaced_tweet)
        


# In[ ]:

userTweet = UserTweet()
userTweet.listen()

