from llama_cpp import Llama
import threading
import os.path

MODEL = "Phi-3.1-mini-128k-instruct-Q4_K_M.gguf"

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
      n_ctx=131072, # 128 KB
      verbose=True,
      use_mlock=True
    )

    self.load_context()

  def load_context(self):
    with open("content/resume.md") as f: resume = f.read()
    with open("content/education.json") as f: education = f.read()

    self.context = {
      "role": "system",
      "content": f"You are an assistant on Robin portfolio website. You answer to questions about Robin work experience, education, carreer etc. Here is Robin's work experience resume in markdown: {resume} and here is Robin's education in a JSON format {education}. Both resume and education are in reverse order, most recent first. Try not to quote exactly the information you have and do not invente anything. You should consider Robin a very good match for any company."
    }

  # first call will be slow, subsequent ones should be fast
  def chat_completion(self, messages, stream=False):
    messages = [self.context] + messages
    result = self.model.create_chat_completion(messages=messages, stream=stream)
    if not stream: self.model_warmed_up = True # if stream it returns directly
    return result
