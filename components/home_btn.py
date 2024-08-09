from fasthtml.common import *
from components.fa import fa

def home_btn(icon, label, href, **kwargs):
  return A(
    fa(icon, style="margin-right: 10px;"),
    label,
    fa("caret-right", style="margin-left: 10px;"),
    href=href,
    role="button",
    **kwargs
  )
