from fasthtml.common import *
from components.atb import Atb
from components.fa import Fa

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

  return Article(
    Header(tweet),
    Content(tweet),
    **props
  )

def Header(tweet):
  return Div(
    Img(src=tweet.user_profile_image_url, width=30, style="border-radius: 30px"),
    Atb(tweet.user_name, href=tweet.user_profile_url(), cls="contrast", style="text-decoration: none;"),
    Small(tweet.created_at_datetime().strftime("%d %b. %Y"), style="color: grey;"),
    Small(Atb("see tweet", Fa("arrow-up-right-from-square", size="xs"), href=tweet.url()), style="margin-left: auto;"),
    style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;"
  )

def Content(tweet):
  content = P(*ParsedTextElements(tweet), style="word-break: break-all; margin-bottom: 0"),
  return ContentWithThumbnail(tweet, content) if tweet.thumbnail_url else content

def ContentWithThumbnail(tweet, content):
  return Div(
    Img(src=tweet.thumbnail_url, alt=tweet.thumbnail_title, style="max-width: 90px;"),
    content,
    style="display: flex; align-items: center; gap: 10px;"
  )


def ParsedTextElements(tweet):
  elements = []
  for item in tweet.parsed_text():
    if item["type"] == "text":
      elements.append(Span(item["content"]))
    else:
      elements.append(Atb(item["display"], href=item["href"]))

  return elements
