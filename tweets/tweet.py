from dataclasses import dataclass
from datetime import datetime
import json
import re

HN_USER = "Hacker News 50"

@dataclass
class Tweet:
  id: str
  created_at: datetime
  user_name: str
  text: str
  thumbnail_title: str
  thumbnail_url: str
  urls: str
  full_text: str

  def parsed_urls(self):
    return json.loads(self.urls)

  def cleaned_text(self):
    result = self.replace_tracked_url(self.text)

    if self.user_name == HN_USER: return self.clean_hn_link_to_comments(result)

    return result

  def replace_tracked_url(self, text):
    new_text = text
    for url in self.parsed_urls():
      new_text = new_text.replace(url["url"], url["expanded_url"])

    return new_text

  def clean_hn_link_to_comments(self, text):
    urls = self.parsed_urls()

    if len(urls) > 1 and urls[-1]["expanded_url"].startswith("https://news.ycombinator.com"):
      return re.sub(r'\s*\(https?://[^\)]+\)', '', text)

    return text
