from fasthtml.common import *
from components.fa import fa

def chat_box(messages_list, session_key):
  return messages(messages_list), form(session_key)

def messages(messages_list):
  messages = [chat_message(m, i) for i, m in enumerate(messages_list)]

  return Div(
    *messages,
    id="messages-list",
    style="""
      height: fit-content;
      max-height: 65vh;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      padding: 20px;
      gap: 10px;
    """
  )

def form(session_key):
  return Form(
    Group(chat_input(), Button(fa("arrow-up", size="lg"))),
    Input(type="hidden", name="session_key", value=session_key),
    hx_ext="ws",
    ws_connect=f"/messages_ws",
    ws_send=True,
    hx_on_htmx_ws_after_message="""
      var div = document.getElementById("messages-list");
      div.scrollTop = div.scrollHeight;
    """
  )

def chat_input():
  return Input(
    type="text",
    autofocus="true",
    name="msg",
    id="msg-input",
    placeholder="Type a message",
    hx_swap_oob="true"
  )

def chat_message(msg, idx):
  fn = user_chat_message if msg["role"] == "user" else assistant_chat_message
  return fn(msg["content"], idx)

def chat_message_div(*args, **kwargs):
  return Div(*args, **kwargs, hx_swap_oob="beforeend:#messages-list")

chat_bubble_style = """
  width: fit-content;
  padding: 10px 20px;
  border-radius: 20px;
"""

def user_chat_message(msg, idx):
  return chat_message_div(
    Div(
      msg,
      id=f"msg-{idx}",
      style=f"""
        margin-left: auto;
        background: rgb(244, 244, 244, 1);
        {chat_bubble_style}
      """
    )
  )

def assistant_chat_message(msg, idx):
  return chat_message_div(
    Div(
      msg,
      id=f"msg-{idx}",
      style=f"""
        background: rgb(215, 236, 247, 1);
        {chat_bubble_style}
      """
    )
  )

def chat_message_chunk(chunk, idx, clear=False):
  oob = f"innerHTML:#msg-{idx}" if clear else f"beforeend:#msg-{idx}"
  return Span(chunk, hx_swap_oob=oob)

