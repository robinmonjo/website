#!/usr/bin/env python
# coding: utf-8

# ### Build liked tweets database
#
# Usage:
# 1 - Use edit this cookie extension to save x.com cookies to `raw_x_cookies.json`
# 2 - Run all the cells
#
# This will create a sqlite database.
#
# Note: deleted liked already synchronized won't be removed from the database, to do so, perform a full re-sync by deleting tweets.db file before running all the cells

# In[1]:


from twikit import Client
import json

async def main():

    # In[2]:


    with open("raw_x_cookies.json", "r") as file:
        cookies = json.load(file)


    # Convert cookie to twikit format

    # In[3]:


    result = {}
    for item in cookies:
        name = item.get("name")
        value = item.get("value")
        if name and value:
            result[name] = value

    with open("x_cookies.json", "w") as file:
        json.dump(result, file, indent=4)


    # In[4]:


    client = Client("en-US")
    client.load_cookies("x_cookies.json")


    # In[5]:


    user = await client.get_user_by_screen_name("b0baille")


    # In[6]:


    # tweets = await user.get_tweets("Likes", 20)
    # for t in tweets:
    #     print(f"{t.media} - {t.media and len(t.media)}")


    # In[7]:


    import sqlite3

    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("../tweets/tweets.db")

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table only if it doesn't already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tweets (
            id TEXT PRIMARY KEY,
            created_at DATETIME NOT NULL,
            user_name TEXT NOT NULL,
            text TEXT NOT NULL,
            thumbnail_title TEXT,
            thumbnail_url TEXT,
            urls TEXT,
            full_text TEXT NOT NULL,
            media TEXT,
            user_profile_image_url TEXT NOT NULL,
            user_screen_name TEXT NOT NULL
        )
    """)

    # Commit the changes
    conn.commit()


    # In[8]:


    def import_tweet(tweet, count):
        # check if tweet already in database
        cursor.execute("SELECT COUNT(*) FROM tweets WHERE id = ?", (tweet.id,))
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"Tweet {tweet.id} already in database")
            return False

        cursor.execute("""
        INSERT INTO tweets (id, created_at, user_name, text, thumbnail_title, thumbnail_url, urls, full_text, media, user_profile_image_url, user_screen_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tweet.id,
            tweet.created_at_datetime,
            tweet.user.name,
            tweet.text,
            tweet.thumbnail_title,
            tweet.thumbnail_url,
            json.dumps(tweet.urls),
            tweet.full_text,
            json.dumps(tweet.media),
            tweet.user.profile_image_url,
            tweet.user.screen_name
            )
        )

        return True


    # In[9]:


    async def iterate_tweets(fn):
        tweets = await user.get_tweets("Likes", 100)

        count = 1
        for t in tweets:
            if fn(t, count):
                count += 1
            else:
                return

        while True:
            tweets = await tweets.next()
            if not tweets: return

            for t in tweets:
                if fn(t, count):
                    count += 1
                else:
                    return


    # In[10]:


    def count_tweets():
        cursor.execute("SELECT COUNT(*) FROM tweets")
        return cursor.fetchone()[0]


    # In[11]:


    count_before = count_tweets()
    print(f"{count_before} entries before import")

    await iterate_tweets(import_tweet)

    conn.commit()

    count_after = count_tweets()
    print(f"{count_after} entries after import")
    print(f"{count_after - count_before} tweets imported")


    # In[12]:


    from datetime import datetime


    # In[13]:


    # Create a table only if it doesn't already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS last_synchronized_at (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            datetime TEXT
        )
    """)

    ts = datetime.now()
    cursor.execute("""
        INSERT OR REPLACE INTO last_synchronized_at (id, datetime) VALUES (1, ?)
    """, (ts,))

    # Commit the changes
    conn.commit()


    # In[14]:


    cursor.execute("SELECT datetime FROM last_synchronized_at WHERE id = 1")
    ts = cursor.fetchone()[0]
    print(f"Last updated at: {ts}")


    # In[15]:


    conn.close()


import asyncio

asyncio.run(main())
