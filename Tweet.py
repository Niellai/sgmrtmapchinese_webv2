
# coding: utf-8

# In[2]:

import json
import re
import asyncio
# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
# Custom python file to allow import of python notebook "ipynb" as module
import import_notebook

# Python notebook files
from FCM import FCM
from WordFormat import WordFormat
from ExportSheet import ExportSheet


# In[1]:

class Tweet:
    
    # define keys to look out for in tweet msg
    keyList = ['incident', 'no train', 'fault', 'resumed', 'svc', 'svcs',
           'service', 'serivces', '[NSL]', '[EWL]', '[CCL]', '[DTL]', '[TSL]']

    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = '80337313-lbccFWgRT0BM8VGvepY9foRbiAXbdKYJOo8kC1NFC'
    ACCESS_SECRET = 'GyPBROB8XPkz3YwRQoJlyNg1kud4ylCPHS73z5M34V7Es'
    CONSUMER_KEY = 'LZ30cTS3iKCZ6XDAlTeTD54xj'
    CONSUMER_SECRET = '1yB0ydySHdFKYcMw0baxYkhzMPgzTkfYvNApoGdfCEnGVqTxV3'

    # Listen for tweet, will loop endlessly until exception occurs
    def listen(self):
        wordFormat = WordFormat()
        fcm = FCM()
        exportSheet = ExportSheet()
        
        oauth = OAuth(self.ACCESS_TOKEN, self.ACCESS_SECRET, self.CONSUMER_KEY, self.CONSUMER_SECRET)  
        print("Running twitter stream...")
        
        try:
            # Initiate the connection to Twitter Streaming API
            twitter_stream = TwitterStream(auth=oauth)

            # Get a sample of the public data following through Twitter
            # location lng/lat pair, 1st: south-west 2nd: north-east 
            stream = twitter_stream.statuses.filter(follow="307781209, 80337313", language="en")
        except Exception as e: 
            print("Connecting to twitter error: {}".format(e))       
        
        print("Waiting for twitter msg...")
             
        for tweet in stream:
            try:            
                tweetJson = json.dumps(tweet)
                jsonData = self.extractTweet(tweetJson)                 
                ori_tweet = jsonData['text']
                
                replaced_tweet, translated_tweet = wordFormat.translateTweet(jsonData['text'])               
                jsonData['text'] = translated_tweet
                
                if self.containKey(ori_tweet):
                    fcm.send_default(jsonData)                 
                
                exportSheet.writeToSheet(jsonData['timestamp_ms'], ori_tweet, replaced_tweet, translated_tweet)                
                print("Waiting for twitter msg...")
            except Exception as e: 
                print("Error in tweet stream: {}".format(e))

    # Extract tweet and return json object             
    def extractTweet(self, tweetsStr):
        try:
            jsonData = json.loads(tweetsStr)            
            # ori_tweet = jsonData['text']        
            data = {}
            userData = jsonData['user']
            userID = userData['id_str']
            if userID == '307781209':
                data['text'] = "[Bus service]{}".format(jsonData['text'])
            else:
                data['text'] = jsonData['text']                     
            data['timestamp_ms'] = int(jsonData['timestamp_ms'])        
            jsonDataStr = json.dumps(data, ensure_ascii=False)   
            print("Tweet received: {}".format(data['text']))
            return json.loads(jsonDataStr)    
        except Exception as e: 
            print("ExtractTweet error: {}".format(e))                 
            
    # Will only match exact word in the sentence
    def containKey(self, jsonData):
        isContainKey = False
        for key in self.keyList:    
            result = self.findWholeWord(key)(jsonData)
            if result is not None:        
                isContainKey = True
                break
        return isContainKey
    
    def findWholeWord(self, w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


# In[ ]:

# Testing purpose
# wordFormat = WordFormat()
tweet = Tweet()
# dataJson = wordFormat.readJsonFile('singleTweet.txt')
# tweet.extractTweet(json.dumps(dataJson))

tweet.listen()

