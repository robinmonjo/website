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
            SiteIcon(),
            DesktopLinks(current_path=current_path),
        ),
        cls="container",
    )


def MobileNavBar(current_path="/"):
    return Header(
        Nav(SiteIcon(), MobileLinks(current_path=current_path)),
        cls="container",
    )


def SiteIcon():
    return Ul(Li(A(Title("Robin Monjo"), href="/", style="text-decoration: none;")))


def MenuItemsLinks(*, current_path):
    return [
        Li(NavBarLink(label, href=path, focused=path == current_path))
        for (label, path) in MENU_ITEMS
    ]


def BrandItemsLinks():
    return [Li(BrandLink(label, url)) for (label, url) in BRAND_ITEMS]


def NavBarLink(label, focused=False, **kwargs):
    style = "font-size: 1.25em;"
    if focused:
        style += " text-decoration: underline;"
    return A(label, **kwargs, cls="contrast", style=style)


def DesktopLinks(*, current_path):
    return Ul(
        *MenuItemsLinks(current_path=current_path),
        Li("|", style="color: lightgrey"),
        *BrandItemsLinks()
    )


def MobileLinks(*, current_path):
    label = "..."
    current_item = next((item for item in MENU_ITEMS if item[1] == current_path), None)
    if current_item:
        label = current_item[0]

    return Ul(
        Li(
            Details(
                Summary(label),
                Ul(*MenuItemsLinks(current_path=None), *BrandItemsLinks(), dir="rtl"),
                cls="dropdown",
            )
        )
    )
