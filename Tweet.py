
# coding: utf-8

# In[38]:

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


# In[39]:

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
            data = {}            
            # Extracting userID
            userData = jsonData['user']                        
            userID = userData['id_str']
            if userID == '3087502272':
                data['text'] = "[Bus service]{}".format(jsonData['text'])
            else:
                data['text'] = jsonData['text']

            # Extracting entities, for media url         
            try:
                if 'extended_tweet' in jsonData:
                    extTweetData = jsonData['extended_tweet']
                    entitiesData = extTweetData['entities']
                    mediaData = entitiesData['media'][0]
                    media_url = mediaData['media_url']
                    data['media_url'] = media_url                    
            except Exception as e:
                try:
                    if 'entities' in jsonData:
                        entitiesData = jsonData['entities']
                        mediaData = entitiesData['media']
                        media_url = mediaData['media_url']
                        data['media_url'] = media_url
                except Exception as e:
                    print('extractTweet error:{}'.format(e))                
            
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


# In[40]:

# Testing purpose
# wordFormat = WordFormat()
# tweet = Tweet()
# tweet.listen()

# jsonData = wordFormat.readJsonFile('error.json')
# jsonStr = tweet.extractTweet(json.dumps(jsonData))
# print(jsonStr)


