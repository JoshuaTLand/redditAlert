New V4 Features!
-
 - multiple sublists are now supported. each list is assigned a discord channel that it's corresponding notifications go to
 - sublists have been moved to text files that only require the name of the sub
 - errors are now collected as reddits & posts are evaluated. They are sent out to a single `error` channel via the discord bot
 - charts used for past averages are now handled dynamically. `'week', 'month', 'year'` are tried in order until posts are returned
 - score threshold is static for all subreddits, except r/all which is much higher
 - posts are only checked for fast rising if they originate from r/all
 - a timer now monitors requests to keep under the 60 requests / minute limit while minimizing wait times
 - minor notification tweaks were added such as a link to the origin subreddit in all notifications and a redirect to old.reddit.com for comment links

Setup
-
Required Packages
 - requests
 - psycopg2 (or equivelant library for used db)
 - discord.py

Database
 - the db class current uses psycopg2 to connect to a postgresql db.
 - create the "redditalert" database
 - change `line 35` of the `dbScript` to your user. Save and run the sql file to create the needed table

Usage
 -
 - Create a list of subreddits to check
    - Multiple lists are supported, with each list being associated with a notification channel
    - Lines that start with `#` are considered comments
 - Setup your credentials / channel Ids
   - Add in your redditApi credential to the redditApi.py file
   - Add your discordBot credentials and error channel Id to the discordBot.py file
   - Add your subreddit list files to the sublists folder
   - Set the channel ids for each file in RedditAlert4.py
   - Link lists to the correct channel ID
 - Setup as a recurring cron job
   - Be careful to no create overlapping jobs
   - e.g. it takes 15 minutes to run, but the cronjob starts every 10 minutes
