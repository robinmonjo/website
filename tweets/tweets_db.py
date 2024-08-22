import sqlite3
import os.path
from datetime import datetime
from tweets.tweet import Tweet

DATABASE = os.path.join("tweets", "tweets.db")


def fetch(page=1, per_page=50):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    offset = (page - 1) * per_page
    query = f"SELECT * FROM tweets ORDER BY created_at DESC LIMIT {per_page} OFFSET {offset}"

    cursor.execute(query)

    # Fetch the records for the current page
    records = cursor.fetchall()
    tweets = [Tweet(*record) for record in records]

    conn.close()

    return tweets


def count():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    result = cursor.execute("SELECT COUNT(*) FROM tweets").fetchone()[0]
    conn.close()
    return result


def last_synchronized_at():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    ts = cursor.execute(
        "SELECT datetime FROM last_synchronized_at WHERE id = 1"
    ).fetchone()[0]
    conn.close()
    return datetime.fromisoformat(ts)
