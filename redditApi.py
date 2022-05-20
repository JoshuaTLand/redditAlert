import requests
import time

import fileManager
from subReddit import subReddit

class redditApi:
    def __init__(self):
        # to do
        # securely store credentials
        self.redditUsername = ''
        self.redditPassword = ''

        self.redditBotUsername = ''
        self.redditBotPassword = ''
        
        self.tokenUrl = 'https://www.reddit.com/api/v1/access_token'
        self.token = fileManager.readToken()
        self.headers = {'Authorization': self.token, 'User-Agent': 'redditScript by ' + self.redditUsername}
        self.mark = 0.0
    
    def getToken(self):
        data = {'grant_type': 'client_credentials', 'username': self.redditUsername, 'password': self.redditPassword}
        auth = requests.auth.HTTPBasicAuth(self.redditBotUsername, self.redditBotPassword)
        r = requests.post(self.tokenUrl,
                          data=data,
                          headers={'user-agent': 'rddtScript by ' + self.redditUsername},
                          auth=auth)
        d = r.json()
        tokenVal = 'bearer ' + d['access_token']
    
        fileManager.saveToken(tokenVal)

    def setToken(self):
        self.getToken()
        self.token = fileManager.readToken()
        self.headers = {'Authorization': self.token, 'User-Agent': 'redditScript by ' + self.redditUsername}
        
    
    def getPosts(self, url):
        cycleCount = 1
        while cycleCount <= 5:
            resp = requests.get(url, headers=self.headers)

            # if the token is not set or invalid
            # reload the token and try again
            # otherwise we're done
            if resp.status_code == 401 or resp.status_code == 403:
                self.setToken()
            else:
                break
        
        return resp


    def loadSubReddit(self, subRow):
        subRdt = subReddit(subRow)

        # Low traffic subreddits might not have entries
        # for week or month, so cycle through increasing
        # timespans until we get results
        chartList = ["week", "month", "year"]
        for chart in chartList:
            pastPosts = self.getPosts(subRdt.pastPostsUrl + chart)
            subRdt.srcChart = chart
            if pastPosts.status_code != 404 and len(pastPosts.json()['data']['children']) > 0:
                break

        subRdt.setPastPostsAverage(pastPosts)
        subRdt.setCurrentPosts(self.getPosts(subRdt.currentPostsUrl))

        # Reddit restricts develop accounts to 60 requests per second
        # track the time since the last subreddit was loaded and wait
        # if it's been less than 2 seconds (2 requests per subreddit)
        mark = time.time()
        delta = mark - self.mark
        self.mark = mark
        if delta < 2.0:
            time.sleep(2.0 - delta)

        return subRdt
    
    def loadSubReddits(self, subList, channelId):
        subreddits = []
        for sub in subList:
            subRdt = self.loadSubReddit(sub)
            subRdt.channelId = channelId
            subreddits.append(subRdt)
        return subreddits
    
    
