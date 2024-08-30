from fasthtml.common import *
from components.brand_link import BrandLink
from components.title import Title

MENU_ITEMS = [
    ("Resume", "/resume"),
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
        DesktopNavBar(current_path=current_path, id="desktop-nav"),
        MobileNavBar(current_path=current_path, id="mobile-nav"),
        Style(
            """
            /* Base state: Hide both menus initially */
            #desktop-nav, #mobile-nav {
                display: none;
            }

            /* Display the desktop menu on larger screens */
            @media screen and (min-width: 769px) {
                #desktop-nav {
                    display: flex;
                }
            }

            /* Display the mobile menu on smaller screens */
            @media screen and (max-width: 768px) {
                #mobile-nav {
                    display: flex;
                }
            }
        """
        ),
        cls="container",
    )


def DesktopNavBar(current_path="/", **kwargs):
    return Nav(SiteIcon(), DesktopLinks(current_path=current_path), **kwargs)


def MobileNavBar(current_path="/", **kwargs):
    return Nav(SiteIcon(), MobileLinks(current_path=current_path), **kwargs)


def SiteIcon():
    return Ul(Li(A(Title("Robin Monjo"), href="/", style="text-decoration: none;")))


def BrandItemsLinks():
    return [Li(BrandLink(label, url)) for (label, url) in BRAND_ITEMS]


def NavBarLink(label, focused=False, **kwargs):
    style = "font-size: 1.25em;"
    if focused:
        style += " text-decoration: underline;"
    return A(label, **kwargs, cls="contrast", style=style)


def DesktopLinks(*, current_path):
    return Ul(
        *[
            Li(NavBarLink(label, href=path, focused=path == current_path))
            for (label, path) in MENU_ITEMS
        ],
        Li("|", style="color: lightgrey"),
        *BrandItemsLinks(),
    )


def MobileLinks(*, current_path):
    label = "Home"
    current_item = next((item for item in MENU_ITEMS if item[1] == current_path), None)
    if current_item:
        label = current_item[0]

    return Ul(
        Li(
            Details(
                Summary(label),
                Ul(
                    *[Li(A(label, href=path)) for (label, path) in MENU_ITEMS],
                    *BrandItemsLinks(),
                    dir="rtl",
                ),
                cls="dropdown",
            )
        )
    )
