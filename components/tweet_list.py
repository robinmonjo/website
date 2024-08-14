from fasthtml.common import *

def TweetList(tweets, page):
  return  *[Tweet(t) for t in tweets[:-1]], Tweet(tweets[-1], next_page=(page + 1))

def Tweet(tweet, next_page=None):
  props = {}
  if next_page:
    props = {
      "hx_get": f"/reading_list?page={next_page}",
      "hx_trigger": "revealed",
      "hx_swap": "afterend"
    }

  return Div(
    f"{tweet.user_name} - {tweet.full_text}",
    **props
  )
