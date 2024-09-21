from datetime import datetime
from fasthtml.common import *
from components.atb import Atb


def PageFooter():
    return Footer(
        Hr(),
        Div(
            Small(
                "Built with ",
                Atb(
                    Img(
                        src="/content/fasthtml_logo.svg",
                        alt="FastHTML",
                        width="60",
                        height="20",
                    ),
                    href="https://www.fastht.ml/",
                    style="text-decoration: none;",
                ),
                "- ",
                Atb(
                    "Report an issue 🐞",
                    href="https://github.com/robinmonjo/website/issues",
                ),
                " - ",
                Atb(
                    "Show me the code 🤓", href="https://github.com/robinmonjo/website"
                ),
            ),
            Small(f"© {datetime.now().year} Robin Monjo", style="margin-left: auto;"),
            style="display: flex;",
        ),
        cls="container",
        style="margin-top: auto;",
    )
