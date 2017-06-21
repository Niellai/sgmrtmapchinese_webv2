
# coding: utf-8

# In[1]:

import json

# Import google api for translation
from googleapiclient.discovery import build


# In[3]:

class Translator:
    
    '''
    Google translate English to Chinese, return Chinese String
    '''
    def toChinese(self, sentence):        
        try:
            print("Started translating")
            service = build('translate', 'v2', developerKey='AIzaSyAQMAyPPGTnBv1yQCiMvgm-8pjJ-XJ5ygQ')
            result = service.translations().list(source='en', target='zh-CN', q=[sentence]).execute()    
            translatedObj = result['translations'][0]
            translatedText = translatedObj['translatedText']
            print("Translate completed")
            return translatedText
        except Expection as e:
            print("tranlateToChinese: {}".format(e))
        
        


# In[7]:

# translator = Translator()
# translator.toChinese('[EWL]UPDATE: Due to a track circuit fault at #BuonaVista,pls add 5mins travel time from #Redhill to #Dover,train svc is still available.')

