from fasthtml.common import *

def fa(name, size="", **kwargs):
  size = f"fa-{size}" if size else ""
  return I(cls=f"fa fa-{name} {size}", **kwargs)
