import db
from datetime import datetime as dt, timedelta
from redditPost import redditPost

class subReddit(object):
    
    def __init__(self, subRow):
        self.baseUrl = 'https://oauth.reddit.com/'

        self.name = 'r/' + subRow.lower().rstrip('\n')

        self.currentPostsUrl = self.baseUrl + self.name +'?limit=25'
        self.pastPostsUrl = self.baseUrl + self.name +'/top/?sort=top&t='
        self.pastAverage = 0
        self.posts = []
        self.errorList = []

        # r/all is handled a little differently than the rest
        # the alert is formatted to inclued the source reddit
        # posts are evaluated for being "fast rising"
        if self.name == 'r/all':
            self.isrAll = True
        else:
            self.isrAll = False

        if self.isrAll:
            self.alertRate = 1.25
            self.fastRisingTime = 75
        else:
            self.alertRate = 0.25
            # many subreddits have new posts hit "hot" immediately
            # TODO: make this dynamic per subreddit
            self.fastRisingTime = 0


    def setPastPostsAverage(self, pastPostResp):
        if pastPostResp is None:
            self.errorList.append(self.name + " past chart request is null")
        elif pastPostResp.status_code != 200:
            self.errorList.append(self.name + " past chart request error: status code = " + str(pastPostResp.status_code))
        else:
            totalScore = 0
            count = 0
            for post in pastPostResp.json()['data']['children']:
                data = post['data']
                totalScore += data['score']
                count += 1
        
            if count is 0 and totalScore is 0:
                self.errorList.append(self.name + " - 0 past entries for " + self.name)
            else:
                self.pastAverage = (totalScore / count) * self.alertRate


    def appendNewPosts(self, posts):
        for post in posts:
            pst = redditPost(post['data'])
            pst.srcChart = self.srcChart

            # Check that the subreddit has an average past post score
            # and the current post has a higher score than the average of past posts
            # and the current post is not logged in the database
            if self.pastAverage > 0.0 and int(pst.score) > self.pastAverage and not db.postLogged(pst.name):
                pst.sourceReddit = self.name
                pst.reason = "High Scoring"
                self.posts.append(pst)

            # if this is r/all we also want to check for
            # fast rising posts.
            if self.isrAll:
                fastRisingDT = (dt.now() - timedelta(minutes = self.fastRisingTime))
                if pst.createdTime > fastRisingDT and not (pst.pinned or pst.stickied) and not db.postLogged(pst.name):
                    pst.sourceReddit = self.name
                    pst.reason = "Fast Rising"
                    self.posts.append(pst)


    def setCurrentPosts(self, currPostResp):
        if currPostResp is None:
            self.errorList.append(self.name + " current chart request is null")
        elif currPostResp.status_code != 200:
            self.errorList.append(self.name + " current chart request error: status code = " + str(currPostResp.status_code))
        else:
            self.appendNewPosts(currPostResp.json()['data']['children'])



