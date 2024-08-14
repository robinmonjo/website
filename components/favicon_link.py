from fasthtml.common import *

# credit: https://emojitofavicon.com/
def FaviconLink(emoji):
  return Link(rel="icon", href=f"data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%2210 0 100 100%22><text y=%22.90em%22 font-size=%2290%22>{emoji}</text></svg>")
