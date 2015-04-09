# -*- coding:utf-8 -*-                                                                                                                                            

from requests_oauthlib import OAuth1Session
import json
import serial
import time
import re

#Twitter APIの利用に必要な定数。（セキュリティ上の観点から省略）                                                                                                                                                   
oath_key_dict = {
    "consumer_key": "",
    "consumer_secret": "",
    "access_token": "",
    "access_token_secret": ""
}

#APIへの認証をする
def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )
    return oath

#screen_nameからその人のつぶやいたツイートを取得する
def tweet_search_by_screen_name(screen_name, oath_key_dict):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
    params = {
        "screen_name": unicode(screen_name),
        "result_type": "recent",
        "count": "15"
        }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    tweets = json.loads(responce.text)
    return tweets



#今回のメイン部分
#screen_nameに指定したユーザーからの新規のツイートに反応しLEDをつけたり消したり
def enlight_by_twitter(screen_name,oath_key_dict):
    ser = serial.Serial('/dev/tty.usbmodem1421', 9600) #arduinoとのシリアル通信開始
    newest_tweets = tweet_search_by_screen_name(screen_name,oath_key_dict)
    since_id = newest_tweets[0]["id"] #最新ツイートのid
    while(1):
        tweets = tweet_search_by_screen_name(screen_name,oath_key_dict)
        newest_id = tweets[0]["id"]
        print "uthacks:新しいツイートある〜？"
        if(newest_id>since_id):
            print "Twitter:あるよ〜"
            since_id=newest_id
            text = tweets[0]["text"] #ツイートの中身
            print text
            #以下ツイートの中身に応じてシリアル通信
            if(("on" in text)  or (u"オン" in text) or (u"点け" in text) or (u"つけ" in text)):
                if((u"青" in text) or (u"あお" in text) or ("blue" in text)):
                    ser.write("q")
                if((u"赤" in text) or (u"あか" in text) or ("red" in text)):
                    ser.write("o")
            if(("off" in text) or (u"オフ" in text) or (u"けし" in text) or (u"消し" in text)):
                if((u"青" in text) or (u"あお" in text) or ("blue" in text)):
                    ser.write("r")
                if((u"赤" in text) or (u"あか" in text) or ("red" in text)):
                    ser.write("p")
        else:
            print "Twitter:ないよ〜"
            
        time.sleep(6) #Twitterの制限を回避するため問い合わせは6秒に１回
    ser.close()
    
                
    


########以後関係ないけど、試しに書いてみたコード #####################################
#リプを飛ばすコード
def post_rep(tweet,oath_key_dict,text):
    url = "https://api.twitter.com/1.1/statuses/update.json"
    tweet_text = '@'+tweet[u'user'][u'screen_name']+" "+text+" "+str(tweet[u'id'])
    print str(tweet[u'id'])
    params = { "status": tweet_text,"in_reply_to_status_id": str(tweet[u'id'])}
    oath = create_oath_session(oath_key_dict)
    responce = oath.post(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
    else:
        print "post successed"

#普通のTwitter検索
def tweet_search(search_word, oath_key_dict):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": search_word.decode("utf-8"),
        "result_type": "recent",
        "count": "100"
        }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print "Error code: %d" %(responce.status_code)
        return None
    tweets = json.loads(responce.text)
    return tweets

