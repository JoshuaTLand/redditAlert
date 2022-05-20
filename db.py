import psycopg2

dbUsername = ''
dbPassword = ''

#dbHost = ''
#database = ''

dbHost = 'localhost'
database = 'redditalert'


def GetConn():
    return psycopg2.connect(database = database, user = dbUsername, password = dbPassword, host = dbHost, port = "5432")

def postLogged(name):

    conn = GetConn()
    cur = conn.cursor()
    sql = ("SELECT COUNT(id) FROM posts WHERE name = '"+name+"'")
    cur.execute(sql)
    count = cur.fetchall()[0][0]
    conn.close()

    if count > 0:
        return True
    else:
        return False


def logPost(post):
    try:
        conn = GetConn()
        
        cur = conn.cursor()
        sql = ("INSERT INTO posts (name,author,subreddit,title, url,score,commentcount,sourcereddit,alertreason,postcreatedtime,entrycreatedtime) \
            VALUES ($$" + post.name + "$$, \
            $$" + post.author + "$$, \
            $$" + post.subreddit_name_prefixed + "$$, \
            $$" + post.title + "$$, \
            $$" + post.url + "$$, \
            $$" + post.score + "$$, \
            $$" + post.num_comments + "$$, \
            $$" + post.sourceReddit + "$$, \
            $$" + post.reason + "$$, \
            $$" + post.createdtime + "$$, \
            NOW())")
        cur.execute(sql)
        conn.commit()
        post.logged = True
        
        conn.close()
        return True

    except:
        return False