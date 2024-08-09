from fasthtml.common import *
from components.fa import fa


def brand_link(name, url):
  return A(
    fa(name, size="lg"),
    rel="noopener noreferrer",
    href=f"https://{url}",
    target="_blank",
    cls="contrast"
  )
