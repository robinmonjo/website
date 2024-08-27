from fasthtml.common import *
from components.css_gradients import random_gradient

ANIMATION = """
    @keyframes textShine {
        0% {
            background-position: 0% 50%;
        }
        100% {
            background-position: 100% 50%;
        }
    }
"""


def style(gradient):
    return f"""
        me {{
            {gradient}
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            text-fill-color: transparent;
            background-size: 200% auto;
            animation: textShine 5s ease-in-out infinite alternate;
            margin-bottom: 0;
        }}
        {ANIMATION}
    """


def Title(text):
    return H1(text, Style(style(random_gradient())))
