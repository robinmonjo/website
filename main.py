from asyncio import sleep
import os
import time
import json
import uuid
from fasthtml.common import *
from components.nav_bar import NavBar
from components.education_card import EducationCard
from components.favicon_link import FaviconLink
from components.page_footer import PageFooter
from components.home_btn import HomeBtn
from components.chat_box import (
    ChatBox,
    ChatInput,
    UserChatMessage,
    AssistantChatMessage,
    ChatMessageChunk,
    ChatBar,
)
from components.home_text import HomeText
from components.tweet_list import TweetList, TweetListHeader
from llm.agent import Agent
from tweets import tweets_db


hdrs = (
    MarkdownJS(),
    HighlightJS(langs=[]),
    Script(src="https://kit.fontawesome.com/e68e45d4cb.js", crossorigin="anonymous"),
    Style("@media (min-width: 1024px) { .container { max-width: 800px; } }"),
    Style("body { min-height: 100vh; display: flex; flex-direction: column; }"),
    FaviconLink("👋"),
)

SESSION_EXPIRATION_DELAY = 2 * 60 * 60  # 2 hours


def set_session(session):
    session.setdefault("key", str(uuid.uuid4()))
    session.setdefault("ts", str(time.time()))


def reset_session(session):
    session.clear()
    set_session(session)


def before(req, session):
    del req

    if not session:
        set_session(session)
    elif time.time() - float(session["ts"]) > SESSION_EXPIRATION_DELAY:
        reset_session(session)


bware = Beforeware(before, skip=[r"/favicon\.ico", r"/content/.*", r".*\.css"])

dev_env = os.getenv("PYTHON_ENV", "development") == "development"

app, rt = fast_app(
    hdrs=hdrs,
    ws_hdr=True,
    debug=dev_env,
    live=dev_env,
    before=bware,
    htmlkw={"lang": "en"},
)


@rt("/")
def get(req):
    return Layout(
        HomeText(
            Img(
                src=f"/content/profile_pictures/picture1.jpeg",
                alt="profile picture",
                width="130",
                style="border-radius: 130px; margin-bottom: 20px;"
            ),
            Div(
                read_md("catch_phrase"),
                cls="marked",
            ),
        ),
        Div(
            HomeBtn("briefcase", "Work Experience", "/resume"),
            HomeBtn("school", "Education", "/education"),
            HomeBtn("comment", "Ask Phi", "/ask_llm"),
            HomeBtn("book", "Reading List", "/reading_list"),
            style="display: flex; justify-content: center; gap: 30px; margin-top: 60px;",
        ),
        current_path=req.url.path,
    )


@rt("/resume")
def get(req):
    return Layout(read_md("resume"), cls="marked", current_path=req.url.path)


@rt("/education")
def get(req):
    with open("content/education.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    return Layout(*[EducationCard(item) for item in content], current_path=req.url.path)


@rt("/ask_llm")
def get(session, req, reset: bool = False):
    if reset:
        reset_session(session)
        return RedirectResponse(url="/ask_llm")

    messages = Agent(session["key"]).messages
    return Layout(ChatBox(messages, session["key"]), current_path=req.url.path)


@app.ws("/messages_ws")
async def messages_ws(msg: str, session_key: str, send):
    # disable input
    await send(ChatBar(enabled=False))

    agent = Agent(session_key)
    messages_len = agent.messages_len()

    # return user message directly
    await send(UserChatMessage(msg, messages_len))

    # clear the input
    await send(ChatInput())

    next_message_idx = messages_len + 1

    # send an empty message from the agent
    await send(AssistantChatMessage("🤔...", next_message_idx))
    await sleep(0.0)  # flush the event loop ?? seems weird

    output = agent.streamed_answer(msg)

    content = ""
    for chunk in output:
        delta_content = chunk.choices[0].delta.content or ""
        await send(
            ChatMessageChunk(
                delta_content, next_message_idx, clear_existing=(content == "")
            )
        )
        await sleep(0)  # flush the event loop ?? seems weird
        content += delta_content

    agent.save_answer(content)

    # re-enable input
    await send(ChatBar())


@rt("/reading_list")
def get(req, page: int = 1):
    tweets = tweets_db.fetch(page=page)
    if not tweets:
        return None

    if page > 1:
        # htmx load more request, no layout
        return TweetList(tweets, page)

    return Layout(
        TweetListHeader(tweets_db.count(), tweets_db.last_synchronized_at()),
        TweetList(tweets, page),
        current_path=req.url.path,
    )


@rt("/{fname:path}.pdf")
async def get(fname: str):
    return FileResponse(f"{fname}.pdf")


def Layout(*args, **kwargs):
    current_path = kwargs.pop("current_path")
    return (
        Title("R. Monjo"),
        NavBar(current_path=current_path),
        Main(Div(*args, **kwargs), cls="container"),
        PageFooter(),
    )


def read_md(file):
    with open(f"content/{file}.md", "r", encoding="utf-8") as f:
        content = f.read()
    return content


serve(reload=dev_env)
