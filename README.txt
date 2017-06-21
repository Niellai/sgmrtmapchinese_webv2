How to deploy onto Google cloud platform
https://cloud.google.com/appengine/docs/flexible/python/quickstart


Key words:
-> Contain incident
-> contain no train
-> contain fault
-> contain resumed
-> contain svc

**Short forms that are causing problems in translation**
# hashtags
  - hashtag station names are to be replace within python and store in database
  - Include station number infront of hashtag station name

adding spaces in between numbers and mins. Eg. 10mins -> 10 mins

info -> information
ave -> avenue
blvd -> boulevard
ln -> lane
rd -> road
st -> street
svc -> service
svcs -> services
stn -> station
stns -> stations
b/w -> between
pls -> please
min -> minute
mins -> minutes
ard -> around
mth -> month
mths -> months
NSL -> north south line
EWL -> east west line
CCL -> circle line
DTL -> down town line
TSL -> Thomson line

abbreviation station names
more abbreviation of words need to be recovered
amk -> ang mo kio



**Steps to take for python translation**
1.1 Listen from SMRT Twitter
1.2 Keep original String to variable

2.1 Replace short form or abbs with full words
    (using abb_replacement.json)
2.2 Keep replaced String to variable    
2.2 Lower case entire sentence
2.3 Send String to Google translate to chinese

3.1 Replace station names with full chinese name and add station number
    Replace train line name with full chinese name
3.2 Keep replacement string to variable    

4.1 Store all 3 String to CSV file

5.1 Check if original message contain Key words
5.2 Send full translated chinese sentence to User through FCM
