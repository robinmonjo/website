from fasthtml.common import *
from components.fa import fa
from components.atb import atb


def brand_link(name, url):
  return atb(
    fa(name, size="lg"),
    href=f"https://{url}",
    cls="contrast"
  )
