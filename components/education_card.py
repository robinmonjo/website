from fasthtml.common import *

def education_card(item):
  lines = [
    Span(item["years"], style="margin-right: 10px;"), Strong(f"{item["establishment"]} {item["flag"]}"),
    Br(),
    item["diploma"],
  ]
  if "notes" in item: lines.extend([Br(), Em(item["notes"], style="color: grey;")])
  if "courses" in item:
    courses = Details(
      Summary("View courses"),
      Ul(
        *[Li(c) for c in item["courses"]]
      ),
      style="margin-bottom: 0; margin-top: 4px;"
    )
    lines.extend([Br(), courses])

  return Article(
    A(
      Img(src=f"/content/{item["logo"]}"),
      rel="noopener noreferrer",
      href=item["website"],
      target="_blank",
      style="width: 80px; margin-right: 20px;"
    ),
    Div(
      *lines,
      style="flex-grow: 1;"
    ),
    style="display: flex; align-items: center;"
  )
