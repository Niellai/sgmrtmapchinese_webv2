
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


# In[ ]:

'''
User tweet will listen and store all tweets that is send to @SG_SMRT
No translation is done but replace of abbrivation words is carried out
'''
class UserTweet:
    # Variables that contains the user credentials to access Twitter API 
    ACCESS_TOKEN = '80337313-rAQ0Gt8CEe3qnrWiL6iJ0GyAcfS8d9hjrKGQQE9mG'
    ACCESS_SECRET = 'fro20QRxZRMUjk4RtM2fLo6qqG5FKdP2jbI4ObkDH1xim'
    CONSUMER_KEY = 'h6CH9ELrd3Xv6BIKpftJQJEjF'
    CONSUMER_SECRET = 'Emy1z0aIQGF0aU8g9nuK8iAojUGH7oyMdNvuafYSKEkSK3nzkm'

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
                    thread = Thread(target=exportSheet.writeToSheet3Async(ori_tweet, replaced_tweet))
                    thread.start()
                    thread.join()
            except Exception as e:    
                 print("Error in tweet stream: {}".format(e))

    # Extract tweet and return json object, return null when not send from targeted user             
    def extractTweet(self, tweetsStr):
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
            if userID == '3087502272':
                data['text'] = "[Bus service]{}".format(jsonData['text'])
            elif userID == '307781209' or userID == '80337313':
                data['text'] = jsonData['text']
            else:     
                data['text'] = jsonData['text']                                                   
                        
            jsonDataStr = json.dumps(data, ensure_ascii=False)   
            print("Tweet received: {}".format(data['text']))
            return json.loads(jsonDataStr)    
        except Exception as e: 
            print("ExtractTweet error: {}".format(e))           


# In[2]:

# exportSheet = ExportSheet()
# thread = Thread(target=exportSheet.writeToSheet3Async("ori_tweet", "replaced_tweet"))
# thread.start()
# thread.join()

# userTweet = UserTweet()
# userTweet.listen()

