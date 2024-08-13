import sqlite3
import os.path
from tweets.tweet import Tweet

DATABASE = os.path.join("tweets", "tweets.db")

def fetch_tweets(page=1, per_page=50):
  conn = sqlite3.connect(DATABASE)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  offset = (page - 1) * per_page
  query = f"SELECT * FROM tweets LIMIT {per_page} OFFSET {offset}"

  cursor.execute(query)

  # Fetch the records for the current page
  records = cursor.fetchall()
  tweets = [Tweet(*record) for record in records]

  conn.close()

  return tweets


