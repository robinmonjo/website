from dataclasses import dataclass
from datetime import datetime
import json

HN_USER = "Hacker News 50"

# pylint: disable=too-many-instance-attributes


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
    media: str
    user_profile_image_url: str
    user_screen_name: str

    def parsed_urls(self):
        return json.loads(self.urls)

    def parsed_media(self):
        return json.loads(self.media)

    def parsed_text(self):
        parts = []
        i = 0

        for url in self.parsed_urls():
            indices = url["indices"]

            parts.extend(
                [
                    {"type": "text", "content": self.text[i : indices[0]]},
                    {
                        "type": "url",
                        "display": url["display_url"],
                        "href": url["expanded_url"],
                    },
                ]
            )
            i = indices[1]

        parts.append({"type": "text", "content": self.text[i : len(self.text)]})

        return parts

    def created_at_datetime(self):
        return datetime.fromisoformat(self.created_at)

    def url(self):
        return f"{self.user_profile_url()}/status/{self.id}"

    def user_profile_url(self):
        return f"https://x.com/{self.user_screen_name}"
