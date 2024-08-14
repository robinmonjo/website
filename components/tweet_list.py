from fasthtml.common import *
from components.atb import Atb

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

  elements = []
  for item in tweet.parsed_text():
    if item["type"] == "text":
      elements.append(Span(item["content"]))
    else:
      elements.append(Atb(item["display"], href=item["href"]))

  return Article(
    P(f"{tweet.user_name} - {tweet.created_at_datetime().strftime("%d %b. %Y")}"),
    P(*elements, style="word-break: break-all;"),
    Small(Atb("see tweet", href=tweet.url())),
    **props
  )
