from fasthtml.common import *
from components.title import title
from components.brand_link import brand_link
from components.fa import fa
from components.education_card import education_card
from components.favicon_link import favicon_link
from components.atb import atb
from components.home_btn import home_btn
from components.chat_box import chat_box, chat_input, user_chat_message, assistant_chat_message, chat_message_chunk, chat_bar, chat_box_js
from datetime import datetime
from agent.agent import Agent
from asyncio import sleep
import time
import json
import uuid

hdrs = (
  MarkdownJS(),
  HighlightJS(langs=[]),
  Script(src="https://kit.fontawesome.com/e68e45d4cb.js", crossorigin="anonymous"),
  Script(chat_box_js()),
  Style(".container { max-width: 800px; }"),
  Style("body { min-height: 100vh; display: flex; flex-direction: column; }"),
  favicon_link("👋")
)

SESSION_EXPIRATION_DELAY = 2 * 60 * 60 # 2 hours

def set_session(session):
  session.setdefault("key", str(uuid.uuid4()))
  session.setdefault("ts", str(time.time()))

def before(req, session):
  if not session:
    set_session(session)
  elif time.time() - float(session["ts"]) > SESSION_EXPIRATION_DELAY:
    session.clear()
    set_session(session)

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/content/.*', r'.*\.css'])

app,rt = fast_app(hdrs=hdrs, ws_hdr=True, debug=True, before=bware)

@rt("/")
def get(req):
  return layout(
    Div(
      read_md("catch_phrase"),
      cls="marked",
      style="font-size: 1.5em; text-align: center;"
    ),
    home_btn("briefcase", "Work Experience", "/resume"),
    home_btn("school", "Education", "/education"),
    home_btn("comment", "Ask Phi", "/ask_llm"),
    style="align-items: center; display: flex; flex-direction: column; gap: 20px"
  )

@app.ws("/messages_ws")
async def messages_ws(msg:str, session_key:str, send):
  # disable input
  await send(chat_bar(enabled=False))

  agent = Agent(session_key)
  output = agent.streamed_answer(msg)
  messages_len = agent.messages_len()

  # return user message directly
  await send(user_chat_message(msg, messages_len))

  # clear the input
  await send(chat_input())

  next_message_idx = messages_len + 1

  # send an empty message from the agent
  waiting_message = "🤔..." if agent.model_warmed_up() else "Please wait, I'm waking up 🥱. Will answer in a few seconds..."
  await send(assistant_chat_message(waiting_message, next_message_idx))

  await sleep(0.0) # flush the event loop ?? seems weird

  content = ""
  for chunk in output:
    delta = chunk["choices"][0]["delta"]
    if "content" in delta:
      await send(chat_message_chunk(delta["content"], next_message_idx, clear=(content == "")))
      await sleep(0) # flush the event loop ?? seems weird
      content += delta["content"]

  agent.save_answer(content)

  # re-enable input
  await send(chat_bar())


@rt("/resume")
def get(req):
  return layout(
    read_md("resume"),
    cls="marked"
  )

@rt("/education")
def get(req):
  with open(f"content/education.json", "r") as f: content = json.load(f)
  return layout(
    education_card(item) for item in content
  )

@rt("/ask_llm")
def get(session, req):
  messages = Agent(session["key"]).messages
  return layout(
    chat_box(messages, session["key"])
  )

@rt("/{fname:path}.pdf")
async def get(fname:str): return FileResponse(f'{fname}.pdf')

def layout(*args, **kwargs):
  return Title("R. Monjo"), nav(), Main(
    Div(*args, **kwargs),
    cls="container"
  ), footer()

def nav():
  return Header(
    Nav(
      Ul(
        Li(A(title("Robin Monjo"), href="/", style="text-decoration: none;"))
      ),
      Ul(
        Li(A("Work", href="/resume", cls="contrast", style="font-size: 1.25em;")),
        Li(A("Education", href="/education", cls="contrast", style="font-size: 1.25em;")),
        Li(A("Ask Phi", href="/ask_llm", cls="contrast", style="font-size: 1.25em;")),
        Li("|", style="color: lightgrey"),
        Li(brand_link("linkedin", "www.linkedin.com/in/robin-monjo-b1384a59/")),
        Li(brand_link("github", "github.com/robinmonjo")),
        Li(brand_link("stack-overflow", "stackoverflow.com/users/251552/rmonjo"))
      )
    ),
    cls="container",
  )

def footer():
  return Footer(
    Hr(),
    Div(
      Small("Built with",
        atb(
          Img(src="/content/fasthtml_logo.svg", alt="FastHTML", width="60"),
          href="https://www.fastht.ml/",
          style="text-decoration: none;"
        ),
        "-",
        atb(
          "Report an issue",
          href="https://github.com/robinmonjo/website/issues"
        ),
        "-",
        atb(
          "See code",
          href="https://github.com/robinmonjo/website"
        )
      ),
      Small(
        f"© {datetime.now().year} Robin Monjo",
        style="margin-left: auto;"
      ),
      style="display: flex;"
    ),
    cls="container", style="margin-top: auto;"
  )

def read_md(file):
  with open(f"content/{file}.md", "r") as f: content = f.read()
  return content

serve()
