# -*- coding:utf-8 -*-
#

from flask import *
from rauth.service import OAuth1Service
from rauth.utils import parse_utf8_qsl
import time
import datetime
import pytz

#Twitterの認証をしてくれるオブジェクト
#認証部分は
#http://stackoverflow.com/questions/17512572/rauth-flask-how-to-login-via-twitter
#を参考に
twitter = OAuth1Service(
    consumer_key="",
    consumer_secret="",
    name='twitter',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    base_url='https://api.twitter.com/1.1/')

app = Flask(__name__)
app.secret_key  = '\x14\xc5\x06l-\x83\xcf\x92\xd5k\x11\r2Y\xaer:L\xa0L\xa7\x18\x94\x90'
DEBUG = True


@app.route('/')
def hello():
    return 'Hello Flask.'


@app.route('/twitter/login')
def login():
    
    oauth_callback = url_for('authorized', _external=True)
    params = {'oauth_callback': oauth_callback}

    r = twitter.get_raw_request_token(params=params)
    data = parse_utf8_qsl(r.content)

    session['twitter_oauth'] = (data['oauth_token'],
                                data['oauth_token_secret'])
    return redirect(twitter.get_authorize_url(data['oauth_token'], **params))


@app.route('/twitter/authorized')
def authorized():
    request_token, request_token_secret = session.pop('twitter_oauth')

    # check to make sure the user authorized the request
    if not 'oauth_token' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('index'))

    try:
        creds = {'request_token': request_token,
                'request_token_secret': request_token_secret}
        params = {'oauth_verifier': request.args['oauth_verifier']}
        sess = twitter.get_auth_session(params=params, **creds)
    except Exception, e:
        flash('There was a problem logging into Twitter: ' + str(e))
        return redirect(url_for('index'))
    
    #ここまでで認証はおしまい
    #ここからはつぶやくコード。
    d = datetime.datetime.now(pytz.timezone("Asia/Tokyo")) 
    text = '今、沖縄にいまーす。もうここではサクラが咲いてます←\n'
    text += '※TechnoEdgeからの自動投稿(at %s時%s分%s秒)\n' % (d.hour, d.minute, d.second)
    text += ' #UTHACKs '
    f = open("Sea_kayaking_Zamami_Okinawa.jpg","rb")
    params = { "status": text,
               "lat":"26.233327",
               "long":"127.686804",
               "display_coordinates":"true",
               "format":"json"
            }
    res = sess.post("statuses/update.json", data = params)
    time.sleep(1)
    d = datetime.datetime.now(pytz.timezone("Asia/Tokyo"))
    text = '札幌に来ちゃいました。まだまだ肌寒いです・・・\n'
    text += '※TechnoEdgeからの自動投稿(at %s時%s分%s秒)\n' % (d.hour, d.minute, d.second)
    text += ' #UTHACKs '
    params = { "status": text,
               "lat":"43.062096",
               "long":"141.354376",
               "display_coordinates":"true",
               "format":"json"
               }
    sess.post("statuses/update.json", data = params)
    
    session.clear()
    f.close()
    return 'post succeed!'



if __name__ == '__main__':
     app.run()
