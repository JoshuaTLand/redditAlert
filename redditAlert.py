import sys
import requests
import time
from datetime import datetime as dt, timedelta
import psycopg2
from twilio.rest import Client

dbHost = 'localhost'

# Your Account SID from twilio.com/console
account_sid = ""
# Your Auth Token from twilio.com/console
auth_token  = ""

def handlePost(post):
    if postWarrantsAlert(post):    
        logPost(post)
        print("[" + str(dt.now()) + "] Alert sent: " + post['title'])


def postWarrantsAlert(post):
    if not postLogged(post['name']):

        createdTime = dt.fromtimestamp(post['created_utc'])
        compareTime = (dt.now() - timedelta(hours = 1, minutes = 15))
    
        if post['score'] > 80000:
            sendAlert(post, "High Scoring")
            return True
    
        if createdTime > compareTime:
            sendAlert(post, "Fast Rising")
            return True

    return False


def sendAlert(post, reason):
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+", 
        from_="+",
        body=reason + ": ["+ post['subreddit_name_prefixed'] + "] " + post['title'] + " (" + post['url'] + ")"
    )

def postLogged(postName):
    conn = psycopg2.connect(database = "redditalert", user = "", password = "", host = dbHost, port = "5432")
    cur = conn.cursor()
    sql = ("SELECT COUNT(id) FROM posts WHERE name = '"+postName+"'")
    cur.execute(sql)
    count = cur.fetchall()[0][0]
    conn.close()

    if count > 0:
        return True
    else:
        return False


def logPost(post):
    createdtime = dt.fromtimestamp(post['created_utc']).strftime("%m/%d/%Y, %H:%M:%S");
    conn = psycopg2.connect(database = "redditalert", user = "", password = "", host = dbHost, port = "5432")
    cur = conn.cursor()
    sql = ("INSERT INTO posts (name,author,subreddit,title, url,score,commentcount,postcreatedtime,entrycreatedtime) \
      VALUES ($$" + str(post['name']) + "$$, \
      $$" + str(post['author']) + "$$, \
      $$" + str(post['subreddit_name_prefixed']) + "$$, \
      $$" + str(post['title']) + "$$, \
      $$" + str(post['url']) + "$$, \
      $$" + str(post['score']) + "$$, \
      $$" + str(post['num_comments']) + "$$, \
      $$" + str(createdtime) + "$$, \
      NOW())")
    cur.execute(sql)
    conn.commit()
    conn.close()


def getToken():
    baseUrl = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': '', 'password': ''}
    auth = requests.auth.HTTPBasicAuth('redditAppId', 'redditAppKey')
    r = requests.post(baseUrl + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': 'reddit_user_agent_format'},
                      auth=auth)
    d = r.json()
    tokenVal = 'bearer ' + d['access_token']
    
    with open('token', 'w') as f:
        f.truncate()
        f.write(tokenVal)

    return tokenVal


def loadToken():
    tokenVal = '' 
    with open('token', 'r') as f:
         tokenVal = f.readline()

    return tokenVal

#########################
#      Main Loop        #
#########################
token = loadToken()
baseUrl = 'https://oauth.reddit.com'
requestUrl = baseUrl + '/r/all?limit=25'
headers = {'Authorization': token, 'User-Agent': 'reddit_user_agent_format'}
completed = False

try:
    while not completed:
  
        response = requests.get(requestUrl, headers=headers)

        if response.status_code == 200:
            for post in response.json()['data']['children']:
                handlePost(post['data'])
        
            completed = True

        elif response.status_code == 401:
            print("[" + str(dt.now()) + "] Refreshing token")
            token = getToken()
            headers = {'Authorization': token, 'User-Agent': 'reddit_user_agent_format'}

        else:
            print("[" + str(dt.now()) + "] Unexpected status - " + str(response.status_code))
            completed = True

    print("[" + str(dt.now()) + "] Finished scan")

except Exception as e:
    print("[" + str(dt.now()) + "] Scan error: " + str(e))