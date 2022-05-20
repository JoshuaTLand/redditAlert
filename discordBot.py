import redditPost
import subReddit
import discord
import db

class MyClient(discord.Client):
    def __init__(self, subreddits, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subreddits = subreddits

        self.errorChannelId = 1234 # <- your channel Id here

    async def on_ready(self):
        errorChannel = self.get_channel(self.errorChannelId)
        
        for subreddit in self.subreddits:
            subChannel = self.get_channel(subreddit.channelId)

            # try to log each post in the db
            # send the notification if success
            # add to the error list if no
            failedPosts = False
            for post in subreddit.posts:
                if db.logPost(post):
                    await subChannel.send(post.getAlert())
                else:
                    failedPosts = True
           
            # create the failed to save to db error
            if failedPosts:
                subreddit.errorList.append(subreddit.name + " failed to save some posts to the db")

            # send each error to the universal error channel
            for err in subreddit.errorList:
                await errorChannel.send(err)

        await self.close()


class discordBot:

    def sendAlerts(self, subReddits):
        client = MyClient(subReddits)
        client.run("discord auth string here")