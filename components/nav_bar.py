from fasthtml.common import *
from components.brand_link import BrandLink
from components.title import Title

def NavBar():
  return Header(
    Nav(
      Ul(
        Li(A(Title("Robin Monjo"), href="/", style="text-decoration: none;"))
      ),
      Ul(
        Li(Link("Work", href="/resume")),
        Li(Link("Education", href="/education")),
        Li(Link("Ask Phi", href="/ask_llm")),
        Li(Link("Reading List", href="/reading_list")),
        Li("|", style="color: lightgrey"),
        Li(BrandLink("linkedin", "www.linkedin.com/in/robin-monjo-b1384a59/")),
        Li(BrandLink("github", "github.com/robinmonjo")),
        Li(BrandLink("stack-overflow", "stackoverflow.com/users/251552/rmonjo"))
      )
    ),
    cls="container",
  )

def Link(label, **kwargs):
  return A(label, **kwargs, cls="contrast", style="font-size: 1.25em;")
