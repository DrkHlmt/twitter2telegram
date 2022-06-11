import tweepy
import requests
import os
import sys
import time
import datetime

#Twitter related tokens, requires a twitter dev account
bearer_token = ""
client = tweepy.Client(bearer_token=bearer_token)
token = ''
twitter_id= ''
#Telgram chat id is a negative integer, I used telegram web application to retrieve it
telegram_chat_id = ''

def getTweets(userID,lastID):
    twts = client.get_users_tweets(id=userID,since_id=lastID,exclude=['retweets'],tweet_fields=['created_at'],max_results=100)
    return twts
def sendTelegram(message):
      write_message2file(message,'/path/to/output.txt')
      url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + telegram_chat_id + "&text=" + message
      results = requests.get(url_req)
      print(results.json())
def write_message2file(message,filename):
        with open(filename,'a') as filewrite:
                filewrite.write(str(message)+"\n")
def readOldest(filename):
    with open(filename,'r') as fileread:
        return fileread.read()
def replaceOldest(filename,new):
    with open(filename,'w') as filewrite:
        filewrite.write(new)

if __name__ == '__main__':
    oldest=readOldest("/path/to/oldest.txt")
    fetched=getTweets(twitter_id,int(oldest))
    meta = fetched.meta
    if (meta['result_count'] > 0):
        print(meta['newest_id'])
        tweets = fetched.data
        replaceOldest("/path/to/oldest.txt",meta['newest_id'])
        for tweet in reversed(tweets):
            sendTelegram("Created: "+str(tweet.created_at)+"\n")
            time.sleep(2)
            sendTelegram(str(tweet.text))
            time.sleep(30)
