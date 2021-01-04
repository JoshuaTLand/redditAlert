import sys
import requests
import time
from datetime import datetime as dt, timedelta
import psycopg2
from twilio.rest import Client
import os.path



scoreLim = 0.5

subList = { 

    "all":("day", (75, 0.85)), 
    #"[subreddit]":("[chart]", ([MinutesForFastRising, PercentOfAvgChartScoreForHighScoring)),
    
}

# Your Account SID from twilio.com/console
account_sid = ""
# Your Auth Token from twilio.com/console
auth_token  = ""


##
##------Reddit Token------------------
##
def getToken():
    baseUrl = 'https://www.reddit.com/'
    data = {'grant_type': 'password', 'username': '', 'password': ''}
    auth = requests.auth.HTTPBasicAuth('', '')
    r = requests.post(baseUrl + 'api/v1/access_token',
                      data=data,
                      headers={'user-agent': ''},
                      auth=auth)
    d = r.json()
    tokenVal = 'bearer ' + d['access_token']
    
    with open('token', 'w') as f:
        f.truncate()
        f.write(tokenVal)

    return tokenVal


def loadToken():
    tokenVal = '' 

    if not os.path.isfile('token'):
        getToken()

    with open('token', 'r') as f:
         tokenVal = f.readline()

    return tokenVal


##
##------Post Logging / Alert------------------
##
def postLogged(postName):

    conn = psycopg2.connect(database = "", user = "", password = "", host = "", port = "")
    cur = conn.cursor()
    sql = ("SELECT COUNT(id) FROM posts WHERE name = '"+postName+"'")
    cur.execute(sql)
    count = cur.fetchall()[0][0]
    conn.close()

    if count > 0:
        return True
    else:
        return False


def logPost(post, reddit, reason):

    createdtime = dt.fromtimestamp(post['created_utc']).strftime("%m/%d/%Y, %H:%M:%S");
    conn = psycopg2.connect(database = "", user = "", password = "", host = "", port = "")
    cur = conn.cursor()
    sql = ("INSERT INTO posts (name,author,subreddit,title, url,score,commentcount,sourcereddit,alertreason,postcreatedtime,entrycreatedtime) \
      VALUES ($$" + str(post['name']) + "$$, \
      $$" + str(post['author']) + "$$, \
      $$" + str(post['subreddit_name_prefixed']) + "$$, \
      $$" + str(post['title']) + "$$, \
      $$" + str(post['url']) + "$$, \
      $$" + str(post['score']) + "$$, \
      $$" + str(post['num_comments']) + "$$, \
      $$" + "r/" + reddit + "$$, \
      $$" + reason + "$$, \
      $$" + str(createdtime) + "$$, \
      NOW())")
    cur.execute(sql)
    conn.commit()
    conn.close()


def sendAlert(post, reddit, reason):

    print("[" + str(dt.now()) + "]\tSending alert for /r/" + reddit + " post \"" + post['title'] + "\"")
    
    redditText = post['subreddit_name_prefixed']
    
    # Format text for r/all posts
    if "r/" + reddit.lower() !=  post['subreddit_name_prefixed'].lower():
        redditText = "r/" + reddit + " ("+ post['subreddit_name_prefixed'] + ")"

    bodyText = reason + " - " + redditText + "\n" + post['title'] + "\n" + post['url']

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="", 
        from_="",
        body=bodyText
    )


##
##------Reddit Functions------------------
##
def getAvgScore(pastChart):

    totalScore = 0
    count = 0

    for post in pastChart.json()['data']['children']:
        data = post['data']
        totalScore += data['score']
        count += 1

    return totalScore / count


def evaluateReddit(reddit, pastChart, currentPosts, riseLimit, scorePercent):
    
    fastRisingDT = (dt.now() - timedelta(minutes = riseLimit))

    # go for 90% of average
    pastAvg = getAvgScore(pastChart) * scorePercent

    for postData in currentPosts.json()['data']['children']:
        post = postData['data']

        if not postLogged(post['name']):

            if post['score'] > pastAvg:
                sendAlert(post, reddit, "High Scoring")
                logPost(post, reddit, "High Scoring")
                continue
            
            createdTime = dt.fromtimestamp(post['created_utc'])
            if createdTime > fastRisingDT and not (post['pinned'] or post['stickied']):
                sendAlert(post, reddit, "Fast Rising")
                logPost(post, reddit, "Fast Rising")
                continue



#########################
#      Main Loop        #
#########################
token = loadToken()
baseUrl = 'https://oauth.reddit.com'
headers = {'Authorization': token, 'User-Agent': ''}

for reddit, (topChart, (riseLimit, scorePercent)) in subList.items():
    try:
        while True:

            # Gather requests for reference chart and hot chart
            #--------------------------------------------------
            requestUrl = baseUrl + '/r/'+reddit+'/top/?sort=top&t='+topChart
            pastChart = requests.get(requestUrl, headers=headers)

            if pastChart.status_code == 401:
                print("[" + str(dt.now()) + "] Refreshing token")
                token = getToken()
                headers = {'Authorization': token, 'User-Agent': ''}
                continue

            requestUrl = baseUrl + '/r/'+reddit+'?limit=25'
            currentPosts = requests.get(requestUrl, headers=headers)

            if currentPosts.status_code == 401:
                print("[" + str(dt.now()) + "] Refreshing token")
                token = getToken()
                headers = {'Authorization': token, 'User-Agent': ''}
                continue


            # Check to make sure we got a successful response
            #-------------------------------------------------
            if pastChart.status_code != 200:
                print("[" + str(dt.now()) + "] Unexpected status - " + str(pastWeek.status_code))
                continue

            if currentPosts.status_code != 200:
                print("[" + str(dt.now()) + "] Unexpected status - " + str(currentPosts.status_code))
                continue

           
            # Evauluate subreddit
            #--------------------------------------------------
            evaluateReddit(reddit, pastChart, currentPosts, riseLimit, scorePercent)

            break

    except Exception as e:
        print("[" + str(dt.now()) + "] Scan error: " + str(e))

    time.sleep(0.5)

print("[" + str(dt.now()) + "] Finished scan")
