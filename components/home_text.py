from fasthtml.common import *
from components.css_gradients import random_gradient


def style():
    return f"""
        me {{
            font-size: 1.5em;
            text-align: center;
            line-height: 1.5em;
            strong {{
                {random_gradient()}
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                text-fill-color: transparent;
                font-size: 1.3em;
            }}

            p {{
                margin-bottom: 30px;
            }}
        }}
        """


def HomeText(*args, **kwargs):
    return Div(
        *args,
        Style(style()),
        **kwargs,
    )
