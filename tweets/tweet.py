from dataclasses import dataclass
from datetime import datetime
import json

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
