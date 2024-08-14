from fasthtml.common import *
from components.fa import Fa
from components.atb import Atb
import json
import random


def chat_box_js():
    return """
    window.onload = (event) => {
        scrollMessagesListDown();

        const input = document.getElementById("msg-input");
        const form = document.getElementById("msg-form");
        const suggestedQuestions = document.querySelectorAll(".suggested-question");

        suggestedQuestions.forEach((div) => {
            div.onclick = () => {
            const text = div.innerText || div.textContent;
            input.value = text;
            const event = new Event("submit");
            form.dispatchEvent(event);

            deleteSuggestedQuestions();
            };
        });
        };

    const deleteSuggestedQuestions = () => {
        const div = document.getElementById("suggested-questions");
        if (div) {
            div.remove();
        }
    };

    const scrollMessagesListDown = () => {
        const div = document.getElementById("messages-list");
        div.scrollTop = div.scrollHeight;
    };
  """


def ChatBox(messages_list, session_key):
    return (
        Script(chat_box_js()),
        SuggestedQuestions(messages_list),
        Messages(messages_list),
        MessageForm(session_key),
        About(),
    )


def SuggestedQuestions(messages_list):
    if messages_list:
        return None

    with open(f"content/suggested_questions.json", "r") as f:
        questions = random.sample(json.load(f), 2)

    return Div(
        H6("👋 Ask me something 😊"),
        *[SuggestedQuestion(q) for q in questions],
        id="suggested-questions",
    )


def SuggestedQuestion(q):
    return Div(
        q,
        style=f"""
            background: rgb(244, 244, 244, 1);
            cursor: pointer;
            margin-bottom: 5px;
            {chat_bubble_style}
        """,
        cls="suggested-question",
    )


def Messages(messages_list):
    messages = [ChatMessage(m, i) for i, m in enumerate(messages_list)]

    return Div(
        *messages,
        id="messages-list",
        style="""
            height: fit-content;
            max-height: 60vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            padding: 20px;
            gap: 10px;
        """,
    )


def MessageForm(session_key):
    return Form(
        ChatBar(),
        Input(type="hidden", name="session_key", value=session_key),
        hx_ext="ws",
        ws_connect=f"/messages_ws",
        ws_send=True,
        hx_on_htmx_ws_after_message="""
            scrollMessagesListDown();
            deleteSuggestedQuestions();
        """,
        id="msg-form",
    )


def ChatBar(enabled=True):
    button_label = Fa("arrow-up", size="lg") if enabled else ""

    return Group(
        ChatInput(),
        Button(
            button_label,
            aria_busy=("true" if not enabled else "false"),
            aria_label=("Please wait" if not enabled else ""),
        ),
        id="chat-bar",
        disabled=(not enabled),
        hx_swap_oob="true",
    )


def ChatInput():
    return Input(
        type="text",
        autofocus="true",
        name="msg",
        id="msg-input",
        placeholder="Type a message",
        hx_swap_oob="true",
    )


def ChatMessage(msg, idx):
    comp = UserChatMessage if msg["role"] == "user" else AssistantChatMessage
    return comp(msg["content"], idx)


def ChatMessageDiv(*args, **kwargs):
    return Div(*args, **kwargs, hx_swap_oob="beforeend:#messages-list")


chat_bubble_style = """
  width: fit-content;
  padding: 10px 20px;
  border-radius: 20px;
  color: black;
"""


def UserChatMessage(msg, idx):
    return ChatMessageDiv(
        Div(
            msg,
            id=f"msg-{idx}",
            style=f"""
                margin-left: auto;
                background: rgb(244, 244, 244, 1);
                {chat_bubble_style}
            """,
        )
    )


def AssistantChatMessage(msg, idx):
    return ChatMessageDiv(
        Div(
            msg,
            id=f"msg-{idx}",
            style=f"""
                background: rgb(215, 236, 247, 1);
                {chat_bubble_style}
            """,
        )
    )


def ChatMessageChunk(chunk, idx, clear=False):
    oob = f"innerHTML:#msg-{idx}" if clear else f"beforeend:#msg-{idx}"
    return Span(chunk, hx_swap_oob=oob)


def About():
    return Small(
        Fa("info-circle"),
        "Please, be nice 😊. You are talking to a self hosted 3.8B parameters LLM:",
        Atb(
            "Phi 3 mini",
            href="https://huggingface.co/microsoft/Phi-3-mini-128k-instruct",
        ),
        "with 4-bit quantized weights. This is not Chat GPT 😋.",
        "Chat sessions are recorded for improvements but 100% anonymous.",
    )
