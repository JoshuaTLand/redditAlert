Setup
-
Required Packages
 - requests
 - psycopg2
 - discord.py

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
