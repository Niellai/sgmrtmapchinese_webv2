
# coding: utf-8

# In[56]:

import json
import codecs
import os.path
import re

# Custom python file to allow import of python notebook "ipynb" as module
import import_notebook

# Google translator
from Translator import Translator


# In[59]:

'''
Replacement of abb words and train line and station names
'''

class WordFormat:
    
    def __init__(self):        
        self.abb_replace = self.readJsonFile("abb_replacement.json")
        self.line_tran = self.readJsonFile("line_translation.json")
        self.station_tran = self.readJsonFile("station_translation.json")
    
    # Read json file, return JSON object
    def readJsonFile(self, fileName):
        try:
            with codecs.open(fileName, "r", "utf-8") as file:               
                jsonData = json.loads(file.read())        
                return jsonData
        except Exception as e:
            print("readJsonFile Error: {}".format(e))
        
    def replaceAbbsWords(self, sentence): 
        try:
            for key in self.abb_replace:        
                sentence = re.sub(r"\b{}\b".format(key), self.abb_replace[key], sentence, flags=re.IGNORECASE)    
                sentence = sentence.replace('&amp;', 'and')
            return sentence
        except Exception as e:
            print("replaceAbbsWords Error: {}".format(e))
            
    # From here on all sentence are suppose to be in chinese
    def replaceStationWords(self, sentence):
        try:
            sentence = sentence.replace(" ", "")
            for station in self.station_tran:
                name = station["name"].replace(" ", "")
                ch_name = station["ch_name"]
                sentence = re.sub(r"{}".format(name), ch_name, sentence, flags=re.IGNORECASE)            
            return sentence
        except Exception as e:
            print("replaceStationWords Error: {}".format(e))          
            
    def replaceTrainLineWords(self, sentence):
        try:
            sentence = sentence.replace(" ", "")
            for lineEng in self.line_tran:        
                line_ch = self.line_tran[lineEng]
                sentence = re.sub(r"{}".format(lineEng), line_ch, sentence, flags=re.IGNORECASE)
            return sentence
        except Exception as e:
            print("replaceTrainLineWords Error: {}".format(e))            
    
    # Translate English tweet to chinese Tweet
    def translateTweet(self, sentence):
        try:             
            translator = Translator()
            replaced_tweet = self.replaceAbbsWords(sentence)
            temp_tweet = translator.toChinese(replaced_tweet)
            temp_tweet = self.replaceStationWords(temp_tweet)
            translated_tweet = self.replaceTrainLineWords(temp_tweet)      
            return replaced_tweet, translated_tweet           
        except Exception as e:
            print("Error in translateTweet: {}".format(e))
            
    def html_escape(self, text):
        """Produce entities within text."""
        return "".join(html_escape_table.get(c,c) for c in text)


# In[55]:

'''
Example / Test methods
'''
# sentence = 'Tweet received: Please be informed that svc 192 will skip bus stops along Tuas Ave 1 &amp; Tuas Ave 12, for both directions, due to a building on fire.'
# wordFormat = WordFormat()
# wordFormat.replaceAbbsWords(sentence)


