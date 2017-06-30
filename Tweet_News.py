
# coding: utf-8

# In[1]:

import json
import re
import asyncio
# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
# Custom python file to allow import of python notebook "ipynb" as module
import import_notebook

# Python notebook files
from WordFormat import WordFormat
from ExportSheet import ExportSheet


# In[2]:

class Tweet_News:
    
    # define keys to look out for in tweet msg
    keyList = ['incident', 'no train', 'fault', 'resumed', 'svc', 'svcs',
           'service', 'serivces', '[NSL]', '[EWL]', '[CCL]', '[DTL]', '[TSL]']

    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = '80337313-rAQ0Gt8CEe3qnrWiL6iJ0GyAcfS8d9hjrKGQQE9mG'
    ACCESS_SECRET = 'fro20QRxZRMUjk4RtM2fLo6qqG5FKdP2jbI4ObkDH1xim'
    CONSUMER_KEY = 'h6CH9ELrd3Xv6BIKpftJQJEjF'
    CONSUMER_SECRET = 'Emy1z0aIQGF0aU8g9nuK8iAojUGH7oyMdNvuafYSKEkSK3nzkm'

    # Listen for tweet, will loop endlessly until exception occurs
    # Refer to twitter API documentation
    # https://dev.twitter.com/streaming/overview/request-parameters#follow
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
            # ChannelNewsAsia:  38400130
            stream = twitter_stream.statuses.filter(follow="38400130", language="en")
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
                
                    replaced_tweet, translated_tweet = wordFormat.translateTweet(jsonData['text'])               
                    jsonData['text'] = translated_tweet                                 
                
                    exportSheet.writeToSheet2(jsonData['timestamp_ms'], ori_tweet, replaced_tweet, translated_tweet)
                print("Waiting for twitter msg...\n")                
            except Exception as e: 
                print("Error in tweet stream: {}".format(e))

    # Extract tweet and return json object, return null when not send from targeted user             
    def extractTweet(self, tweetsStr):
        exportSheet = ExportSheet()
        
        try:            
            jsonData = json.loads(tweetsStr)                        
            
            # Ignore retweet
            if jsonData['retweeted'] == True:
                print('Retweet ignored')
                return
            
            # Extracting userID
            data = {}                        
            userData = jsonData['user']                        
            userID = userData['id_str']
            if userID == '38400130':
                data['text'] = jsonData['text']            
            else:     
                print('Ignore current tweet')
                return
            
            # Extracting entities, for media url         
            try:
                if 'extended_tweet' in jsonData:
                    extTweetData = jsonData['extended_tweet']
                    entitiesData = extTweetData['entities']
                    mediaData = entitiesData['media'][0]
                    media_url = mediaData['media_url']
                    if len(media_url) > 0:
                        data['media_url'] = media_url                    
            except Exception as e:
                print('extractTweet > extended_tweet error:{}'.format(e)) 
                
            try:
                if 'entities' in jsonData:
                    entitiesData = jsonData['entities']
                    mediaData = entitiesData['media'][0]
                    media_url = mediaData['media_url']
                    if len(media_url) > 0:
                        data['media_url'] = media_url
            except Exception as e:
                print('extractTweet > entities error:{}'.format(e))                               
            
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


# In[9]:

# Testing purpose
# wordFormat = WordFormat()
# tweet = Tweet()

# jsonData = wordFormat.readJsonFile('singleTweet.json')
# jsonStr = tweet.extractTweet(json.dumps(jsonData))
# print(jsonStr)

