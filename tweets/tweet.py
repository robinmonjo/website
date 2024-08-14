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
    if self.user_name == HN_USER: return self.clean_hn_link_to_comments()

    return self.text

  def clean_hn_link_to_comments(self):
    return re.sub(r'\s*\(https?://[^\)]+\)', '', self.text)
