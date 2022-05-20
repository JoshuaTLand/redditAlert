import fileManager
from subReddit import subReddit
from redditApi import redditApi as rdtApi
from discordBot import discordBot
from datetime import datetime as dt
import os

print("[" + str(dt.now()) + "] Starting scan.....")

subredditFile = os.path.join('sublists', 'subList.txt')
alertChannelId = 1234 # <- your discord channel here

# load the lists of subreddits
subList = fileManager.loadSubList(subredditFile)

# send in list of strings of subreddits, get list of finished subreddits in return
# add returned list to a single collection of processed subreddits
redditApi = rdtApi()
subReddits = redditApi.loadSubReddits(subList, alertChannelId)

# Hand of list of subreddits to discord bot for notification
dscrd = discordBot()
dscrd.sendAlerts(subReddits)

print("[" + str(dt.now()) + "] Scan finished")