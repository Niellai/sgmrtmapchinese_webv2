
# coding: utf-8

# In[5]:

import json

# Import Firebase Cloud Message
from pyfcm import FCMNotification


# In[6]:

class FCM:
    
    FCM_API_KEY = 'AAAA7txeP1w:APA91bGgt2_t3W3__9IG0uGrJek4PsDES3_IWNv22x9sa41HVufRNYIrHZpSq8L02VPOQxBU-qz1ewPdIPxJh8fGNoJ6UM1NALy0jGKJ3S1hGq3ug-65Jc8LEV6nZVPGuGfDX3wfZIRx'
    FCM_TOPICS = 'SMRT_UPDATES'

    # Send json data to fcm in default topic
    def send_default(self, jsondata):    
        try:
            push_service = FCMNotification(api_key=FCM.FCM_API_KEY)
            result = push_service.notify_topic_subscribers(
                data_message = jsondata,
                topic_name = FCM.FCM_TOPICS)
            print(result)
        except Exception as e:
            print("fcm_topic error: {}".format(e)) 
    
    # Send json data to fcm in given topic
    def send_topic(self, jsondata, topic):    
        try:
            push_service = FCMNotification(api_key=FCM.FCM_API_KEY)
            result = push_service.notify_topic_subscribers(
                data_message = jsondata,
                topic_name = topic)
            print(result)
        except Exception as e:
            print("fcm_topic error: {}".format(e)) 


# In[13]:

'''
Example / Test methods
'''
# sendData = {}
# # sendData['text'] = "[东西地铁线]更新：请从#政府大厦到＃杜佛额外10分钟的旅行时间。我们正在努力恢复服务。"
# sendData['text'] = "testing message"
# sendData['timestamp_ms'] = 1498050580169

# # sendData['text'] = json.dumps(sendData, ensure_ascii=False)

# fcm = FCM()
# fcm.send_topic(sendData, 'SMRT_UPDATES')

