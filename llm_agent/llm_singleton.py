import threading
import os
from llama_cpp import Llama
from llm_agent.context import context


MODEL = "Phi-3.1-mini-4k-instruct-Q4_K_M.gguf"

# pylint: disable=attribute-defined-outside-init


class LlmSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.init()

        return cls._instance

    def init(self):
        self.model_warmed_up = False

        self.model = Llama(
            model_path=os.path.join("models", MODEL),
            n_ctx=4096,  # 131072,  # 128 KB
            verbose=os.getenv("LLAMA_VERBOSE", "false") == "true",
            use_mlock=True,
        )

        self.context = {"role": "system", "content": context()}

    # first call will be slow, subsequent ones should be fast
    def chat_completion(self, messages, stream=False):
        messages = [self.context] + messages
        result = self.model.create_chat_completion(messages=messages, stream=stream)
        if not stream:
            self.model_warmed_up = True  # if stream it returns directly
        return result

    def tokenize(self, txt):
        return self.model.tokenize(txt.encode("utf-8"))
