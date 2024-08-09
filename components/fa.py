from fasthtml.common import *

def fa(name, size=""):
  size = f"fa-{size}" if size else ""
  return I(cls=f"fa fa-{name} {size}")
