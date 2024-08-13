from fasthtml.common import *
from components.brand_link import BrandLink
from components.title import title

def nav_bar():
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
        Li(BrandLink("linkedin", "www.linkedin.com/in/robin-monjo-b1384a59/")),
        Li(BrandLink("github", "github.com/robinmonjo")),
        Li(BrandLink("stack-overflow", "stackoverflow.com/users/251552/rmonjo"))
      )
    ),
    cls="container",
  )
