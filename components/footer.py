from fasthtml.common import *
from components.atb import atb
from datetime import datetime

def footer():
  return Footer(
    Hr(),
    Div(
      Small("Built with",
        atb(
          Img(src="/content/fasthtml_logo.svg", alt="FastHTML", width="60"),
          href="https://www.fastht.ml/",
          style="text-decoration: none;"
        ),
        "-",
        atb(
          "Report an issue",
          href="https://github.com/robinmonjo/website/issues"
        ),
        "-",
        atb(
          "See code",
          href="https://github.com/robinmonjo/website"
        )
      ),
      Small(
        f"© {datetime.now().year} Robin Monjo",
        style="margin-left: auto;"
      ),
      style="display: flex;"
    ),
    cls="container", style="margin-top: auto;"
  )
