import os.path
import json
from llm.client import Client


class Agent:
    def __init__(self, session_key):
        self.session_file = os.path.join("chat_sessions", f"chat_{session_key}.json")
        self.messages = self.load_messages()
        self.client = Client()

    def streamed_answer(self, question):
        self.append_question(question)
        return self.client.chat_completion(self.messages, stream=True)

    def save_answer(self, content):
        self.append_answer(content)
        self.save_messages()

    def append_question(self, q):
        self.messages.append({"role": "user", "content": q})

    def append_answer(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def messages_len(self):
        return len(self.messages)

    def load_messages(self):
        if self.session_exists():
            with open(self.session_file, "r", encoding="utf-8") as f:
                return json.load(f)

        return []

    def save_messages(self):
        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)

    def session_exists(self):
        return os.path.isfile(self.session_file)


def llm_server_up():
    return Client().server_up()
