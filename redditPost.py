from datetime import datetime as dt

class redditPost:
    def __init__(self, post):
        self.subreddit_name_prefixed = post['subreddit_name_prefixed'].lower()
        self.title = str(post['title']).replace("$$", "($)($))")
        self.url = post['url']
        self.createdtime = str(dt.fromtimestamp(post['created_utc']).strftime("%m/%d/%Y, %H:%M:%S"));
        self.name = str(post['name'])
        self.author = str(post['author'])
        self.score = str(post['score'])
        self.num_comments = str(post['num_comments'])
        self.createdTime = dt.fromtimestamp(post['created_utc'])
        self.pinned = post['pinned']
        self.stickied = post['stickied']
        self.logged = False
        self.sourceReddit = ""
    
        if self.title[0] == "$" or self.title[-1] == "$":
            self.title = "[" + self.title + "]"

        if "comments" in self.url:
            self.url = self.url.replace('www.reddit.com', 'old.reddit.com')

    def getAlert(self):
        #format the text of the reddit as a link to that reddit
        redditText = self.subreddit_name_prefixed
        reasonText = self.reason
    
        # Format text for r/all posts
        if self.sourceReddit !=  self.subreddit_name_prefixed:
            redditText = self.sourceReddit + " ("+ self.subreddit_name_prefixed + ")"

        # Format reason for non week subreddits
        if self.srcChart != 'week':
            reasonText =  self.reason + " (" + self.srcChart + ")"

        bodyText = reasonText + " - " + redditText + " (" + self.author + ")\n" + self.title + "\n<https://old.reddit.com/" + self.subreddit_name_prefixed +">\n" + self.url

        return bodyText
    