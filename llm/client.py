from openai import OpenAI
from llm.context import context


class Client:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="unused",
        )
        self.context = {"role": "system", "content": context()}
        self.model_warmed_up = False

    def chat_completion(self, messages, stream=False):
        messages = [self.context] + messages

        result = self.client.chat.completions.create(
            model="unused",
            messages=messages,
            stream=stream,
        )

        if not stream:
            self.model_warmed_up = True  # if stream it returns directly

        return result
