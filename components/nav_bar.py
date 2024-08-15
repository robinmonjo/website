from fasthtml.common import *
from components.brand_link import BrandLink
from components.title import Title

MENU_ITEMS = [
    ("Work", "/resume"),
    ("Education", "/education"),
    ("Ask Phi", "/ask_llm"),
    ("Reading List", "/reading_list"),
]

BRAND_ITEMS = [
    ("linkedin", "www.linkedin.com/in/robin-monjo-b1384a59/"),
    ("github", "github.com/robinmonjo"),
    ("stack-overflow", "stackoverflow.com/users/251552/rmonjo"),
]


def NavBar(current_path="/"):
    return Header(
        Nav(
            Ul(Li(A(Title("Robin Monjo"), href="/", style="text-decoration: none;"))),
            Ul(
                *[
                    Li(NavBarLink(label, href=path, focused=path == current_path))
                    for (label, path) in MENU_ITEMS
                ],
                Li("|", style="color: lightgrey"),
                *[Li(BrandLink(label, url)) for (label, url) in BRAND_ITEMS]
            ),
        ),
        cls="container",
    )


def NavBarLink(label, focused=False, **kwargs):
    style = "font-size: 1.25em;"
    if focused:
        style += " text-decoration: underline;"
    return A(label, **kwargs, cls="contrast", style=style)
