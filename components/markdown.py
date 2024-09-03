from fasthtml.common import *

# FastHTML provides a MarkdownJS component, but here it's customized to hide by default raw Markdown until it's
# parsed in order to avoid glitches when the page is rendered.


def CustomMarkdownJSAndCSS(sel=".marked"):
    markdown_css = f"""
    {sel} {{ display: none; }}
    """

    markdown_js = f"""
    import {{ marked }} from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";

    any('{sel}')?.forEach(e => {{
        e.innerHTML = marked.parse(e.textContent);
        e.style.display = 'block';
    }});
    """

    return (Style(markdown_css), Script(markdown_js, type="module"))
