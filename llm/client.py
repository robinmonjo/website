from openai import OpenAI
import requests
from llm.context import context

SERVER_URL = "http://localhost:8000"


class Client:
    def __init__(self):
        self.client = OpenAI(
            base_url=f"{SERVER_URL}/v1",
            api_key="unused",
        )
        self.context = {"role": "system", "content": context()}

    def chat_completion(self, messages, stream=False):
        messages = [self.context] + messages

        return self.client.chat.completions.create(
            model="unused",
            messages=messages,
            stream=stream,
            extra_body={"cache_prompt": True},
        )

    def tokenize(self, text):
        data = {"content": text}
        response = requests.post(f"{SERVER_URL}/tokenize", json=data)
        return response.json()["tokens"]

    def initial_prompt_size(self):
        return len(self.tokenize(context()))
