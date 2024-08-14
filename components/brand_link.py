from fasthtml.common import *
from components.fa import Fa
from components.atb import Atb


def BrandLink(name, url):
  return Atb(
    Fa(name, size="lg"),
    href=f"https://{url}",
    cls="contrast"
  )
