from fasthtml.common import *
from components.fa import fa
from components.atb import Atb


def BrandLink(name, url):
  return Atb(
    fa(name, size="lg"),
    href=f"https://{url}",
    cls="contrast"
  )
