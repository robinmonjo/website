from openai import OpenAI
from llm.context import context


class Client:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="unused",
        )
        self.context = {"role": "system", "content": context()}

    def chat_completion(self, messages, stream=False):
        messages = [self.context] + messages

        return self.client.chat.completions.create(
            model="unused",
            messages=messages,
            stream=stream,
            extra_body={"cache_prompt": True}
        )
