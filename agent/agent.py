import os.path
import json
from agent.llm_singleton import LlmSingleton


class Agent:
    def __init__(self, session_key):
        self.session_file = os.path.join("chat_sessions", f"chat_{session_key}.json")
        self.messages = self.load_messages()
        self.llm = LlmSingleton()

    def model_warmed_up(self):
        return self.llm.model_warmed_up

    def streamed_answer(self, question):
        self.append_question(question)
        return self.llm.chat_completion(self.messages, stream=True)

    def save_answer(self, content):
        self.append_answer(content)
        self.save_messages()
        self.llm.model_warmed_up = True

    def answer(self, question):
        self.append_question(question)
        answer = self.llm.chat_completion(self.messages)
        content = answer["choices"][0]["message"]["content"]
        self.save_answer(content)
        return content

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
