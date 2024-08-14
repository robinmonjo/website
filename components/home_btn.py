from fasthtml.common import *
from components.fa import Fa

def home_btn(icon, label, href, **kwargs):
  return A(
    Fa(icon, style="margin-right: 10px;"),
    label,
    Fa("caret-right", style="margin-left: 10px;"),
    href=href,
    role="button",
    **kwargs
  )
